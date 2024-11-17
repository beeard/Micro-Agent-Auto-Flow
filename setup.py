from setuptools import setup, find_packages

setup(
    name="ai-assistant",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "click",
        "pydantic",
        "aiohttp",
        "redis",
        "networkx",
        "anthropic",
        "openai"
    ],
    entry_points={
        'console_scripts': [
            'ai-assistant=ai_assistant.cli:cli',
        ],
    },
)