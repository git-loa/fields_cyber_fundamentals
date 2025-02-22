#!/usr/bin/ python3
# -*- coding: utf-8 -*-

"""
Exercise: Android swipr pattern
Created: on Tue Dec 17 2024
@author: Leonard Okyere Afeke
"""


# ##############  Exercise 1: #####################
# Define two Python functions row(i) and col(i) 
# that map an index between 0 and 8 to its respective 
# row and column in the 3 x 3 grid representation

def row(i : int)->int:
    """ 
    Determine the row of index `i` in a 3x3 grid. 

    Parameters 
    ---------- 
    i : int 
        An index between 0 and 8. 
        
    Returns 
    ------- 
    int 
        The row number (0, 1, or 2) of the index `i`. 
    
    Example 
    ------- 
    >>> row(5) #(Second row) 
    1
    Raises 
    ------ 
    TypeError 
        If `i` is not an integer. 
    IndexError 
        If `i` is not between 0 and 8 inclusive. 
    """
    if not isinstance(i, int):
        raise TypeError(f"Sorry. '{i}' must be an integer")
    
    if i not in range(0, 9):
        raise IndexError(f"Sorry. '{i}' must be a number between 0 and 8 inclusive.")
    
    
    return i//3

def col(i:int) -> int:
    """
    Determine the column of index `i` in a 3x3 grid. 

    Parameters
    ----------
    i : int
        An index between 0 and 8. 

    Returns
    --------
    int
        The column number (0,1, or 2) of the index 'i'.

    Example 
    -----------------------
    >>> col(5) #(Third column)
    2

    Raises 
    ------ 
    TypeError 
        If `i` is not an integer. 
    IndexError 
        If `i` is not between 0 and 8 inclusive. 
    """
    if not isinstance(i, int):
        raise TypeError(f"Sorry. '{i}' must be an integer")
    
    if i not in range(0, 9):
        raise IndexError(f"Sorry. '{i}' must be a number between 0 and 8 inclusive.")
    
    
    return i%3


#print(f'Row of index 5: {row(2)}')
#print(f'Column of index 5: {col(5)}')


##############  Exercise 2: #####################
# Write a Python function that takes two node indices
# i and j between 0 and 8 representing nodes in the 
# pattern grid. If there is an intermediate node between 
# i and j, your function should return this node. 
# Otherwise, it should return -1


def intermediate_node(i: int, j: int) -> int:
    """
    Determine the intermediate node `k` lying between `i` and `j` in a 3x3 grid, if it exists.
    
    Parameters
    ----------
    i : int 
        An index between 0 and 8.
    j : int 
        An index between 0 and 8.

    Returns
    -------
    int
        The node `k` lying between `i` and `j` if it exists, otherwise -1.

    Raises
    ------
    TypeError
        If `i` or `j` is not an integer.
    IndexError
        If `i` or `j` is not between 0 and 8 inclusive.
    
    Examples
    --------
    >>> intermediate_node(0, 8)
    4
    >>> intermediate_node(1, 5)
    -1
    """
    if not all(isinstance(index, int) for index in (i, j)):
        raise TypeError(f"Sorry, both '{i}' and '{j}' must be integers")
    
    if not all(0 <= index <= 8 for index in (i, j)):
        raise IndexError(f"Sorry, both '{i}' and '{j}' must be numbers between 0 and 8 inclusive.")
    
    col_set = {col(i), col(j)}
    row_set = {row(i), row(j)}
    
    # Checking for an intermediate in a column.
    if abs(row(i) - row(j)) == 2 and len(col_set) == 1:
        return (i + j) // 2
    
    # Checking for an intermediate in a row.
    if abs(col(i) - col(j)) == 2 and len(row_set) == 1:
        return (i + j) // 2
    
    # Checking for an intermediate in a diagonal.
    if len(row_set) == 2 and len(col_set) == 2 \
        and abs(row(i) - row(j)) == 2 and abs(col(i) - col(j)) == 2:
        return (i + j) // 2
    
    return -1



####################################################
####################################################
# Helper function for Exercise 3: is_valid_pattern.
####################################################

def is_valid_pattern(pattern: tuple[int, ...])->bool: 
    """ 
    Determines if the given swipe pattern is valid according to Android pattern rules. 

    Parameters 
    ---------- 
    pattern : tuple 
        A tuple of digits from 0 to 8 representing a swipe pattern. 
          
    Returns 
    ------- 
    bool 
        True if the pattern is valid, False otherwise. 
    """ 
    
    # Empty pattern ()
    if len(pattern) == 0: 
        return True 
    
    # Non-empty pattern
    for i in range(1, len(pattern)): 
        if pattern[i] in pattern[:i]:
            False

        intermediate = intermediate_node(pattern[i-1], pattern[i])         
        if intermediate != -1 and intermediate not in pattern[i-1:i+1]: 
            return False 
    return True

###############################################
###############################################


##############  Exercise 3: #####################
def is_admissible(pattern: tuple[int, ...], i: int) -> bool:
    """
    Determines if the index i can be appended to the given pattern

    Parameters
    ----------
    pattern: tuple of int
        A tuple of digits from 0 to 8 representing a valid swipe pattern
    i: int
        An integer between 0 to 8 representing a potential extension node.

    Returns
    -------
    bool
        True if index i can be appended to pattern, False otherwise.
    """

    if i in pattern:
        return False
    
    new_pattern = pattern + (i,)
    return is_valid_pattern(new_pattern)


##############  Exercise 4: #####################
def extensions(pattern: tuple[int, ...]) -> set[tuple[int, ...]]:
    
    """
    Extends a pattern by one more node.

    Parameters
    ----------
    pattern : tuple
        A tuple of digits from 0 to 8 representing a valid swipe
        pattern

    Returns
    -------
        The set of all possible extensions of pattern by 1 more node. 
    """

    set_of_tuples = set()

    for i in range(9):
        if is_admissible(pattern, i):
            extended_pattern = pattern + (i,)
            set_of_tuples.add(extended_pattern)
        
    return set_of_tuples


#############  Exercise 5: #####################
def generate_patterns()-> dict:
    """
    Generate all swipe pattern of length 1 to 9 and return then as a dictionary.

    Returns
    -------
    dict
        A dictionary whose keys are integers 0 through 9 and whose 
        value at integer `i` is the set of all swipe patterns of length `i`
    """

    patterns = {k : set() for k in range(10)}

    # patterns of length 1
    for i in range(9):
        patterns[1].add((i,))

    for k in range(2,10):
        for pattern in patterns[k-1]:
            new_pattern = extensions(pattern)
            patterns[k].update(new_pattern)
    return patterns



if __name__ == '__main__':
    
    #############  Exercise 6: #####################
    pattern_dict = generate_patterns()
    pattern_length_4_or_more = sum(len(pattern_dict[i]) for i in range(4,10))
    pattern_length_9 = len(pattern_dict[9])
    print(pattern_length_9)
    print(f"Number of possible swipe patterns of length 4 or more: {pattern_length_4_or_more}")
    print(f"Number of possible swipe patterns of length 9: {pattern_length_9}")



    #############  Exercise 7: #####################
    filtered_patterns = []
    pattern_dict = generate_patterns()
    for pattern in pattern_dict[9]:
        if (pattern[0], pattern[1]) == (1,0) and pattern[-2:] == (7,8)\
            and 4 in pattern and 6 in pattern\
                and 4 in pattern[:pattern.index(6)+1]:
            filtered_patterns.append(pattern)
    number_of_valid_patterns = len(filtered_patterns)

    print(f"Number of possible swipe patterns fitting the description is: {number_of_valid_patterns}")