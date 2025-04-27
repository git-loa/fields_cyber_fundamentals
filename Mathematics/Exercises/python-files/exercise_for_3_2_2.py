#!/usr/bin/python3
"""
This module contains Exercise 3.2.2

Run a randomized experiment to empirically validate the
lower bound on the Miller-Rabin test's probability of
successfully identifying a prime
"""

import random
import math

from CyberFoundations.exercise_package import is_prime


def generate_large_composite(num_bits=512):
    """
    Generate a large composite number by multiplying two large odd numbers.

    Args:
        num_bits (int): The bit length of the desired composite number.

    Returns:
        int: A composite number formed by multiplying two large odd numbers.
    """
    p = random.getrandbits(num_bits // 2) | 1  # Ensure odd
    q = random.getrandbits(num_bits // 2) | 1  # Ensure odd
    return p * q


def generate_large_composite_alt(num_bits=512):
    """
    Generate a large composite number by multiplying a random number with a small prime.

    Args:
        num_bits (int): The bit length of the random number.

    Returns:
        int: A composite number formed by multiplying a random number with a small prime.
    """
    n = random.getrandbits(num_bits) | 1  # Ensure odd number
    return n * random.choice([3, 5, 7, 11])


def generate_large_composite_with_factor(num_bits=512):
    """
    Generate a large composite number by ensuring it has a known factor.

    Args:
        num_bits (int): The bit length of the random number.

    Returns:
        int: A composite number with a known factor.
    """
    factor = random.choice([3, 5, 7, 11, 13])  # Choose a known factor
    n = random.getrandbits(num_bits) | 1  # Ensure odd number
    composite = factor * n
    return composite if composite > factor else composite + factor


def generate_carmichael(initial_k=1):
    """
    Generate a single Carmichael number using the (6k+1)(12k+1)(18k+1) formula.

    Args:
        initial_k (int): Initial value for generating Carmichael numbers.

    Returns:
        int: A Carmichael number, ensuring compositeness while passing primality tests.
    """
    k = initial_k
    while True:
        p1, p2, p3 = (6 * k + 1, 12 * k + 1, 18 * k + 1)

        if is_prime(p1) and is_prime(p2) and is_prime(p3):
            return p1 * p2 * p3  # Return the first valid Carmichael number

        k += 1


def experiment(num_witnesses, num_trials=1000, num_bits=512):
    """
    Run an experiment using the Miller-Rabin primality test to measure false negatives.

    Args:
        num_witnesses (int): Number of Miller-Rabin tests per integer.
        num_trials (int): Number of trials to run the experiment.
        num_bits (int): Bit length of generated composite numbers.

    Returns:
        tuple: Empirical probability of misclassification, theoretical lower bound.
    """
    false_negative_count = (
        0  # Tracks cases where the test fails to detect compositeness
    )

    for _ in range(num_trials):
        n = generate_large_composite(num_bits=num_bits)
        is_prime_result, _ = is_prime(n, num_wit=num_witnesses)
        if is_prime_result:  # Incorrectly classified as prime
            false_negative_count += 1

    empirical_prob = false_negative_count / num_trials
    theoretical_bound = 1 - (math.log(n) / 4**num_witnesses)

    return empirical_prob, theoretical_bound


def experiment_carmichael(num_witnesses, num_trials=1000):
    """
    Run an experiment using Carmichael numbers with the Miller-Rabin test.

    Args:
        num_witnesses (int): Number of Miller-Rabin tests per Carmichael number.
        num_trials (int): Number of trials to run the experiment.

    Returns:
        tuple: Empirical probability of misclassification, theoretical lower bound.
    """
    false_negative_count = (
        0  # Tracks cases where the test fails to detect compositeness
    )

    for _ in range(num_trials):
        n = generate_carmichael(initial_k=5)
        is_prime_result, _ = is_prime(n, num_wit=num_witnesses)
        if is_prime_result:
            false_negative_count += 1

    empirical_prob = false_negative_count / num_trials
    theoretical_bound = 1 - (math.log(n) / 4**num_witnesses)

    return empirical_prob, theoretical_bound


# Run the final experiment
print("\nRun experiment")
N = 10  # Number of Miller-Rabin tests per integer
empirical, bound = experiment(N, num_bits=1024)
print(f"Empirical probability of misclassification: {empirical}")
print(f"Theoretical lower bound: {bound}")

# Run experiment using Carmichael numbers
print("\nRun experiment using Carmichael numbers only")
N = 5  # Number of Miller-Rabin tests per number
empirical_c, bound_c = experiment_carmichael(N)
print(f"Empirical probability of misclassification (Carmichael numbers): {empirical_c}")
print(f"Theoretical lower bound: {bound_c}")
