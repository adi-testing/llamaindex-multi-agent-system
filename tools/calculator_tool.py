import math
from llama_index.core.tools import FunctionTool, ToolMetadata

def calculate(operation: str, a: float, b: float = None) -> str:
    """Perform basic mathematical calculations."""
    try:
        if operation == "add":
            if b is None:
                raise ValueError("Second number required for addition")
            result = a + b
            return f"{a} + {b} = {result}"
            
        elif operation == "subtract":
            if b is None:
                raise ValueError("Second number required for subtraction")
            result = a - b
            return f"{a} - {b} = {result}"
            
        elif operation == "multiply":
            if b is None:
                raise ValueError("Second number required for multiplication")
            result = a * b
            return f"{a} × {b} = {result}"
            
        elif operation == "divide":
            if b is None:
                raise ValueError("Second number required for division")
            if b == 0:
                raise ValueError("Cannot divide by zero")
            result = a / b
            return f"{a} ÷ {b} = {result}"
            
        elif operation == "power":
            if b is None:
                raise ValueError("Exponent required for power operation")
            result = math.pow(a, b)
            return f"{a} ^ {b} = {result}"
            
        elif operation == "square_root":
            if a < 0:
                raise ValueError("Cannot calculate square root of negative number")
            result = math.sqrt(a)
            return f"√{a} = {result}"
            
        else:
            raise ValueError(f"Unknown operation: {operation}")
    
    except Exception as e:
        return f"Error: {str(e)}"

def get_calculator_tool():
    """Create and return a calculator FunctionTool."""
    return FunctionTool.from_defaults(
        fn=calculate,
        name="calculator",
        description="Perform mathematical calculations. Available operations: add, subtract, multiply, divide, power, square_root. For square_root, only provide the 'a' parameter."
    )