#!/usr/bin/python3

import random

class Ring:
    def __init__(self, addition, multiplication, unit, zero, additive_inverse):

        """
        A class to represent a ring.

        Attributes
        ----------
            addition: binary function representing addition operation
            multiplication: binary function representing multiplication operation
            unit: the unit element for the ring. 
            zero: the zero element for the ring
            additive_inverse: the additive inverse function for the ring

        Methods
        -------
            reduce(poly): Remove every instance of the ring zero object from the end of a list (poly)
            degree(poly): The degree of a polyomial
            polynomial_multiplication(poly1, poly2): 'Multiply' of two polynomials
            polynomial_addition(poly1, poly2): 'Add' two polynomials
            scalar_multiply(poly, scalar): multiply a polynomial by a scalar

        """
        self.add = addition
        self.mult = multiplication
        self.one = unit
        self.zero = zero
        self.add_inv = additive_inverse


    def reduce(self, poly: list) -> list:
        """
        Remove every instance of the ring zero object from the end of a list.

        Parameters:
        poly (list): Coefficients of the polynomial.

        Returns:
        list: Trimmed coefficients of the polynomial.
        """
        trimmed_poly = poly[:]
        while trimmed_poly and trimmed_poly[-1] == self.zero:
            trimmed_poly.pop()
        return trimmed_poly

    def degree(self, poly: list) -> int:
        """
        Compute the degree of a polyomial

        Parameters:
        -----------
            poly (list): Coefficients of the polynomial.

        Returns:
        --------
            int: degree of poly.
        """
        if poly == []:
            return 0
        else:
            return len(poly) - 1

    # Exercise 1: Polynomial Multiplication
    def polynomial_multiplication(self, poly1, poly2):
        """
        Perform polynomial multiplication.

        Parameters:
            poly1 (list): Coefficients of the first polynomial.
            poly2 (list): Coefficients of the second polynomial.

        Returns:
            list: Coefficients of the resulting polynomial after multiplication.
        """
        # Your code here
        num_of_coeff = len(poly1) + len(poly2) - 1 # Number of coefficients afer multiplication.
        result = [self.zero]*num_of_coeff

        for i in range(len(poly1)):
            for j in range(len(poly2)):
                result[i+j] = self.add(result[i+j], self.mult(poly1[i], poly2[j]))
        return self.reduce(result)

    # Exercise 2: Polynomial Addition
    def polynomial_addition(self, poly1, poly2):
        """
        Perform polynomial addition.

        Parameters:
            poly1 (list): Coefficients of the first polynomial.
            poly2 (list): Coefficients of the second polynomial.

        Returns:
            list: Coefficients of the resulting polynomial after addition.
        """
        # Your code here
        # Length of longer polynomial
        max_len = max(len(poly1), len(poly2))

        #Extend shorter polynomial with zeros
        poly1 = poly1 + [self.zero]*(max_len - len(poly1))
        poly2 = poly2 + [self.zero]*(max_len - len(poly2))

        #Add the corresponding coefficients
        result = [self.add(poly1[i], poly2[i]) for i in range(max_len)]
        return self.reduce(result)
        
    # Exercise 3: Scalar Multiplication
    def scalar_multiply(self, poly, scalar):
        """
        Perform scalar multiplication of a polynomial by a ring element.

        Parameters:
        poly (list): Coefficients of the polynomial.
        scalar: The ring element to multiply by.

        Returns:
        list: Coefficients of the resulting polynomial after scalar multiplication.
        """
        # Your code here

        result = [self.zero]*len(poly)
        for k in range(len(poly)):
            result[k] = self.mult(scalar, poly[k])

        return self.reduce(result)

    def __str__(self):
        return f"Ring with unit: {self.one} and zero: {self.zero}"
    
    def __repr__(self):
        return f"Ring(addition={self.add}, multiplication={self.mult}, unit={self.one}, zero={self.zero}, additive_inverse={self.add_inv})"

