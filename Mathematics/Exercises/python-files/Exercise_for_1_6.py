#!/usr/bin/python3

"""
This module is for Exercise 1.6
"""

import random
from CyberFoundations import exercise_package as pk

###############################################################
################## Exercise 1: RSA Key Generation #############


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
        p = pk.get_prime_2(n)
        q = pk.get_prime_2(n)
        while p == q:
            q = pk.get_prime_2(n)

        m = p * q

        # Check if m is within the specified interval and Compute Euler totient for m
        if 2**n < m < 2 ** (n + 1):
            phi = (p - 1) * (q - 1)

            # Chossing e randomly
            e = random.randint(3, phi)
            if pk.gcd(e, phi) != 1:
                continue  # Restart if e is not co-prime with phi_N

            # Compute the modulo inverse of e
            d = pk.mod_inv(e, phi)

            return e, d, m
    raise pk.IterationLimitReached(n, max_iteration)

##################### End Exercise 1 #########################
##############################################################


#######################################################################################
################## Exercise 2: Implementing RSA Encryption and Decryption #############
# ---------- Encryption function---------

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
    return pk.mod_pow_2(m, e, md)


# ------------ Decryption Function

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
    return pk.mod_pow_2(c, d, md)


####################################### End Exercise 2 ################################
#######################################################################################


##########################################################################
######################### Begin Optional ###############################



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
    if pk.is_prime(q)[0]:
        phi = (p - 1) * (q - 1)
        d = pk.mod_inv(e, phi)
    else:
        return None

    return rsa_decrypt(c, d, rsa_m)


# @pk.timer
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
        sqrt_discriminant = pk.sqrt_newton_raphson(int(discriminant))  # Newton Raphson
    if sqrt_option == "b":
        sqrt_discriminant = pk.sqrt_binary_search(int(discriminant))  # Binary Search

    # Compute the roots of the quadratic
    p = round(sum_p_q + sqrt_discriminant) // 2
    q = round(sum_p_q - sqrt_discriminant) // 2

    return p, q



if __name__ == "__main__":
    print("\n-- Using functions from Exercise 1 and 1 --\n")
    expo, dexpo, N = rsa_keygen(30)
    print(f"Encryption key pair: (e, N) = {(expo, N)}. ")
    print(f"Decryption key pair: (d, N) = {(dexpo, N)}. ")
    # print(f"A prime factor for {N} is {p}")
    rand_num = random.randint(1, N)
    while rand_num >= N:
        rand_num = random.randint(1, N)
    print(f"Message to encrypt is {rand_num}.")
    enc_num = rsa_encrypt(rand_num, expo, N)  # c = m^e (mod N)
    print(f"The ciphertext for the message is {enc_num}.")
    decrytp_num = rsa_decrypt(enc_num, dexpo, N)
    print(f"The decrypted message is {decrytp_num}.")
    assert rand_num == decrytp_num
    print("\n ---------------- End -----------------\n\n")

    print(
        "\n -- Optional  Exercice 2 -- \n"
    )
    print(f"Odinary Square root: {rsa_factor(221, 192, "o")}")
    print(f"Square root using Newton Raphson method: {rsa_factor(221, 192, "nr")}")
    print(
        f"Square root leveraging Binary search algorithm: {rsa_factor(221, 192, "b")}\n\n"
    )

    print(f"Odinary Square root: {rsa_factor(2430101, 2426892, "o")}")
    print(
        f"Square root using Newton Raphson method: {rsa_factor(2430101, 2426892, "nr")}"
    )
    print(
        f"Square root leveraging Binary search algorithm: {rsa_factor(2430101, 2426892, "b")}"
    )
    print(
        "\n -- End --\n\n"
    )
