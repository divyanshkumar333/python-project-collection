import ast
import operator as op
import math

class SafeParser:
    """
    A safe mathematical expression parser that avoids using eval().
    Uses Python's ast module to parse the expression tree and recursively
    evaluates it using a whitelist of allowed nodes.
    """
    # Whitelist of binary and unary operators
    operators = {
        ast.Add: op.add,
        ast.Sub: op.sub,
        ast.Mult: op.mul,
        ast.Div: op.truediv,
        ast.FloorDiv: op.floordiv,
        ast.Mod: op.mod,
        ast.Pow: op.pow,
        ast.USub: op.neg,
        ast.UAdd: op.pos
    }

    # Whitelist of mathematical constants
    constants = {
        'pi': math.pi,
        'PI': math.pi,
        'e': math.e,
        'E': math.e
    }

    @classmethod
    def evaluate(cls, expression: str) -> float:
        """
        Parses and safely evaluates a mathematical expression string.
        
        Args:
            expression (str): The mathematical expression to evaluate.
            
        Returns:
            float: The evaluation result.
            
        Raises:
            ValueError: For invalid math syntax or unsupported operations/variables.
            ZeroDivisionError: When division or modulo by zero is attempted.
            OverflowError: When calculations exceed maximum float limits.
        """
        cleaned = expression.strip()
        if not cleaned:
            raise ValueError("Expression is empty.")

        try:
            # Parse in 'eval' mode (expects a single expression)
            node = ast.parse(cleaned, mode='eval')
        except SyntaxError as e:
            raise ValueError(f"Syntax error: {e.msg} at position {e.offset}") from e

        return cls._eval(node.body)

    @classmethod
    def _eval(cls, node) -> float:
        # Number literal compatibility across Python versions
        if hasattr(ast, 'Constant') and isinstance(node, ast.Constant):
            if isinstance(node.value, (int, float)):
                return float(node.value)
            raise ValueError(f"Unsupported literal type: {type(node.value).__name__}")
        elif hasattr(ast, 'Num') and isinstance(node, getattr(ast, 'Num')):
            return float(node.n)
        
        # Name resolution for constants
        elif isinstance(node, ast.Name):
            if node.id in cls.constants:
                return cls.constants[node.id]
            raise ValueError(f"Undefined variable/constant '{node.id}' is not allowed.")
        
        # Binary Operations (e.g., 2 + 3)
        elif isinstance(node, ast.BinOp):
            left = cls._eval(node.left)
            right = cls._eval(node.right)
            op_type = type(node.op)
            
            if op_type in cls.operators:
                if op_type in (ast.Div, ast.FloorDiv, ast.Mod) and right == 0:
                    raise ZeroDivisionError("Division or modulo by zero.")
                try:
                    # Prevent execution of extremely large exponents to avoid hangs or crash
                    if op_type is ast.Pow and right > 10000:
                        raise OverflowError("Exponent too large; potential overflow.")
                    result = cls.operators[op_type](left, right)
                    return float(result)
                except OverflowError as e:
                    raise OverflowError("Calculation resulted in numerical overflow.") from e
            raise ValueError(f"Operator '{op_type.__name__}' is not supported.")
        
        # Unary Operations (e.g., -5)
        elif isinstance(node, ast.UnaryOp):
            operand = cls._eval(node.operand)
            op_type = type(node.op)
            
            if op_type in cls.operators:
                return float(cls.operators[op_type](operand))
            raise ValueError(f"Unary operator '{op_type.__name__}' is not supported.")
        
        # Fallback for all other AST elements (e.g., Call, Attribute, List, Dict)
        else:
            raise ValueError(f"Expression contains unsupported elements: {type(node).__name__}")
