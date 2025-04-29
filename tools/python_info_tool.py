"""
Python Package Information Tool

This module provides a specialized tool for retrieving information about Python packages:

1. KNOWLEDGE BASE: Contains pre-defined information about common Python packages
2. LOOKUP FUNCTION: Retrieves package details or provides a list of available packages
3. AGENT INTERFACE: Exposes the functionality through a standardized tool interface
4. ERROR HANDLING: Gracefully handles queries for packages not in the database

This tool allows AI agents to quickly access information about Python packages
without needing to search the internet or documentation sites.
"""

from llama_index.core.tools import FunctionTool, ToolMetadata
from data.sample_documents import PYTHON_PACKAGES

def _get_python_package_info(package_name: str) -> str:
    """Get information about a Python package."""
    if package_name.lower() in PYTHON_PACKAGES:
        return PYTHON_PACKAGES[package_name.lower()]
    else:
        available_packages = ", ".join(PYTHON_PACKAGES.keys())
        return f"Information about '{package_name}' is not in my database. Available packages: {available_packages}"

def get_python_info_tool():
    """Create and return a Python package info FunctionTool."""
    return FunctionTool.from_defaults(
        fn=_get_python_package_info,
        name="python_package_info",
        description="Get information about Python packages. Input should be the name of a Python package."
    )