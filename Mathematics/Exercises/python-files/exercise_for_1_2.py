#!/usr/bin/python3
"""
exercise_for_1_2.py - This module contains functions for Exercise 1.2
"""
import functools
import time


###############################################
# IGNORE: It is a   decorator to check the perfomace
# of function by time.

# Exercices are below.

################## Timer decorator ############
###############################################


def timer(func):
    """
    Print the runtime of the decorated function
    """

    @functools.wraps(func)
    def _timer(*args, **kwargs):
        start_time = time.perf_counter()
        value = func(*args, **kwargs)
        end_time = time.perf_counter()
        run_time = end_time - start_time
        print(f"Finished {func.__name__}() in {run_time:.4f} secs")
        return value

    return _timer


#####################################################
#####################################################


##############################################################
############# Start of exercise 1.2.1: Modular Inverse #######
##############################################################
def mod_inv(a: int, n: int) -> int:
    """
    Computes the inverse modulo n of an integer a.

    Parameter
    ---------
    a: int
        Inter to finds it inverse
    n: int
        The modulus

    Returns
    -------
    int: The inverse modulo b such that ab = 1 (mod n)

    Raises
    ------
    ValueError(f"Inverse does not exist because {a} and {n} are not coprimes (GCD = {gcd})")
    """

    # Inner function
    def extended_gcd(a: int, b: int) -> tuple[int, int, int]:
        """
        Computes the gcd of a and b, and finds the coefficients
        u and v such that u a + v b = gcd(a,b)

        Parameters
        ----------
        a: int
            First integer
        b: int
            Second integer

        Returns
        -------
        tuple[int, int, int]
            First int is the gcd.
            Second int is the u coefficient.
            Third int is the v coefficient.

        Raises
        ------
        TypeError: Both parameters a and  b must be integers

        Example:
        -------
        try:
            inverse1 = mod_inv(a1, n1):
            print(f"The inverse of {a1} modulo {n1} is {inverse1}")
        except ValueError as e:
            print(e)

        """
        # Check if inputs are integers
        if not isinstance(a, int) or not isinstance(b, int):
            raise TypeError("Both a and b must be integers.")

        if a == 0:
            return b, 0, 1  # gcd = b

        if b == 0:
            return a, 1, 0  # gcd = a

        # When both m and n are zero.
        if a == 0 and b == 0:
            return 0, 0, 0  # gcd is not well defined.

        # Initialize the variables u,g,x,y
        u, g, x, y = 1, abs(a), 0, abs(b)

        # A while loop that runs until y == 0
        while y != 0:
            q, t = g // y, g % y  # quotient q and remainder t such that g = q * y + t
            s = u - q * x  # Compute s
            u, g, x, y = x, y, s, t  # Update variables

        v = (g - a * u) // b  # Calculate v
        return g, u, v  # return the gcd, and the coefficients

    # Compute the gcd and the corresponding coefficients.
    gcd, u, _ = extended_gcd(a, n)  # u*a + v*n = gcd

    # Check if gcd = 1
    if gcd != 1:
        raise ValueError(
            f"Inverse does not exist because {a} and {n} are not coprimes (GCD = {gcd})"
        )

    return u % n  # Returns u (mod n)


############# End of exercise 1.2.1: Modular Inverse #############
##################################################################


########################################################################
############# Start of exercise 1.2.2:  Fast Powering Algorithm ########
########################################################################
# @timer
def mod_pow(a: int, e: int, n: int) -> int:
    """
    Computes a**e (mod n), where a is the base,
    e is the exponent and n is the modulus

    parameters
    ----------
    a: int
        The base
    e: int
        The exponent
    n: int
        The modulus

    Returns
    -------
    int: a**e (mod n )
    """

    ## Inner function to return binary representation.

    def binary_epansion(m: int) -> list:
        """
        Compute the binary represetation of m.
        """
        if m == 0:
            return [0]
        bin_list = []

        # Use bitwise operation to find the binary representation
        while m > 0:
            bin_list.append(m & 1)
            m >>= 1
        return bin_list

    bin_list = binary_epansion(e)  # binary representation of e as a list

    # Compute a^(2^r) (mod n)
    pow_a_mod_n = [
        (a ** (2**r)) % n for r, _ in enumerate(bin_list)
    ]  # compute the powers of a modulo n

    prod = 1
    for reduced_mod_n in [i**j for i, j in zip(pow_a_mod_n, bin_list)]:
        prod = prod * reduced_mod_n

    return prod % n


############# End of exercise 1.2.2: Fast Powering Algorithm ###########
########################################################################


###################################################################################
############# Start of exercise 1.2.3: Improved Fast Powering Algorithm ###########
# #################################################################################
# @timer
def mod_pow_2(g, e, m):
    """
    Computes g**e (mod m), where g is the base, e is the exponent
    and N is the modulus.

    parameters
    ----------
    g: int
        The base
    e: int
        The exponent
    m: int
        The modulus

    Returns
    -------
    int: g**e (mod m)
    """

    a, b = g, 1
    while e > 0:
        if (e - 1) % 2 == 0:
            b = (b * a) % m
        a, e = (a * a) % m, e // 2
    return b


############# End of exercise 1.2.3: Improved Fast Powering Algorithm #########
###############################################################################


####################################################################
############# Start of exercise 1.2.4: Euler Totient Function ######
####################################################################


