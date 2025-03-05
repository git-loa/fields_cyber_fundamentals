#!/usr/bin/python3
"""
A package for the Exercises
"""
import functools
import time
import random


class SameLengthError(Exception):
    """
    A class to represent same length error exception
    """

    def __init__(self, cmp, congs):
        super().__init__(f"Lists {cmp} and {congs} must have the same length.")


class CoprimesError(Exception):
    """
    A class to represent coprimes error exception
    """

    def __init__(self, m_list):
        super().__init__(f"The integers in {m_list} are not pairwise coprimes.")


class PositiveNumberError(Exception):
    """
    A class to represent positive number error exception
    """

    def __init__(self, positive_number):
        super().__init__(
            f"Number {positive_number} is not positive. A positive number required."
        )


class NumberTooSmallError(Exception):
    """
    A class to represent number too small error exception
    """

    def __init__(self, n):
        super().__init__(f"Number {n} is too small")


class SafePrimesError(Exception):
    """
    A class to represent safe primes error exception
    """

    def __init__(self, p):
        super().__init__(
            f"Number {p} is not a safe prime. \
                A safe prime (p = 2q + 1), where q is prime, is required."
        )


class IterationLimitReached(Exception):
    """
    A class to represent iteration limit reached error exception
    """

    def __init__(self, n, max_iteration):
        super().__init__(
            f"Iteration limit {max_iteration} exceeded for {n}. Failed to generate RSA keys."
        )


def timer(func):
    """
    Print the run time of the decorated function
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


def gcd(a: int, b: int) -> int:
    """
    Return the gcd of a and b

    Parameters
    ----------
    a: int
    b: int

    Preconditions
    -------------
    a >= 0, b >= 0

    Returns
    -------
    int: gcd of a and b

    Raises
    ------
    TypeError: Both parameters a and  b must be integers.
    """
    # Initialize a and b

    # Check if inputs are integers
    if not isinstance(a, int) or not isinstance(b, int):
        raise TypeError("Both a and b must be integers.")

    # When both m and n are zero.
    if a == 0 and b == 0:
        return 0

    a, b = abs(a), abs(b)
    while b != 0:
        a, b = b, a % b

    return a


def bezout_coeffs(m: int, n: int) -> tuple[int, int, int]:
    """
    Computes the gcd of m and n, and finds the coefficients
    u and v such that u m + v n = gcd(m,n)

    Parameters
    ----------
    m: int
        First integer
    n: int
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
    """
    # Check if inputs are integers
    if not isinstance(m, int) or not isinstance(n, int):
        raise TypeError("Both m and n must be integers.")

    # When both m and n are zero.
    if m == 0 and n == 0:
        return 0, 0, 0  # gcd is not well-defined

    if m == 0:
        return n, 0, 1  # gcd = n

    if n == 0:
        return m, 1, 0  # gcd = m

    # Initalize values of coefficients u and v
    #  u*m + v*n = gcd

    m, n = abs(m), abs(n)
    u_m, v_m = 1, 0  # initial coefficients for m:
    u_n, v_n = 0, 1  # initial coefficients for n

    while n != 0:
        q = m // n  # The quotient when m is divided by n
        m, n = n, m - q * n  # Update m and n

        # Update coefficients u_m, v_m, u_n and v_n
        u_m, u_n = u_n, u_m - q * u_n
        v_m, v_n = v_n, v_m - q * v_n

    # End iteration
    # m is the gcd
    # u_m and v_m are the coefficients suc that (u_m)*m + (v_m) n = gcd
    return m, u_m, v_m


def decompose(n: int) -> tuple[int, int]:
    """
    Decompose an integer as (2^k)q, where q is odd.

    Parameter
    ---------
    n: int
        Integer to decompose

    Returns
    -------
    tuple[int, int]
        First int is the power k
        Second int is q.
    """
    k = 0
    q = n - 1

    while q % 2 == 0:
        q //= 2
        k += 1
    return k, q


def mod_pow_2(g, e, m):
    """
    Computes g**e (mod m), where g is the base, e is the exponent
    and m is the modulus.

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
    int: g**A (mod N)
    """

    a, b = g, 1
    while e > 0:
        if (e - 1) % 2 == 0:
            b = (b * a) % m
        a, e = (a * a) % m, e // 2
    return b


def miller_rabin(n: int, a: int) -> str:
    """
    Determies if a number n is composite or not.

    Parameters
    ----------
    n: int
        n is either a composite or not.
    a: int
        base or a witness.

    Return
    ------
    str:
        "Composite" or "Test Fails"
    """
    if n in (2, 3):
        return "Test Fails"
    # 1. If n is even or 1 < gcd(a, n) < n, return composite
    if n % 2 == 0 or 1 < gcd(a, n) < n:
        return "Composite"

    # 2. Write n-1 as (2^k)*q where q is odd.
    k, q = decompose(n)

    # 3. Set a = a^q mod n
    a = mod_pow_2(a, q, n)  # Returns a^q mod n.

    # 4.  Test for composite failure
    if (a - 1) % n == 0:
        return "Test Fails"

    # 5. Loop 0 through k-1
    for _ in range(k):
        # 6. Test for composite failure
        if (a + 1) % n == 0:
            return "Test Fails"
        # Compute a^2 mod n and assign to a
        a = mod_pow_2(a, 2, n)

    return "Composite"


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


def is_primitive(g, p):
    """
    Check if an integer g is primitive root modulo p

    Parameter
    ---------
    g: int
        The integer to check whether or not it is primitive.
    p: int
        The modulus.

    Returns
    -------
    bool:
            True if g is a primitve root modulo p.
    """
    q = (p - 1) // 2
    if (
        mod_pow_2(g, 1, p) == 0
        or mod_pow_2(g, 1, p) == 1
        or mod_pow_2(g, 1, p) == -1
        or mod_pow_2(g, q, p) == 1
    ):
        return False
    return True


def are_pairwise_coprimes(m_list):
    """
    Decide numbers in a list are coprimes
    """
    for i, _ in enumerate(m_list):
        for j in range(i + 1, len(m_list)):
            if gcd(m_list[i], m_list[j]) != 1:
                return False
    return True


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
    int: The inverse b is such that ab = 1 (mod n)

    Raises
    ------
    ValueError(f"Inverse does not exist because {a} and {n} are not coprimes (GCD = {gcd})")
    """

    # Compute the gcd and the corresponding coefficients.
    g, u, _ = extended_gcd(a, n)  # u*a + v*n = gcd

    # Check if gcd = 1
    if g != 1:
        raise ValueError(
            f"Inverse does not exist because {a} and {n} are not coprimes (GCD = {g})"
        )

    return u % n  # Returns u (mod n)


