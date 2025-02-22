#!/usr/bin/python3

###################################################################
########## Exercise 1: Implementing the Euclidean Algorithm #######


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


###################################################################################
##############  Exersice 2: Implementing the Extended Euclidean Algorithm #########

def bezout_coeffs(m: int, n: int) -> tuple[int, int, int]:
    '''
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
    '''

    # Check if inputs are integers
    if not isinstance(m, int) or not isinstance(n, int):
        raise TypeError("Both m and n must be integers.")
    
    # When both m and n are zero.
    if m == 0 and n == 0:
        return 0,0,0 # gcd is not well-defined
    
    if m == 0:
        return n, 0, 1 # gcd = n
    
    if n == 0:
        return m, 1, 0 # gcd = m

    #Initalize values of coefficients u and v
    #  u*m + v*n = gcd

    m, n=abs(m), abs(n)
    u_m, v_m = 1, 0  # initial coefficients for m:
    u_n, v_n = 0, 1  # initial coefficients for n

    
    while n != 0:
        q = m//n # The quotient when m is divided by n
        m, n = n, m - q*n # Update m and n 

       # Update coefficients u_m, v_m, u_n and v_n
        u_m, u_n = u_n, u_m - q*u_n
        v_m, v_n = v_n, v_m - q*v_n

    # End f iteration
    # m is the gcd
    # u_m and v_m are the coefficients suc that (u_m)*m + (v_m) n = gcd
    return m, u_m, v_m


####################################################################################
############### Exercise 3: Exercise 1.12 from the Course Text #####################

def extended_gcd(a: int, b: int)-> tuple[int, int, int]:
    '''
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
    '''
     # Check if inputs are integers
    if not isinstance(a, int) or not isinstance(b, int):
        raise TypeError("Both a and b must be integers.")
    
    if a == 0:
        return b, 0, 1 # gcd = b
    
    if b == 0:
        return a, 1, 0 # gcd = a
    
     # When both m and n are zero.
    if a == 0 and b == 0:
        return 0,0,0 # gcd is not well defined.
    
	# Initialize the variables u,g,x,y 
    u, g, x, y = 1, abs(a), 0, abs(b)
    
	# A while loop that runs until y == 0
    while y != 0:
        q, r = g//y, g%y #quotient q and remainder r such that g = q * y + t
        s = u - q * x # Compute s
        u, g, x, y = x, y, s, r  # Update variables
    
    v = (g - a * u) // b  # Calculate v
    return g, u, v



if __name__ == "__main__":
    print('\n--------------------- Start Question 1 -------------------------\n')
    print(f'This is Exercise 1.1 Question 1')
    print('---------------------------------\n')
    print(f'The gcd of 12 and 8 is gcd(12,8) = {gcd(12, 8)} \n')
    print(f'The gcd of 66528 and 52920 is gcd(66528,52920) = {gcd(66528, 52920)} \n')
    print('--------------------- End Question 1  --------------------------\n\n\n')



    print('--------------------- Start Question 2 -------------------------\n')
    print(f'This is Exercise 1.1 Question 2')
    print('---------------------------------\n')
    g, x, y = bezout_coeffs(12, 8)
    print(f'The gcd of 12 and 8 from bezout_coeffs(12,8) is {g}. The bezout coefficients are {x} and {y} \n')
    g, x, y = bezout_coeffs(26513, 32321)
    print(f'The gcd of 26513 and 32321 from bezout_coeffs(26513,32321) is {g}. The bezout coefficients are {x} and {y} \n\n')

    print('--------------------- End Question 2  --------------------------\n\n\n')



    print('--------------------- Start Question 3 -------------------------\n')
    print(f'This is Exercise 1.1 Question 3')
    c1 = 12849217045006222
    c2 = 6485880443666222
    
    print('----------------------------------\n')
    k2, x2, y2 = extended_gcd(c1,c2)

    print(f'The private key used by Alice and Bob to decode their messages {c1} and {c2} is k = {k2} \n')
    print('--------------------- End Question 3  --------------------------\n\n')