def phi(n: int):
    """
    Computes the Euler totient of n.

    Parameter
    ---------
    n: int
        Number whose Euer totient is to be computed.

    Return
    ------
    int:
        number of integers  is coprimes to n
    """

    # Inner function returns the gcd of a and b
    def gcd(a, b):
        while b != 0:
            a, b = b, a % b
        return a

    count = 0
    for i in range(1, n + 1):
        if gcd(n, i) == 1:
            count += 1
    return count


# @timer
def fast_phi(n: int):
    """
    Compute the Euler totient of using prime factorization technique

    Parameter
    ---------
    n: int
        Number whose Euer totient is to be computed.

    Return
    ------
    int:
        number of integers  is coprimes to n
    """
    count = n  # Initialze count as n
    p = 2  # Start with the smallest prime

    # Compute n(1-1/p1)...(1-1/pk) -- p1, ... pk are prime numbers
    # Loop though potential prime factors of n starting with p =2
    while p * p <= n:  # Using the square root technique
        # Check if p is a factor of n
        if n % p == 0:
            # If p is a factor, then update count by the factor (1 - 1/p)
            while n % p == 0:
                n //= p  # Divied by p until p is completely eliminated (p is not a factor).
            count -= count // p  #  \phi(n) = n(1-1/p)
        p += 1  # Move to the next potential factor

    # After smaller primes.
    if n > 1:  # If n > 1, then it is a prime factor greater that square of n
        count -= count // n
    return count  # Return the number of integers coprime to n.


############# End of exercise 1.2.4: Euler Totient Function ########
####################################################################

if __name__ == "__main__":

    ## Start of testing exercise 1.2.1
    print("\n-- Start of testing exercise 1.2.1 --\n")
    a0, n0 = 21454362362356235, 34623572343523462537647
    a1, n1 = 7, 24
    a2, n2 = 4, 5
    a3, n3 = 3, 5
    a4, n4 = 4, 8

    # Testing function for
    # a0, n0 = 21454362362356235, 34623572343523462537647
    try:
        INV0 = mod_inv(a0, n0)
        print(f"The inverse of {a0} modulo {n0} is {INV0}")
    except ValueError as e:
        print(e)

    # Testing function for
    # a1, n1 = 7, 24
    try:
        INV1 = mod_inv(a1, n1)
        print(f"The inverse of {a1} modulo {n1} is {INV1}")
    except ValueError as e:
        print(e)

    # Testing function for
    # a2, n2 = 4, 5
    try:
        INV2 = mod_inv(a2, n2)
        print(f"The inverse of {a2} modulo {n2} is {INV2}")
    except ValueError as e:
        print(e)

    # Testing function for
    #  a3, n3 = 3, 5
    try:
        INV3 = mod_inv(a3, n3)
        print(f"The inverse of {a3} modulo {n3} is {INV3}")
    except ValueError as e:
        print(e)

    # Testing function for
    # a4, n4 = 4, 8
    try:
        INV4 = mod_inv(a4, n4)
        print(f"The inverse of {a4} modulo {n4} is {INV4}")
    except ValueError as e:
        print(e)
    print("\n-- End of testing exercise 1.2.1 --\n\n")
    ## End of testing exercise 1.2.1

    ## Start of testing exercise 1.2.2
    print("\n-- Start of testing exercise 1.2.2 --\n")
    print(f"mod_pow(3, 218, 1000) = {mod_pow(3,218, 1000)}\n")
    print(f"mod_pow(17,183, 256) = {mod_pow(17,183, 256)}\n")
    print(f"mod_pow(2, 477, 256) = {mod_pow(2, 477, 1000)}\n")
    print(f"mod_pow(11, 507, 1237) = {mod_pow(11, 507, 1237)}\n")
    print("\n-- End of testing exercise 1.2.2 --\n\n")
    ## End of testing exercise 1.2.2

    ## Start of testing exercise 1.2.3
    print("\n-- Start of testing exercise 1.2.3 --\n")
    print(f"mod_pow_2(3, 218, 1000) = {mod_pow_2(3,218, 1000)}\n")
    print(f"mod_pow_2(17,183, 256) = {mod_pow_2(17,183, 256)}\n")
    print(f"mod_pow_2(2, 477, 256) = {mod_pow_2(2, 477, 1000)}\n")
    print(f"mod_pow_2(11, 507, 1237) = {mod_pow_2(11, 507, 1237)}\n")
    print("\n-- End of testing exercise 1.2.3 --\n\n")
    ## End of testing exercise 1.2.3

    ## Start of testing exercise 1.2.4
    print("\n-- Start of testing exercise 1.2.4 --\n")
    print(f"Euler totient of 24 is phi(24) = {phi(24)}\n")
    print(f"Euler totient of 500 is phi(500) = {phi(500)}\n")
    print(f"Euler totient of 4567 is phi(4567) = {phi(4567)}\n\n")

    print(f"Euler totient of 24 is fast_phi(24) = {fast_phi(24)}\n")
    print(f"Euler totient of 500 is fast_phi(500) = {fast_phi(500)}\n")
    print(f"Euler totient of 4567 is fast_phi(4567) = {fast_phi(4567)}")
    print("\n-- End of testing exercise 1.2.4 --\n\n")
    ## End of testing exercise 1.2.4
