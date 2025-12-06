from setuptools import setup, find_packages

setup(
    name="shakespeare-ai",
    version="2.3.0",
    description="AI-Powered Book Creation & Automated Developmental Editing",
    author="Robert Monroe",
    url="https://github.com/robertmonroe/shakespeare-ai",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "typer",
        "openai",
        "python-dotenv",
        "pydantic",
        "pydantic-settings",
        "beautifulsoup4",
        "requests",
        "markdown",
        "fpdf",
        "tenacity",
        "anthropic",
        "google-generativeai",
        "rich",
    ],
    entry_points={
        "console_scripts": [
            "shakespeare=libriscribe.main:app",  # New primary command
            "libriscribe=libriscribe.main:app",  # Legacy alias for compatibility
        ],
    },
    python_requires=">=3.8",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)