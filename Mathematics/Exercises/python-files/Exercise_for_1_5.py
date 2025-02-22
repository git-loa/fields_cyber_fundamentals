#!/usr/bin/python3

from CyberFoundations import exercise_package as pk


def chinese_remainder(m_list: list, a_list: list) -> int:
    """
    Solves a simultaneous systems of congruences.

    Parameters
    ----------
    m:_list: list
        A list of coprime moduluses
    a_list:
        A list of congruences

    Return
    ------
    x: int
        solution x to the congruences x \equiv a[i] (mod m[i]) for each 0 <= i < len(ms)

    Raises
    ------
    SameLengthError:
        Lists m_list and a_list must have the same length.
    CoprimesError:
        List m_list of integers are not pairwise coprimes. Pairwise coprimes required.
        
    """
    
    # Ensure the two lists have the same length.
    if len(m_list) != len(a_list):
        raise pk.SameLengthError(m_list, a_list)
    
    # Ensure all the moduli are pairwise comprimes; 
    # raise an exception otherwise.
    if not pk.are_pairwise_coprimes(m_list):
        raise pk.CoprimesError(m_list)
    
    # Compute the product of all moduli in m_list
    N = 1
    for n in m_list:
        N *= n

    x = 0 # Set the solution to zero
    for n_i, a_i in zip(m_list, a_list):
        N_i = N//n_i 
        x_i = pk.mod_inv(N_i, n_i)
        x += a_i * N_i * x_i
    
    return x % N


if __name__ == "__main__":
    
    print("\n--------------- a. x ≡ 3 (mod 7) and x ≡ 4 (mod 9) ----------------- \n")
    try:
        m = [7, 9]
        a = [3,4] 
        print(f"The solution to the equations with moduli {m} and congruences {a} is x = {chinese_remainder(m, a)}")  
    except pk.CoprimesError as ce:
        print(ce)      
    except pk.SameLengthError as sle:
        print(sle)
    except ValueError as ve:
        print(ve)
    print("\n----------------------------- End of a. ---------------------------\n\n")


    print("\n--------------- b. x ≡ 137 (mod 423) and x ≡ 87 (mod 191) ----------------- \n")
    try:
        m = [423, 191]
        a = [137, 87] 
        print(f"The solution to the equations with moduli {m} and congruences {a} is x = {chinese_remainder(m, a)}")  
    except pk.CoprimesError as ce:
        print(ce)      
    except pk.SameLengthError as sle:
        print(sle)
    except ValueError as ve:
        print(ve)
    print("\n----------------------------- End of b. ---------------------------\n\n")



    print("\n--------------- c. x ≡ 133 (mod 451) and x ≡ 237 (mod 697) ----------------- \n")
    try:
        m = [451, 697]
        a = [133, 237] 
        print(f"The solution to the equations with moduli {m} and congruences {a} is x = {chinese_remainder(m, a)}")  
    except pk.CoprimesError as ce:
        print(ce)      
    except pk.SameLengthError as sle:
        print(sle)
    except ValueError as ve:
        print(ve)
    print("\n----------------------------- End of c. ---------------------------\n\n")




    print("\n--------------- d. x ≡ 5 (mod 9), x ≡ 6 (mod 10), and x ≡ 7 (mod 11) ----------------- \n")
    try:
        m = [9, 10, 11]
        a = [5, 6, 7] 
        print(f"The solution to the equations with moduli {m} and congruences {a} is x = {chinese_remainder(m, a)}")  
    except pk.CoprimesError as ce:
        print(ce)      
    except pk.SameLengthError as sle:
        print(sle)
    except ValueError as ve:
        print(ve)
    print("\n----------------------------- End of d. ---------------------------\n\n")


    print("\n--------------- e. x ≡ 37 (mod 43), x ≡ 22 (mod 49), and x ≡ 18 (mod 71)  ----------------- \n")
    try:
        m = [43, 49, 71]
        a = [37, 22, 18] 
        print(f"The solution to the equations with moduli {m} and congruences {a} is x = {chinese_remainder(m, a)}")  
    except pk.CoprimesError as ce:
        print(ce)      
    except pk.SameLengthError as sle:
        print(sle)
    except ValueError as ve:
        print(ve)
    print("\n----------------------------- End of e. ---------------------------\n\n")



    print("\n--------------- Exercise 2: exercise on Cryptohack: ----------------- \n")
    print("\n-- x ≡ 2 (mod 5) ")
    print("\n-- x ≡ 3 (mod 11) ")
    print("\n-- x ≡ 5 (mod 17) \n")
    try:
        m = [5, 11, 17]
        a = [2, 3, 5] 
        print(f"The solution to the equations with moduli {m} and congruences {a} is x = {chinese_remainder(m, a)}")  
    except pk.CoprimesError as ce:
        print(ce)      
    except pk.SameLengthError as sle:
        print(sle)
    except ValueError as ve:
        print(ve)
    print("\n----------------------------- End of Exercise 2: exercise on Cryptohack. ---------------------------\n\n")











