#!/usr/bin/python3
"""
exercise_for_1_4.py - This module contains functions for Exercise 1.4
"""
import random
from CyberFoundations import exercise_package as pk

######################################################################
#################### Exercise 1: Miller-Rabin Primality Test #########


# @pk.timer
def is_prime(n: int, num_wit: int = 40) -> tuple[bool, list]:
    """
    Test for probable primeness of n.

    Parameter
    ---------
    n: int
        Integer to determine its primeness.
    N: int
        The number of possible test witness to use (The number of compositeness tests to run).

    Return
    ------
    tuple[bool, set]:
        bool: True if prime, False otherwise.
        list: A witness or non witnesses.

    Raises
    ------
    TypeError:
        Bothe n and N must be integers.
    PositiveNumberError:
        Both n and N must be positive
    NumberTooSmall:
        n be at least 2. However, a large will generate a large safe prime.
    """
    if not isinstance(n, int) or not isinstance(num_wit, int):
        raise TypeError(f"Both numbers {n} and {num_wit} must be integers.")

    if n <= 0:
        raise pk.PositiveNumberError(n)

    if num_wit <= 0:
        raise pk.PositiveNumberError(num_wit)

    if n == 1:
        raise pk.NumberTooSmallError(n)

    if n in (2, 3):
        return True, []
    test_witnesses = [random.randint(2, n - 2) for _ in range(num_wit)]
    for a in test_witnesses:
        if pk.miller_rabin(n, a) == "Composite":
            return False, [a]
    return True, test_witnesses


########################### End Exercise 1 #############################
########################################################################


######################################################################
################# Exercise 2: Generating Large Primes ################
# @pk.timer
def get_prime(n: int):
    """
    Generate a prime number p which is between 2^n and 2^(n+1) using an infinite loop.
    The loop discontinues once a candidate found.

    Parameter
    ---------
    n: int
        Integer size parameter such that p is in (2^n, 2^(n+1)

    Return
    ------
    int:
        A prime number

    Raises
    ------
    TypeError:
        n must be an integer.
    PositiveNumberError:
        n must be a positive number
    NumberTooSmall:
        n be at least 2. However, a large will generate a large prime.
    """

    if not isinstance(n, int):
        raise TypeError("{n} is not an integer. An integer is rquired.")

    if n <= 0:
        raise pk.PositiveNumberError(n)

    if n == 1:
        raise pk.NumberTooSmallError(n)

    lower_bound = 2**n
    upper_bound = 2 ** (n + 1)

    while True:
        p = random.randint(lower_bound, upper_bound)
        if is_prime(p)[0]:  # Is_prime returns a tuple, tuple[bool, list]
            return p


########################### End Exercise 2 #############################
########################################################################


########################################################################
#################### Exercise 3: Generating Safe Primes ################


def get_safe_prime(n: int):
    """
    Generate a safe prime number p between 2^n and 2^(n+1) given a positive number n, and such that
    p = 2q + 1, where q is also a prime nmber. The loop discontinues once a candidate found.

    Parameter
    ---------
    n: int
        Integer size parameter such that p is in (2^n, 2^(n+1)

    Raises
    ------
    TypeError:
        n must be an integer.
    PositiveNumberError:
        n must be a positive number
    NumberTooSmall:
        n be at least 2. However, a large will generate a large safe prime.

    Return
    ------
    int:
        A safe prime number
    """

    if not isinstance(n, int):
        raise TypeError("{n} is not an integer. An integer is rquired.")

    if n <= 0:
        raise pk.PositiveNumberError(n)

    if n == 1:
        raise pk.NumberTooSmallError(n)

    lower_bound = 2**n
    upper_bound = 2 ** (n + 1)

    while True:
        p = random.randint(lower_bound, upper_bound)
        if is_prime(p)[0] and is_prime(
            (p - 1) // 2
        ):  # Is_prime returns a tuple, tuple[bool, list]
            return p


########################### End Exercise 3 #############################
########################################################################


########################################################################
#################### Exercise 6: Finding Primitive Roots ###############
def get_primitive_root(p: int):
    """
    Generate a primitive root modulo p

    Parameter
    ---------
    p: int
        The modulus

    Return
    ------
    int:
        A primitive root modulo p

    Raises
    ------
    SafePrimesError:
        Number {p} is not a safe prime. A safe prime (p = 2q + 1), where q is prime, is required.
    """
    if not is_prime(p)[0] or not is_prime((p - 1) // 2):
        raise pk.SafePrimesError(p)

    # is_primitive

    for g in range(2, p):
        if pk.is_primitive(g, p):
            return g
    return None


########################### End Exercise 6 #############################
########################################################################


if __name__ == "__main__":
    print("\n--Question 3.15 | Exercise 1: Miller-Rabin Primality Test --\n")
    n_list = [1105, 294409, 294439, 118901509, 118901521, 118901527, 118915387]
    for k in n_list:
        prime_bool, witness_composite = is_prime(k)
        if prime_bool is True:
            print(
                f"{k} is probably prime. The non Miller-Rabin witnesses: {witness_composite[:10]}\n"
            )
        else:
            print(f"{k} is composite. A Miller-Rabin witness: {witness_composite[0]}\n")
    print("--- End Exercise 1  ---\n\n")

    print("\n-- Exercise 2: Generating Large Primes --\n")
    for k in range(100, 105):
        prime = get_prime(k)
        print(
            f"The randomly generated prime number in the range (2^{k}, 2^{(k+1)}) is {prime}\n"
        )
    print("-- End Exercise 2  --\n\n")

    print("\n-- Exercise 3: Generating Safe Primes --\n")
    for k in range(100, 105):
        prime = get_safe_prime(k)
        print(
            f"The randomly generated safe prime number in the range (2^{k}, 2^{(k+1)}) is {prime}\n"
        )

    print("-- End Exercise 3  --\n\n")

    print("\n-- Exercise 6: Finding Primitive Roots --\n")
    safe_prime = get_safe_prime(100)
    print(f"A safe prime is {safe_prime}\n")
    primitive_root = get_primitive_root(safe_prime)
    print(f"A primitive root modulo {safe_prime} is {primitive_root}\n")
    print("-- End Exercise 6  --\n\n")
