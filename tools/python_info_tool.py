from llama_index.core.tools import FunctionTool, ToolMetadata
from data.sample_documents import PYTHON_PACKAGES

def get_python_package_info(package_name: str) -> str:
    """Get information about a Python package."""
    if package_name.lower() in PYTHON_PACKAGES:
        return PYTHON_PACKAGES[package_name.lower()]
    else:
        available_packages = ", ".join(PYTHON_PACKAGES.keys())
        return f"Information about '{package_name}' is not in my database. Available packages: {available_packages}"

def get_python_info_tool():
    """Create and return a Python package info FunctionTool."""
    return FunctionTool.from_defaults(
        fn=get_python_package_info,
        name="python_package_info",
        description="Get information about Python packages. Input should be the name of a Python package."
    )