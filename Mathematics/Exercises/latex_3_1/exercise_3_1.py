import math


def derangement(n):
    """Compute the number of derangements (!n) using the inclusion-exclusion principle."""
    return round(
        math.factorial(n) * sum((-1) ** k / math.factorial(k) for k in range(n + 1))
    )


# Example usage:
print(math.factorial(10) - 10 * derangement(9))
print(math.factorial(26) - 26 * derangement(25))
