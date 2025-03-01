#!/usr/bin/python3
"""
This module contain the function group_pow
"""


def group_pow(func, n: int, x, identity=None):
    """
    General group exponentiation. Computes the exponentiation of element x.
    That is x^n or n*x depending on the group operation.

    Parameters
    ----------
    func: any
        A binary function func(x,y) which represents a group operation
    n: int
        A natural number exponent
    x: any
        Agroup element
    identity: any
        Indentity of group.
        1 for multiplication and 0 for addition.

    Returns
    -------
    x^n or n*x depending on the group operation
    """

    if identity is None:
        raise ValueError("Identity element required.")

    base = x
    elmt = identity

    # Implementing the fast powering algorithm
    while n > 0:
        if n % 2 == 1:
            elmt = func(elmt, base)
        base = func(base, base)
        n = n // 2
    return elmt


if __name__ == "__main__":
    print("\nTest cases:")
    print("-------------------------------------------")
    k, s = 45, 34
    print(
        f"group_pow(lambda x,y : x+y, 45, 34) = {group_pow(lambda x,y : x+y, k, s, 0)}"
    )
    print(
        f"group_pow(lambda x,y : (x*y)%67, 45, 34) = {group_pow(lambda x,y : (x*y)%67, k, s, 1)}"
    )
