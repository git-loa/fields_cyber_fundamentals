# Euclidean and Extended Euclidean Algorithm

### Euclidean Algorithm
> **Theorem** *(Quotient-Remainder Theorem)* For all $n \in \mathbb{Z}$ and $d \in \mathbb{Z}$, if $d\ne 0$ then there exit $q \in \mathbb{Z}$ and $r \in \mathbb{Z}$ such that $n = qd + r$ and $0 \le r < |d|.$ Moreover, thses $q$ and $r$ are unique for a given $n$ and $d$.

> **Theorem** For all $a, b \in \mathbb{Z}$ where $b\ne 0$, $gcd(a,b) = gcd(b, a\% b)$.
>
> > For example since $24 \% 16 = 8$, then $gcd(24,16) = gcd(16, 8) = gcd(8,0) = 8.$

> **Euclidean Algorithom:**
>
> The steps of the Euclidean Algorithm consist of the following:
> 1. **Initialization:** 
>       - Start with two positive integers, $a$ and $b$, where $a \ge b$.
> 2. **Iteration:** 
>       - Divide $a$ by $b$ and find the remainder $r$. 
>       - Replace $a$ with $b$ and $b$ with $r$.
>       - Repeat the process until $b = 0$.
> 3. **Result:**
>       - When b is zero, $a$ is the gcd of $a$ abd $b$.

The Euclidean Algorithm consists of a sequence of divisions with remainder. From this sequence, we get a formula $r_{i-1} = r_i q_i + r_{i+1}$, where $r_0 = a$ and $r_1=b$

``` pseudocode
Given: non-negative integers a and b.

Returns: gcd(a, b).

1. Initialize two variables x, y to the given numbers a and b.
2. Let r be the remainder when x is divided by y.
3. Reassign x and y to y and r, respectively.
4. Repeat steps 2 and 3 until y is 0.
5. At this point, x refers to the gcd of a and b.

```

```python
def euclidean_gcd(a: int, b: int) -> int:
    """Return the gcd of a and b.

    Preconditions:
    - a >= 0
    - b >= 0
    """
    # Step 1: initialize x and y
    x, y = a, b

    while y != 0:  # Step 4: repeat Steps 2 and 3 until y is 0
        assert math.gcd(x, y) == math.gcd(a, b)  # (NEW) Loop invariant

        # Step 2: calculate the remainder of x divided by y
        r = x % y

        # Step 3: reassign x and y
        x, y = y, r

    # Step 5: x now refers to the gcd of a and b
    return x
```

### Bezout identity and the Extended Euclidean Algorithm
> **Theorem** *(Extended Euclidean Algorithm)* Let $a$ and $b$ be positive integers. Then the equation $au + bv = gcd(a,b)$ always has a solution in integers $u$ and $v$.

**Mathematics**

The Euclidean Algorithm gives the formula $r_{i-2} = r_{i-1} \cdot q_{i-1} + r_{i}$ where $r_0 = a$ and $r_1=b$

> Rewrite:  $r_i = r_{i-2} - r_{i-1} \cdot q_{i-1}$,

At each iteration, we perform the Euclidean division: 
- $r_i = r_{i-2} - r_{i-1} \cdot q_{i-1}$. 
- We maintain the coefficients such that $r_i = u_i\cdot a + v_i\cdot b$
- The next iteration is $r_{i+1} = r_{i-1} - r_{i} \cdot q_{i}$.
- Substitute $r_i = u_i\cdot a + v_i\cdot b$ and $r_{i-1} = u_{i-1}\cdot a + v_{i-1}\cdot b$. We obtain the following recursive formulas for the coefficients
  
> $u_i = u_{i-2} - u_{i-1} \cdot q_{i-1}$
>
> $v_i = v_{i-2} - v_{i-1} \cdot q_{i-1}$


# Modular Arithmetic
1. Modular Operations
        
   - **Congruent modulo:** Let $m\ge 1$ be an integer. The integers $a$ and $b$ are *congruent modulo* $m$ if their difference $a-b$ is divisible by $m$: $a \equiv b\; (mod\;\; m)$
   - **Multiplicative inverse:** Let $a$ be and integer. Then $a\cdot b\;\equiv\; 1\; (mod \; m)$ for some integer $b$ $\iff$ $gcd(a,m) = 1$. The integer $b$ is called the *multiplicative inverse* of $a$ modulo $m$.
2. Modular Arithmetic and Shift Ciphers
   
   - (Ciphertext Letter) $\equiv$ (Plaintext Letter) $+$ (Secret Key) $(mod \; 26)$
   - Let  $c=$ Ciphertext Letter, $p=$ Plaintext Letter, $k=$ Secret Key. Then 
     - Encryption: $c \equiv p+k (mod \; 26)$ and  Decryption: $p \equiv c-k (mod \; 26)$
  
- Understand mechanics and performance of fast-powering algorithm
- Implement the fast-powering algorithm in Python

