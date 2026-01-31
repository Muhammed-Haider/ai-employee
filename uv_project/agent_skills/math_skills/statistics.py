"""Statistical functions."""

from typing import List, Union, Optional
import statistics as stats

def mean(numbers: List[Union[int, float]]) -> float:
    """Calculate the mean (average) of a list of numbers."""
    if not numbers:
        raise ValueError("Cannot calculate mean of empty list")
    return sum(numbers) / len(numbers)

def median(numbers: List[Union[int, float]]) -> float:
    """Calculate the median of a list of numbers."""
    if not numbers:
        raise ValueError("Cannot calculate median of empty list")

    sorted_numbers = sorted(numbers)
    n = len(sorted_numbers)

    if n % 2 == 1:
        # Odd number of elements
        return sorted_numbers[n // 2]
    else:
        # Even number of elements
        mid1 = sorted_numbers[n // 2 - 1]
        mid2 = sorted_numbers[n // 2]
        return (mid1 + mid2) / 2

def mode(numbers: List[Union[int, float]]) -> List[Union[int, float]]:
    """Calculate the mode(s) of a list of numbers.

    Returns a list since there can be multiple modes.
    """
    if not numbers:
        raise ValueError("Cannot calculate mode of empty list")

    frequency = {}
    for num in numbers:
        frequency[num] = frequency.get(num, 0) + 1

    max_freq = max(frequency.values())
    modes = [num for num, freq in frequency.items() if freq == max_freq]

    return modes

def variance(numbers: List[Union[int, float]], sample: bool = False) -> float:
    """Calculate the variance of a list of numbers.

    Args:
        numbers: List of numbers
        sample: If True, calculate sample variance (n-1 denominator).
                If False, calculate population variance (n denominator).
    """
    if not numbers:
        raise ValueError("Cannot calculate variance of empty list")

    n = len(numbers)
    if sample and n < 2:
        raise ValueError("Sample variance requires at least 2 numbers")

    m = mean(numbers)
    squared_diffs = [(x - m) ** 2 for x in numbers]

    denominator = n if not sample else n - 1
    return sum(squared_diffs) / denominator

def standard_deviation(numbers: List[Union[int, float]], sample: bool = False) -> float:
    """Calculate the standard deviation of a list of numbers."""
    return variance(numbers, sample) ** 0.5