import asyncio
import os
from pathlib import Path
from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel
from typing import Dict, Optional

console = Console()

class AISetupValidator:
    def __init__(self):
        self.required_vars = {
            'OPENROUTER_API_KEY': 'OpenRouter API nøkkel'
        }
        # Pek direkte på /app/.env hvor Docker mounter filen
        self.env_path = Path('/app/.env')
        console.print(f"[cyan]Leter etter .env fil i: {self.env_path.absolute()}[/cyan]")
    
    def validate_env(self) -> Dict[str, bool]:
        """Validerer alle påkrevde miljøvariabler"""
        load_dotenv(self.env_path)
        results = {}
        
        for var, description in self.required_vars.items():
            value = os.getenv(var)
            results[var] = bool(value)
            status = "[green]✓" if value else "[red]❌"
            console.print(f"{status} {description}: {'funnet' if value else 'mangler'}[/]")
        
        return results

    async def test_api_connection(self, api_key: Optional[str] = None) -> bool:
        """Tester API-tilkobling"""
        if not api_key:
            api_key = os.getenv('OPENROUTER_API_KEY')
            
        try:
            from ai_assistant.agents.openrouter_client import OpenRouterClient
            client = OpenRouterClient()
            
            test_messages = [
                {"role": "system", "content": "Du er en hjelpsom assistent."},
                {"role": "user", "content": "Si 'Test vellykket!'"}
            ]
            
            response = await client.generate_completion(
                model="anthropic/claude-2",
                messages=test_messages
            )
            
            return bool(response and 'choices' in response)
        except Exception as e:
            console.print(f"[red]API Test Feil: {str(e)}[/]")
            return False

async def run_tests():
    """Kjører alle tester"""
    console.print("\n[bold blue]Kjører AI Oppsett Tester...[/bold blue]\n")
    
    validator = AISetupValidator()
    
    # Test 1: Miljøvariabler
    console.print(Panel("[yellow]1. Validerer Miljøvariabler[/yellow]"))
    env_results = validator.validate_env()
    
    if not all(env_results.values()):
        console.print("\n[red]❌ Miljøvariabel-test feilet[/]")
        return
    
    # Test 2: API Tilkobling
    console.print(Panel("[yellow]2. Tester API Tilkobling[/yellow]"))
    api_success = await validator.test_api_connection()
    
    if api_success:
        console.print("[green]✓ API-tilkobling vellykket[/]")
    else:
        console.print("[red]❌ API-tilkobling feilet[/]")
        return
    
    console.print("\n[bold green]✨ Alle tester fullført vellykket![/]")

if __name__ == "__main__":
    asyncio.run(run_tests())