class Field(Ring):
    def __init__(self, addition, multiplication, unit, zero, additive_inverse, multiplicative_inverse):
        """
        A class to represent a field.

        Attributes
        ----------
            addition: binary function representing addition operation
            multiplication: binary function representing multiplication operation
            unit: the unit element for the ring. 
            zero: the zero element for the ring
            additive_inverse: the additive inverse function for the ring
            multiplicative_inverse: the multiplicative inverse function for the ring

        Methods
        -------
            Extends the Ring class
            polynomial_division(poly1, poly2): Perform polynomial division.
            extended_euclidean(poly1, poly2): Extended Euclidean Algorithm for polynomials over a field.

        """
        super().__init__(addition, multiplication, unit, zero, additive_inverse)
        self.mult_inv = multiplicative_inverse

    # Exercise 4: Polynomial Division
    def polynomial_division(self, poly1, poly2):
        """
        Perform polynomial division.

        Parameters:
        poly1 (list): Coefficients of the dividend polynomial.
        poly2 (list): Coefficients of the divisor polynomial.

        Returns:
        tuple: Quotient and remainder polynomials such that poly1 = quotient * poly2 + remainder.
        """

        # Your code here
        if poly2 == [self.zero]*(self.degree(poly2) + 1):
            raise ValueError("Cannot divide by the zero polynomial")

        remainder = poly1[:]
        quotient = [self.zero]*(self.degree(remainder) - self.degree(poly2) + 1)
       
        #print(self.degree(remainder))
        
        while self.degree(remainder) >= self.degree(poly2):

            # "Divide" lead coefficients
            coeff_remainder = remainder[-1]
            coeff_divisor = poly2[-1]
            div_coeffs = self.mult(coeff_remainder, self.mult_inv(coeff_divisor))

            # Update quotient
            current_deg = self.degree(remainder) - self.degree(poly2)
            quotient[current_deg] = self.add(quotient[current_deg], div_coeffs)
            
            # Update remainder
            polx = [self.zero]*(self.degree(remainder) - self.degree(poly2) + 1)
            polx[current_deg] = 1
            scaled_polx = self.scalar_multiply(polx, self.add_inv(div_coeffs))
            remainder = self.polynomial_addition(remainder, self.polynomial_multiplication(scaled_polx, poly2))
               
        return self.reduce(quotient), self.reduce(remainder)

    # Exercise 5: Extended Euclidean Algorithm for Polynomials
    def extended_euclidean(self, a, b):
        """
        Extended Euclidean Algorithm for polynomials over a field.

        Parameters:
        a (list): Coefficients of the first polynomial.
        b (list): Coefficients of the second polynomial.

        Returns:
        tuple: (gcd, s, t) such that gcd = a * s + b * t.
        """
        # Your code here

        if a == [self.zero]*len(a) and b == [self.zero]*len(b):
            raise ValueError("Both polynomials cannot be the zero polynomial.")
        
        #Initialize the coefficients
        s, g, x, y = [self.one], a[:], [self.zero], b[:]

        while y != [self.zero]*len(y):
            q, r = self.polynomial_division(g, y) # a = bq + r, 0 <= deg(r) < deg(b) 

            # Updates
            # u = s - x * q
            u = self.polynomial_addition(s,  self.scalar_multiply(self.polynomial_multiplication(x, q) , self.add_inv(self.one)))
            s, g, x, y = x[:], y[:], u[:], r[:]
            
        # Compute t = (g - a*s)//b
        denominator = self.polynomial_addition(g,  self.scalar_multiply(self.polynomial_multiplication(a, s) , self.add_inv(self.one)))
        t, _ = self.polynomial_division(denominator, b)
        return g, s, t 



    def __str__(self):
        return f"Field with unit: {self.one} and zero: {self.zero}"
    def __repr__(self):
        return f"Field(addition={self.add}, multiplication={self.mult}, unit={self.one}, zero={self.zero}, additive_inverse={self.add_inv}, multiplicative_inverse={self.mult_inv})"

