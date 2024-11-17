import asyncio
import os
from pathlib import Path
from dotenv import load_dotenv
from rich.console import Console
from rich.progress import Progress
from rich.panel import Panel

console = Console()

class AITestSuite:
    def __init__(self):
        self.console = Console()
        self.tests_run = 0
        self.tests_passed = 0
    
    async def run_all_tests(self):
        with Progress() as progress:
            task = progress.add_task("[cyan]Kjører tester...", total=4)
            
            # Test miljøvariabler
            await self.test_env_vars()
            progress.update(task, advance=1)
            
            # Test API-tilkobling
            await self.test_api_connection()
            progress.update(task, advance=1)
            
            # Test modell-liste
            await self.test_model_list()
            progress.update(task, advance=1)
            
            # Test kodeanalyse
            await self.test_code_analysis()
            progress.update(task, advance=1)
        
        self.print_summary()
    
    def print_summary(self):
        console.print(Panel(
            f"[bold]Test Resultater[/bold]\n"
            f"Tester kjørt: {self.tests_run}\n"
            f"Tester bestått: {self.tests_passed}\n"
            f"Status: {'[green]OK' if self.tests_run == self.tests_passed else '[red]FEIL'}",
            title="Test Oppsummering"
        ))

if __name__ == "__main__":
    test_suite = AITestSuite()
    asyncio.run(test_suite.run_all_tests())