def is_prime(n: int, num_wit: int = 40) -> tuple[bool, list]:
    """
    Test for probable primeness of n.

    Parameter
    ---------
    n: int
        Integer to determine its primeness.
    num_wit: int
        The number of possible test witness to use (The number of compositeness tests to run).

    Return
    ------
    tuple[bool, set]:
        bool: True if prime, False otherwise.
        list: A witness or non witnesses.

    Raises
    ------
    TypeError:
        Both n and num_wit must be integers.
    PositiveNumberError:
        Both n and num_wit must be positive
    NumberTooSmall:
        n be at least 2. However, a large will generate a large safe prime.
    """
    if not isinstance(n, int) or not isinstance(num_wit, int):
        raise TypeError(f"Both numbers {n} and {num_wit} must be integers.")

    if n <= 0:
        raise PositiveNumberError(n)

    if num_wit <= 0:
        raise PositiveNumberError(num_wit)

    if n == 1:
        raise NumberTooSmallError(n)

    if n in (2, 3):
        return True, []
    test_witnesses = [random.randint(2, n - 2) for _ in range(num_wit)]
    for a in test_witnesses:
        if miller_rabin(n, a) == "Composite":
            return False, [a]
    return True, test_witnesses


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
        raise PositiveNumberError(n)

    if n == 1:
        raise NumberTooSmallError(n)

    lower_bound = 2**n
    upper_bound = 2 ** (n + 1)

    while True:
        p = random.randint(lower_bound, upper_bound)
        if is_prime(p)[0]:  # Is_prime returns a tuple, tuple[bool, list]
            return p