class Utility:
    """
    A utility class that provides operation on integers.

    Methods
    -------
        gcd(a, b): Computes the gcd of two integers.
        extended_gcd(a, b): Computes gcd, u, v such that gcd = ua + vb.
        mod_pow_2(g, A, N): Computes g**A (mod N).
        decompose(n): Decomposes an integer as (2^k)q where q is odd.
        miller_rabin(n, a): Determies if a number n is composite or not, given a witness a.
        mod_inv(a, n): Computes the inverse modulo n of an integer a.

    """
    @staticmethod
    def gcd(a: int, b: int) -> int:
        """
        Compute gcd of two numbers

        Parameters
        ----------
        a: int
        b: int

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
    
    @staticmethod
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

        Example:
        -------
        try:
            inverse1 = mod_inv(a1, n1):
            print(f"The inverse of {a1} modulo {n1} is {inverse1}")
        except ValueError as e:
            print(e)

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
            q, t = g//y, g%y #quotient q and remainder t such that g = q * y + t
            s = u - q * x # Compute s 
            u, g, x, y = x, y, s, t  # Update variables
        
        v = (g - a * u) // b  # Calculate v
        return g, u, v #return the gcd, and the coefficients

    @staticmethod
    def mod_pow_2(g, A, N):
        """
        Computes g**A (mod N), where g is the base, A is the exponent
        and N is the modulus.

        parameters
        ----------
        g: int
            The base
        A: int 
            The exponent
        N: int
            The modulus

        Returns 
        -------
        int: g**A (mod N)
        """

        a, b = g, 1
        while A > 0:
            if (A-1)%2 == 0:
                b = (b*a)%N
            a, A = (a*a)%N, A//2
        return b

    @staticmethod
    def decompose(n: int)-> tuple[int, int]:
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
        k=0
        q = n-1

        while q%2 == 0:
            q //= 2
            k += 1
        return k, q
    
    @staticmethod
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
        if n in (2,3):
            return "Test Fails"
        #1. If n is even or 1 < gcd(a, n) < n, return composite
        if n%2 == 0 or 1 < Utility.gcd(a,n) < n:
            return "Composite"
        
        #2. Write n-1 as (2^k)*q where q is odd.
        k, q = Utility.decompose(n)

        #3. Set a = a^q mod n
        a = Utility.mod_pow_2(a,q,n) # Returns a^q mod n.

        #4.  Test for composite failure
        if (a-1) % n == 0:
            return "Test Fails"
        
        #5. Loop 0 through k-1
        for i in range(k):
            #6. Test for composite failure
            if (a+1)%n == 0:
                return "Test Fails"
            # Compute a^2 mod n and assign to a
            a = Utility.mod_pow_2(a, 2, n)

        return "Composite"

    @staticmethod
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
        gcd, u, v = Utility.extended_gcd(a, n) # u*a + v*n = gcd

        # Check if gcd = 1
        if gcd != 1:
            raise ValueError(f"Inverse does not exist because {a} and {n} are not coprimes (GCD = {gcd})") 
        else:
            return u%n # Returns u (mod n)

class PrimeFiniteField(Field):
    def __init__(self, prime):
        """
        Initialize a prime finite field of order prime.

        Parameters:
        prime (int): Prime number representing the order of the field.
        """
        if not PrimeFiniteField.is_prime(prime):
            raise ValueError("Input is not a prime number.")
        
        self.prime = prime

        # Define addition, multiplication, additive inverse, and multiplicative inverse functions
        def addition(x, y):
            return (x+y) % self.prime

        def multiplication(x, y):
            return (x*y) % self.prime

        def additive_inverse(x):
            return (-x) 

        def multiplicative_inverse(x):
            return Utility.mod_inv(x, self.prime)

        super().__init__(addition, multiplication, 1, 0, additive_inverse, multiplicative_inverse)

    
    @staticmethod
    def is_prime(n: int, N: int = 40)-> bool:
        """
        Check if a number is prime.

        Parameter
        ---------
        n: int
            Integer to be checked..
        N: int
            The number of possible test witness to use (The number of compositeness tests to run).
            
        Return
        ------
        bool: 
            bool: True if n prime, False otherwise.
        """
        if not isinstance(n, int) or not isinstance(N, int):
            raise TypeError(f"Both numbers {n} and {N} must be integers.") 
        
        if n <= 0:
            raise ValueError(f"Input {n} is not a positive number")
        
        if N <= 0:
            raise ValueError(f"Input {N} is not a positive number")
        
        if n == 1:
            raise ValueError(f"Input {n} is too small.")

        if n in (2,3):
            return True
        test_witnesses = [random.randint(2, n-2) for _ in range(N)] 
        for a in test_witnesses:
            if Utility.miller_rabin(n, a) == "Composite":
                return False
        return True


    def __str__(self):
        return f"A prime finite field PrimeFiniteField({self.prime})"
    
    def __repr__(self):
        return f"PrimeFiniteField(prime={self.prime})"

class FiniteField(Field):
    def __init__(self, prime, irr_poly):
        """
        Initialize a finite field F_p[x]/(f).

        Parameters:
        prime (int): Prime number representing the order of the field.
        irr_poly (list): Coefficients of the irreducible polynomial f.
        """
        self.prime = prime
        self.prime_field = PrimeFiniteField(prime)
        self.irr_poly = irr_poly
        
        def addition(p, q):
            return self.prime_field.polynomial_addition(p, q)

        def multiplication(p, q):
            # Your code here
            pass
        
        def additive_inverse(x):
            # Your code here
            pass
        
        def multiplicative_inverse(x):
            # Your code here. Hint: use the extended Euclidean algorithm for polynomials.
            pass

        super().__init__(addition, multiplication, 1, 0, additive_inverse, multiplicative_inverse)

    def reduce_mod_irr_poly(self, poly):
        """
        Reduce a polynomial modulo the irreducible polynomial.

        Parameters:
        poly (list): Coefficients of the polynomial.

        Returns:
        list: Coefficients of the reduced polynomial modulo the irreducible polynomial.
        """
        _, remainder = self.prime_field.polynomial_division(poly, self.irr_poly)
        return remainder

if __name__ == "__main__":
    def add(x, y):
        return x + y
    
    def mult(x, y):
        return x * y
    
    def add_inv(x):
        return -x

    def  mult_inv(x):
        if x == 0:
            raise ValueError("Cannot divide by zero")
        return 1/x


    poly1 = [1,2]
    poly2 = [4,5, 9]

    ring = Ring(add, mult, 1, 0, add_inv)
    print(f"Product of {poly1} and {poly2} is {ring.polynomial_multiplication(poly1, poly2)}\n")
    print(f"Sum of {poly1} and {poly2} is {ring.polynomial_addition(poly1, poly2)}\n\n")


    field = Field(add, mult, 1, 0, add_inv, mult_inv)
    p1 = [1,-3,0,2]
    p2 = [1,-1]
    q, r = field.polynomial_division(p1, p2)
    print(f"Quotient: {q}")
    print(f"Remainder: {r}\n")

    p1 = [7,0,0,0,2,1]
    p2 = [-5,0,0,8]
    q, r = field.polynomial_division(p1, p2)
    print(f"Quotient: {q}")
    print(f"Remainder: {r}\n")

    p1 = [-1, 0, 1]
    p2 = [1, 0, 0, 1]
    g, s, t = field.extended_euclidean(p2, p1)
    print(f"GCD({p1, p2}) = {g}")
    print(f"Coefficients: s={s}, t = {t}\n")

    p1 = [2,0,-3,1]
    p2 = [-1,1]
    g, s, t = field.extended_euclidean(p2, p1)
    print(f"GCD({p1, p2}) = {g}")
    print(f"Coefficients: s={s}, t = {t}\n")
    
    from CyberFoundations.exercise_package import mod_inv
    field1 = Field(lambda x, y: (x+y)%13, lambda x, y: (x*y)%13, 1, 0, lambda x: -x, lambda x: mod_inv(x, 13))
    p1 = [-1, 0,0,0,0,1]
    p2 = [-3, 2, 0, 1]
    g, s, t = field1.extended_euclidean(p2, p1)
    print(f"GCD({p1, p2}) = {g}")
    print(f"Coefficients: s={s}, t = {t}\n")

    p1 = [-1, 0,0,0,0,1]
    p2 = [-3, 2, 0, 1]

    pff = PrimeFiniteField(13)
    #print(pff.polynomial_addition(p2, p1))
    #print(pff.polynomial_multiplication(p1, p2))
    print(pff.polynomial_division(p1, p2))
    #print(pff.extended_euclidean(p2, p1))

    