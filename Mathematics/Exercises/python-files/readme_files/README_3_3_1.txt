The python file "exercise_for_3_3_1.py" relies on the module "exercise_package.py" in the package 
CyberFoundations. The module "exercise_package.py" contains functions that "exercise_for_3_3_1.py" 
uses to produce results.

To use the "exercise_package.py", you can use one of the following import statements in "exercise_for_3_3_1.py"
(It has already been done for this exercise.)

    > from CyberFoundations.exercise_package import mod_inv, gcd, extended_gcd, mod_pow_2

Please run the file "exercise_for_3_3_1.py" using the following command:

    > python3 exercise_for_3_3_1.py 

to see the outputs for the exercise.

-----------------------------------------------------------------------------------


-------------
SOME NOTES
-------------

I was unable to solve the given discrete logarithm problem 

  g^x ≡ 4143508631 (mod p)

for the safe prime p = 102135195196922039 with primitive root g = 11 

The pollard rho algorithm runs for some prime. It seem the prime is too large.

