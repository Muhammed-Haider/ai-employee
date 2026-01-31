"""Example usage of math skills."""

import sys
import os

# Add project root to path to import skills
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from skills.math_skills import calculator, statistics

    print("=== Math Skills Examples ===\n")

    # Calculator examples
    print("Calculator Operations:")
    print(f"  5 + 3 = {calculator.add(5, 3)}")
    print(f"  10 - 4 = {calculator.subtract(10, 4)}")
    print(f"  6 * 7 = {calculator.multiply(6, 7)}")
    print(f"  15 / 3 = {calculator.divide(15, 3)}")

    # Statistics examples
    numbers = [1, 2, 3, 4, 5, 5, 6, 7, 8, 9, 10]
    print(f"\nStatistics for numbers: {numbers}")
    print(f"  Mean: {statistics.mean(numbers):.2f}")
    print(f"  Median: {statistics.median(numbers)}")
    print(f"  Mode: {statistics.mode(numbers)}")
    print(f"  Variance: {statistics.variance(numbers, sample=True):.2f}")
    print(f"  Standard Deviation: {statistics.standard_deviation(numbers, sample=True):.2f}")

    # More complex example
    print("\nComplex Calculation:")
    result = calculator.add(
        calculator.multiply(3, 4),
        calculator.divide(20, 5)
    )
    print(f"  3 * 4 + 20 / 5 = {result}")

except ImportError as e:
    print(f"Error importing math skills: {e}")
    print("Make sure you're running from the project root directory.")
except Exception as e:
    print(f"Error: {e}")