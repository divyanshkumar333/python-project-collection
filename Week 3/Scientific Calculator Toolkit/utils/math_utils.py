import math

class MathUtilities:
    """
    Implements mathematical helper functions, constants, and formula reference utilities.
    """

    # Mathematical Constants
    CONSTANTS = {
        "Pi (π)": (math.pi, "Ratio of a circle's circumference to its diameter"),
        "Euler's number (e)": (math.e, "Base of the natural logarithm"),
        "Golden Ratio (φ)": ((1.0 + math.sqrt(5)) / 2.0, "Mathematical ratio of beauty/harmony (≈ 1.618)"),
        "Euler-Mascheroni constant (γ)": (0.5772156649015328, "Limiting difference between harmonic series and natural log")
    }

    # Formula Reference Cheat Sheet
    FORMULAS = {
        "Geometry - Area": [
            "Circle: Area = π * r^2",
            "Rectangle: Area = l * w",
            "Triangle: Area = 0.5 * b * h"
        ],
        "Geometry - Volume": [
            "Sphere: Volume = (4/3) * π * r^3",
            "Cylinder: Volume = π * r^2 * h",
            "Cube: Volume = s^3"
        ],
        "Algebra & Calculus": [
            "Quadratic Formula: x = (-b ± √(b^2 - 4ac)) / 2a",
            "Pythagorean Theorem: a^2 + b^2 = c^2",
            "Euler's Identity: e^(i*π) + 1 = 0"
        ],
        "Financial Math": [
            "Simple Interest: I = (P * R * T) / 100",
            "Compound Interest: A = P * (1 + R/100)^N - P",
            "EMI = [P * r * (1+r)^n] / [(1+r)^n - 1]"
        ]
    }

    @staticmethod
    def is_prime(n: int) -> bool:
        """Checks if an integer is prime."""
        if n < 2:
            return False
        if n == 2:
            return True
        if n % 2 == 0:
            return False
        for i in range(3, int(math.isqrt(n)) + 1, 2):
            if n % i == 0:
                return False
        return True

    @staticmethod
    def check_even_odd(n: int) -> str:
        """Returns whether a number is Even or Odd."""
        return "Even" if n % 2 == 0 else "Odd"

    @staticmethod
    def gcd(a: int, b: int) -> int:
        """Calculates Greatest Common Divisor of two integers."""
        return math.gcd(a, b)

    @staticmethod
    def lcm(a: int, b: int) -> int:
        """Calculates Least Common Multiple of two integers."""
        if a == 0 or b == 0:
            return 0
        return abs(a * b) // math.gcd(a, b)

    @staticmethod
    def generate_fibonacci(n: int) -> list[int]:
        """Generates the first N terms of the Fibonacci sequence."""
        if n <= 0:
            return []
        elif n == 1:
            return [0]
        
        sequence = [0, 1]
        while len(sequence) < n:
            sequence.append(sequence[-1] + sequence[-2])
        return sequence[:n]
