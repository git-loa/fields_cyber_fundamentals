import random
import matplotlib.pyplot as plt
import android_swipe_pattern as asp
from numpy import array, sqrt, dot, degrees, arccos

def compute_angle(x: tuple[int, int], y: tuple[int, int], z: tuple[int, int]) -> float:
    """ 
    Calculate the angle between three points. 
    
    Parameters 
    ---------- 
    x, y, z : tuple[int, int] 
        Points representing the nodes. For example x = (x1, x2). 
    
    Returns 
    ------- 
    float 
        The angle in degrees between the three points. 
    """

    # Return a vector b-a 
    def vector(a,b):
        return (b[0]-a[0], b[1]- a[1])
    

    # Angle formula: v.u = |u||v|cos(theta)
    u = vector(x,y)
    v = vector(z,y)

    dot_product = dot(array(u), array(v)) # Compute dot product using the dot function from numpy module
    norm_u = sqrt(u[0]**2 + u[1]**2) # Norm of the vector u
    norm_v = sqrt(v[0]**2 + v[1]**2) # Norm of the vector v
    cos_theta = dot_product/ (norm_u * norm_v) ## From angle formula
    
    return degrees(arccos(cos_theta))

def angle_change(pattern: tuple[int, ...]) -> int:
    """
    Compute the number of angle changes in the pattern.

    Parameters
    ----------
    pattern: tuple[int, ...]
        A tuple of digits from 0 to 8 representing a swipe pattern.

    Returns
    -------
    int
        The number of significant angle changes in the pattern.
    """
    coordinate_of_nodes = [(asp.row(node), asp.col(node)) for node in pattern]
    number_of_angle_changes = 0

    # Loop through the coordinates of the nodes
    for i in range(1, len(coordinate_of_nodes)-1):
        #Compute angle between two vectors formed by three points.
        angle = compute_angle(coordinate_of_nodes[i-1], coordinate_of_nodes[i], coordinate_of_nodes[i+1])
        if angle != 180:
            
            number_of_angle_changes += 1

    return number_of_angle_changes


def calculate_direction(a: int, b: int) -> str: 
    """ 
    Calculate the direction of the move from a to b. 

    Parameters 
    ---------- 
    a : int 
        Starting index. 
    b : int 
        Ending index. 
        
    Returns 
    ------- 
    str 
        Direction of the move: "horizontal", "vertical", "diagonal", or "same". 
    """ 
    row_a, col_a = asp.row(a), asp.col(a) # Coordinates of node a
    row_b, col_b = asp.row(b), asp.col(b) # Coordinates of node b
    if row_a == row_b and col_a != col_b: 
        return "horizontal" 
    elif col_a == col_b and row_a != row_b: 
        return "vertical" 
    elif row_a != row_b and col_a != col_b: 
        return "diagonal" 
    else: 
        return "same"

def complexity_score(pattern: tuple[int, ...]) -> int:
    """
    Compute the complexity score of a pattern using the metrics:
        Length of pattern
        Changes in direction
        Changes in angle

    Parameters
    ----------
    pattern: tuple[int, ...]
        A tuple of digits from 0 to 8 representing a swipe pattern.

    Returns
    -------
    int 
        The complexity score of the pattern
    """

    score = 0

    #Length of pattern
    score += len(pattern)
    
    # Changes in direction
    for i in range(2,len(pattern)):
        previous_direction = calculate_direction(pattern[i-2], pattern[i-1])
        current_direction = calculate_direction(pattern[i-1], pattern[i])
        if previous_direction != current_direction:
            score += 1

    # Changes in angle 
    score += angle_change(pattern=pattern)


    return score # The higher the score the more complex the pattern is.

def generate_complex_patterns(threshold: int) -> dict[int, set[tuple[int, ...]]]:
    """
    Generate swipe patterns with a complexity score above a given threshold.
    
    Parameters
    ----------
    threshold : int
        The minimum complexity score for a pattern to be included.
        
    Returns
    -------
    dict
        A dictionary of patterns meeting the complexity requirements.
    """
    all_patterns = asp.generate_patterns()
    complex_patterns = {k: set() for k in range(1, 10)}
    
    for length, patterns in all_patterns.items():
        for pattern in patterns:
            if complexity_score(pattern) >= threshold:
                complex_patterns[length].add(pattern)
    
    return complex_patterns

def random_pattern(length, pattern_dict):
    '''
    Parameters
    ----------
    length : int
        an integer length between 2 and 9
    pattern_dict : dict
        A dictionary mapping pattern lengths to sets of patterns 
        (like the output of generate_patterns, for example)

    Returns
    -------
    A random choice of pattern from pattern_dict of the prescribed
    length  
    '''
    out = random.choice(list(pattern_dict[length]))
    print(out)
    return out


def draw_arrow(i, j):
    '''
    Parameters
    ----------
    i : int
        A node between 0 and 8.
    j : int
        A node between 0 and 8.

    Returns
    -------
    None. Plots an arrow connecting node i to node j
    '''

    # The x and y coordinates of the nodes.
    x1 = asp.col(i)
    y1 = asp.row(i)
    x2 = asp.col(j)
    y2 = asp.row(j)
    dx, dy = x2 - x1, y2 - y1
   
    plt.arrow(x1, y1, dx, dy, head_width = 0.04, width = 0.01, ec ='green')
       
def draw(path):
    '''
    Parameters
    ----------
    path : tuple
        A tuple of integers representing a swipe pattern

    Returns
    -------
    None. Plots a visualization of the input pattern
    '''

    #Clear any existing plots
    plt.clf()

    #Draw the 9 dots representing the grid
    for i in range(0,3):
        for j in range(0,3):      
            plt.scatter(i, j, s=200, c='black',  edgecolors='black')
            
    #Invert the y-axis
    plt.ylim(2.1, -0.1)
    
    #Can't draw a path of length less than 2
    if len(path) < 2: 
        return
    
    #Connect each pair of adjacent nodes with an arrow:
    for i in range(len(path)-1):
        draw_arrow(path[i], path[i+1])
        
    #Display the result
    plt.savefig("swipe_pattern")
    plt.show()

if __name__ == '__main__':
    from random import choice
    pattern_dict = generate_complex_patterns(threshold=5)
    random_length = choice(range(4,10))
    pattern = random_pattern(length=random_length, pattern_dict=pattern_dict)
    draw(path=pattern)