def get_prime_2(n: int):
    """
    Generate a prime number p which is between 2**(n//2) and 2**((n//2)+1) using an infinite loop.
    The loop discontinues once a candidate found.

    Parameter
    ---------
    n: int
        Integer size parameter such that p is in ( 2**(n//2),  2**((n//2)+1) )

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
        raise PositiveNumberError(n)

    if n == 1:
        raise NumberTooSmallError(n)

    lower_bound = 2 ** (n // 2)
    upper_bound = 2 ** ((n // 2) + 1)

    while True:
        p = random.randint(lower_bound, upper_bound)
        if is_prime(p)[0]:  # Is_prime returns a tuple, tuple[bool, list]
            return p


def sqrt_newton_raphson(n: float, precision=1e-10):
    """
    Find the value of x such that f(x) = x^2 - n is zero
    using the Newton Raphson's method.

    Return
    ------
    int:
        Square root of n
    """
    if n < 0:
        raise ValueError("Cannot compute square root of a negative number.")

    # Initial guess
    x = n

    # Iterate until the desired precision is reached.
    while True:
        # Compute the next approximation
        next_x = 0.5 * (x + n / x)

        # Check for convergence.
        if abs(x - next_x) < precision:
            break

        x = next_x
    return x


def sqrt_binary_search(n: float, precision=1e-100):
    """
    Find the square root of n leveraging the binary seacrh algorithm.

    Return
    ------
    int:
        Square root of n
    """
    if n < 0:
        raise ValueError("Cannot compute square root of a negative number.")

    left = float(0)
    right = n
    while True:
        mid = (left + right) / 2
        square = mid * mid

        if abs(square - n) < precision:
            return mid

        if square < n:
            left = mid
        else:
            right = mid
    return mid


def rsa_keygen(n: int, max_iteration: int = 1000) -> tuple[int, int, int]:
    """
    RSA Key Generation: Generates RSA key pairs (e, m) and (d, m), where
    ed = 1 (mod phi), and phi is the Euler totient for m.

    Parameters
    ----------
    n: int
        An integer
    max_iteration: int
        The number of iterations. This is to prevent the function from hanging.
        It could be increased for large n.
    """
    iterations = 0
    while iterations < max_iteration:
        iterations += 1

        # Get prime numbers
        p = get_prime_2(n)
        q = get_prime_2(n)
        while p == q:
            q = get_prime_2(n)

        m = p * q

        # Check if m is within the specified interval and Compute Euler totient for m
        if 2**n < m < 2 ** (n + 1):
            phi = (p - 1) * (q - 1)

            # Chossing e randomly
            e = random.randint(3, phi)
            if gcd(e, phi) != 1:
                continue  # Restart if e is not co-prime with phi_N

            # Compute the modulo inverse of e
            d = mod_inv(e, phi)

            return e, d, m
    raise IterationLimitReached(n, max_iteration)


def rsa_encrypt(m: int, e: int, md: int):
    """
    Encrypts the message m by computing m^e (mod md)
    using the public key pair (md, e)

    Parameters
    ----------
    m: int
        The message to be encrypted
    e: int
        The exponent
    md: int
        The modulus

    """
    return mod_pow_2(m, e, md)


def rsa_decrypt(c: int, d: int, md: int):
    """
    Decrypts the message c by computing c^d (mod md)
    using pair (md, d)

    Parameters
    ----------
    c: int
        The message to be decrypted
    d: int
        The exponent
    md: int
        The modulus
    """
    return mod_pow_2(c, d, md)


def break_rsa(e: int, rsa_m: int, p: int, c: int):
    """
    Break RSA: Decrypts a ciphertxt c = m^e (mod rsa_m) for some unknown message m.

    Parameters
    ----------
    e: int
        A public encryption exponent e for rsa_m
    rsa_m: int
        An RSA modulus rsa_m
    p: int
        A prime factor p of rsa_m
    c: int
         A ciphertxt c = m^e (mod rsa_m) for some unknown message m

    Returns
    -------
    int:
        Decrypted message
    """
    q = rsa_m // p
    if is_prime(q)[0]:
        phi = (p - 1) * (q - 1)
        d = mod_inv(e, phi)
    else:
        return None

    return rsa_decrypt(c, d, rsa_m)


def rsa_factor(n, phi, sqrt_option="nr") -> tuple[int, int]:
    """
    Generate the primes p and q such that  n = p*q

    Parameters
    ----------
    N: int
        The number to decompose as p*q
    phi: int
        The Euler totient for n.
    sqrt_options: str
        An option to compute the square root: ('o', 'nr', 'b')
        'o'--Odinary Square root
        'nr'--Square root using Newton Raphson method
        'b'--Square root leveraging Binary search algorithm

    Returns
    -------
    tuple[int, int]: (p, q)
        p and q a re prime numbers
    """
    # Compute the sum of the primes
    sum_p_q = n - phi + 1  # N = p*q,  phi_N = (p-1)*(q-1)

    # Compute the discriminant of the equation x^2 - (p+q) + p*q = 0
    discriminant = sum_p_q**2 - 4 * n

    sqrt_discriminant = 1
    # Compute the square root of the discriminant.
    if sqrt_option == "o":
        sqrt_discriminant = int(discriminant) ** 0.5  # Odinary square root
    if sqrt_option == "nr":
        sqrt_discriminant = sqrt_newton_raphson(int(discriminant))  # Newton Raphson
    if sqrt_option == "b":
        sqrt_discriminant = sqrt_binary_search(int(discriminant))  # Binary Search

    # Compute the roots of the quadratic
    p = round(sum_p_q + sqrt_discriminant) // 2
    q = round(sum_p_q - sqrt_discriminant) // 2

    return p, q


def group_pow(func, n: int, x, identity=None):
    """
    Group exponentiation
    """
    # Assuming e is the
    if identity is None:
        raise ValueError("Identity element required.")

    base = x
    elmt = identity

    while n > 0:
        print(f"n={n}")
        if n % 2 == 1:
            elmt = func(elmt, base)
        base = func(base, base)
        n = n // 2
    return elmt


if __name__ == "__main__":
    print(mod_inv(1, 13))