3. Modular Inverse
4. Fast Powering Algorithm
   
   Computing $g^A (mod \; N)$ for large $A$.

# Irreducibility Tests in $F_p[T]$
***Theorem:*** Let $f(T) \in \mathbb{F}_p[T]$ have degree $d \ge 2$. Then $f(T)$ is irreducible if and only if $f(T)$ is not divisible by any nonconstant monic polynomial of degree at most d/2. 

***Proof***
1. ***If $f(T)$ is irreducible, it is not divisible by any non-constant monic polynomial of degree at most $d/2$.*** 

    Assume $f(T)$ is irreducible, and suppose it divible by a monic polynomial $g(T)$ of degree at most d/2. Then we can write $f(T) = h(T)g(T)$ for some $h(T) \in \mathbb{F}_p[T]$.

    Since $g(T)$ is monic and has degree at most d/2, the degree of $h(T)$ must be 
    $$\deg(h(T)) = d - \deg(g(T)) \ge d - d/2 > 0.$$
    This implies that $f(T)$ can be factored into two non-constant polynomials $g(T)$ and $h(T)$, contradicting the irreducibility of $f(T)$. 
2. ***If $f(T)$ is not divisible by any nonconstant monic polynomial of degree at most d/2, then $f(T)$ is irreducible.***
    
    Assume $f(T)$ is not divisible by any nonconstant monic polynomial of degree at most d/2. Suppose $f(T) = h(T)g(T)$, where $g(T)$ and $h(T)$ are non-constant polynomials. 

    WLOG, assume that $\deg(g(T)) \le \deg(h(T))$. Since $\deg(f(T)) = d$, then 
    $$\deg(g(T)) + \deg(h(T)) = d.$$
    Since both $g(T)$ and $h(T)$ are non-constants, we have $1 \le \deg(g(T)) \le d/2$. 
    
    But this constradicts the assumptions that $f(T)$ is not divisible by a non-constant monic polynomial od degree at mot d/2.

***Theorem*** If $\pi$ is irreducible in $\mathbb{F}_p[T]$ then $a^{N(\pi)-1} \equiv 1 \mod \pi$ for all $g \in \mathbb{F}_p[T]$ such that $(g,\pi) = 1$.

***Proof***



Great question! **Pollard’s rho algorithm** for discrete logarithms works by finding **collisions** in a pseudo-random sequence of elements within a cyclic group. Let me break it down step by step:

### **1. Goal of Pollard’s Rho**
We want to solve the **discrete logarithm problem**, meaning we need to find an integer $x$ such that:

$$
g^x \equiv h \mod p
$$

or more generally:

$$
\text{group operation}(g, x) = h
$$

in **any cyclic group**, not just modular arithmetic.

### **2. Why Use Pollard’s Rho?**
Instead of **brute-force searching** for $x$, which takes **O(N)** time (where $N$ is the group size), **Pollard’s rho** speeds up the process using **random walks and cycle detection**, making it much closer to **O(√N) complexity**.

### **3. How It Works**
#### **Step 1: Define a Random Walk in the Group**
We define a function that randomly **moves through group elements**, modifying the exponent `x` via three cases:
- **Case 1:** Multiply by $g$, increasing $x$.
- **Case 2:** Square the value, doubling $x$.
- **Case 3:** Multiply by $h$, modifying $x$ another way.

This walk ensures a **pseudo-random progression**, leading to eventual **collisions**.

#### **Step 2: Use Floyd’s Cycle Detection**
Instead of storing all previous values, we use **two iterators**:
- **Slow iterator (`x, a, b`)** moves **step by step**.
- **Fast iterator (`X, A, B`)** moves **twice as fast**.

Eventually, because the sequence is **finite**, they will hit a **collision** where:

$$
x = X
$$

At this point, we extract the exponents from both sequences and solve:

$$g^{a - A} \equiv h^{B - b} \mod p$$

#### **Step 3: Solve Using Modular Arithmetic**
The equation $v \cdot x \equiv u \mod (p-1)$ is solved using the **extended Euclidean algorithm**, which finds the **modular inverse** and yields \( x \).

---

### **4. Why Does `hash(x) % 3` Matter?**
The **`hash(x) % 3` condition** helps determine which transformation case to apply:
- **Randomly partitions the sequence** for better distribution.
- **Avoids predictable patterns** in modular arithmetic.
- **Ensures efficient cycling**, helping with **faster collision detection**.

If we didn't use hashing, the algorithm might **fall into repetitive loops**, missing valid collisions.

---

### **5. Summary**
 **Pollard’s rho reduces complexity from O(N) to O(√N)** using cycle detection.  
 **Randomized transformations ensure efficient searching in cyclic groups**.  
 **Floyd’s cycle detection avoids unnecessary memory storage**.  
 **Extended Euclidean algorithm solves the final modular equation**.  

This method is widely used in **cryptography**, **security analysis**, and **number theory**!  Would you like me to refine any part further?