"""
Project Setup Configuration

This setup.py file configures the llamaindex-multi-agent package for development and installation:

1. PACKAGE DISCOVERY: Automatically finds all directories with __init__.py files and includes them as packages
2. ROOT MODULES: Explicitly includes standalone Python modules in the project root (config.py)
3. DEVELOPMENT MODE: When installed with 'pip install -e .', creates a link to the source code
   instead of copying it, allowing for immediate code changes without reinstallation

Key benefits:
- Resolves import errors by making all modules available in the Python path
- Allows imports like 'from knowledge_base.vector_store import KnowledgeBase' from anywhere
- Creates a proper Python package structure for better organization

To install in development mode:
    pip install -e .

For production installation:
    pip install .
"""

from setuptools import setup, find_packages

setup(
    name="llamaindex-multi-agent",
    version="0.1",
    packages=find_packages(),  # This will automatically find all packages
    py_modules=['config'],     # Still need this for individual modules
)