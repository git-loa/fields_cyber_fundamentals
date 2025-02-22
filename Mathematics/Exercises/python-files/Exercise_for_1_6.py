#!/usr/bin/python3

import random
from CyberFoundations import exercise_package as pk

###############################################################
################## Exercise 1: RSA Key Generation #############

def rsa_keygen(n: int, max_iteration: int=1000) -> tuple[int, int, int]:
    """
    RSA Key Generation: Generates RSA key pairs (e, N) and (d, N), where 
    ed = 1 (mod phi_N), and phi_N is the Euler totient for N.

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
        
        N = p*q

        # Check if N is within the specified interval and Compute Euler totient for N
        if 2**n < N < 2**(n+1):
            phi_N = (p-1)*(q-1)
    
            # Chossing e randomly
            e = random.randint(3, phi_N)
            if pk.gcd(e, phi_N) != 1:
                continue # Restart if e is not co-prime with phi_N

            # Compute the modulo inverse of e
            d = pk.mod_inv(e, phi_N)

            return e, d, N 
    raise pk.IterationLimitReached(n, max_iteration)
##################### End Exercise 1 #########################
##############################################################



#######################################################################################
################## Exercise 2: Implementing RSA Encryption and Decryption #############
#---------- Encryption function---------
def rsa_encrypt(m: int, e: int, N: int):
    """
    Encrypts the message m by computing m^e (mod N)
    using the public key pair (N, e)

    Parameters
    ----------
    m: int
        The message to be encrypted
    e: int
        The exponent 
    N: int
        The modulus

    """
    return pk.mod_pow_2(m, e, N)


# ------------ Decryption Function
def rsa_decrypt(c: int , d: int , N: int):
    """
    Decrypts the message c by computing c^d (mod N)
    using pair (N, d)

    Parameters
    ----------
    c: int
        The message to be decrypted
    d: int
        The exponent 
    N: int
        The modulus
    """
    return pk.mod_pow_2(c, d, N)
####################################### End Exercise 2 ################################
#######################################################################################


##########################################################################
######################### Begin Optional ###############################

def break_rsa(e: int , N: int , p: int , c: int):
    """
    Break RSA: Decrypts a ciphertxt c = m^e (mod N) for some unknown message m.

    Parameters
    ----------
    e: int
        A public encryption exponent e for N
    N: int
        An RSA modulus N
    p: int 
        A prime factor p of N
    c: int 
         A ciphertxt c = m^e (mod N) for some unknown message m

    Returns
    -------
    int:
        Decrypted message
    """
    q = N//p
    if pk.is_prime(q)[0]:
        phi_N = (p-1)*(q-1)
        d = pk.mod_inv(e, phi_N)
    else:
        return None

    return rsa_decrypt(c, d, N)

#@pk.timer
def rsa_factor(N, phi_N, sqrt_option = "o")->tuple[int, int]:
    """
    Generate the primes p and q such that  N = p*q

    Parameters
    ----------
    N: int
        The number to decompose as p*q
    phi_N: int
        The Euler totient for N.
    sqrt_options: str
        An option to compute the square root: ('o', 'n', 'b')
        'o'--Odinary Square root
        'n'--Square root using Newton Raphson method
        'b'--Square root leveraging Binary search algorithm

    Returns
    -------
    tuple[int, int]: (p, q)
        p and q a re prime numbers
    """
    # Compute the sum of the primes
    sum_p_q = N - phi_N + 1  # N = p*q,  phi_N = (p-1)*(q-1)

    # Compute the discriminant of the equation x^2 - (p+q) + p*q = 0
    discriminant = sum_p_q**2 - 4*N

    #Compute the square root of the discriminant.
    if sqrt_option == "o":
        sqrt_discriminant = int(discriminant)**0.5 # Odinary square root
    if sqrt_option == "n":
        sqrt_discriminant = pk.sqrt_newton_raphson(int(discriminant)) # Newton Raphson
    if sqrt_option == "b":
        sqrt_discriminant = pk.sqrt_binary_search(int(discriminant)) # Binary Search
    
    # Compute the roots of the quadratic
    p = round(sum_p_q + sqrt_discriminant)//2
    q = round(sum_p_q - sqrt_discriminant)//2

    return p, q






if __name__ == "__main__":
    print("\n-------------- Using functions from Exercise 1 and 1-------------------\n")
    e, d, N = rsa_keygen(30)
    print(f"Encryption key pair: (e, N) = {(e, N)}. ")
    print(f"Decryption key pair: (d, N) = {(d, N)}. ")
    #print(f"A prime factor for {N} is {p}")
    m = random.randint(1, N)
    while m >= N:
        m = random.randint(1, N)
    print(f"Message to encrypt is {m}.")
    c = rsa_encrypt(m, e, N) # c = m^e (mod N)
    print(f"The ciphertext for the message is {c}.")
    decrytp_c = rsa_decrypt(c, d, N)
    print(f"The decrypted message is {decrytp_c}.")
    assert(m == decrytp_c)
    print("\n ---------------- End -----------------\n\n")


    print("\n ------------------------------- Optional  Exercice 2 ----------------------------- \n")
    print(f"Odinary Square root: {rsa_factor(221, 192, "o")}")
    print(f"Square root using Newton Raphson method: {rsa_factor(221, 192, "n")}")
    print(f"Square root leveraging Binary search algorithm: {rsa_factor(221, 192, "b")}\n\n")

    print(f"Odinary Square root: {rsa_factor(2430101, 2426892, "o")}")
    print(f"Square root using Newton Raphson method: {rsa_factor(2430101, 2426892, "n")}")
    print(f"Square root leveraging Binary search algorithm: {rsa_factor(2430101, 2426892, "b")}")
    print("\n --------------------------------------- End -------------------------------------------\n\n")


    
    

    
    