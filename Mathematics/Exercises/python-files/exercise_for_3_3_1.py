# from math import gcd
# from sympy import mod_inverse

from CyberFoundations.exercise_package import mod_inv, gcd, extended_gcd, mod_pow_2


# -------------------------------
# Field Class: Modular Arithmetic
# -------------------------------
class Field:
    """
    A finite field supporting modular arithmetic operations.

    Attributes:
    - p: Prime modulus of the field.
    """

    def __init__(self, p):
        self.p = p

    def add(self, x, y):
        return (x + y) % self.p

    def sub(self, x, y):
        return (x - y) % self.p

    def mul(self, x, y):
        return (x * y) % self.p

    def inv(self, x):
        return mod_inv(x, self.p) if gcd(x, self.p) == 1 else None

    def neg(self, x):
        return (-x) % self.p


# ---------------------------------
# CyclicGroup Class: General Group
# ---------------------------------
class CyclicGroup:
    """
    Represents a cyclic group for modular arithmetic and elliptic curves.

    Attributes:
    - generator: Base element of the group.
    - order: Number of elements in the group.
    - operation: Binary operation defining the group.
    - inverse_operation: Function for computing inverse (optional).
    - identity: Identity element in the group.
    - is_elliptic: Boolean flag indicating if the group is elliptic.
    """

    def __init__(
        self,
        generator,
        field,
        operation,
        inverse_operation=None,
        identity=None,
        is_elliptic=False,
    ):
        self.generator = generator
        self.field = field
        self.operation = operation
        self.inverse_operation = inverse_operation
        self.identity = identity
        self.is_elliptic = is_elliptic
        self.order = self.compute_order()

    def multiply(self, x, y):
        return self.operation(x, y)

    def inverse(self, x):
        return self.inverse_operation(x) if self.inverse_operation else None

    def compute_order(self):
        """Computes the order of the cyclic subgroup."""
        return self.field.p - 1 if not self.is_elliptic else self._find_elliptic_order()

    def _find_elliptic_order(self):
        """Determines the order of an elliptic curve subgroup."""
        P = self.generator
        order = 1
        while P != self.identity:
            P = self.multiply(P, self.generator)
            order += 1
        return order


# --------------------------------
# EllipticCurve Class: EC Arithmetic
# --------------------------------
class EllipticCurve:
    """
    Represents an elliptic curve over a finite field with arithmetic operations.

    Curve equation: y^2 = x^3 + ax + b (mod p)
    """

    def __init__(self, a, b, field):
        self.a = a
        self.b = b
        self.field = field

    def is_on_curve(self, P):
        """Checks whether a point P = (x, y) satisfies the elliptic curve equation."""
        if P == "INF":
            return True
        x, y = P
        left_side = self.field.mul(y, y)
        right_side = self.field.add(
            self.field.mul(x, self.field.mul(x, x)),
            self.field.add(self.field.mul(self.a, x), self.b),
        )
        return left_side == right_side

    def negate(self, P):
        """Computes the inverse (negation) of a point P on the curve."""
        if P == "INF":
            return "INF"
        x, y = P
        return (x, self.field.neg(y))

    def add(self, P, Q):
        """Elliptic curve point addition following group law."""
        if P == "INF":
            return Q
        if Q == "INF":
            return P

        x1, y1 = P
        x2, y2 = Q

        if P == Q:
            if y1 == 0:
                return "INF"
            m = self.field.mul(
                self.field.add(self.field.mul(3, self.field.mul(x1, x1)), self.a),
                self.field.inv(self.field.mul(2, y1)),
            )
        else:
            if x1 == x2:
                return "INF"
            m = self.field.mul(
                self.field.sub(y2, y1), self.field.inv(self.field.sub(x2, x1))
            )

        x3 = self.field.sub(self.field.mul(m, m), self.field.add(x1, x2))
        y3 = self.field.sub(self.field.mul(m, self.field.sub(x1, x3)), y1)

        return (x3, y3)

    def scalar_multiply(self, P, k):
        """Computes k * P using the double-and-add method."""
        if k == 0 or P == "INF":
            return "INF"

        result = "INF"
        current = P

        while k:
            if k & 1:
                result = self.add(result, current)
            current = self.add(current, current)
            k >>= 1  # Bit-shifting to divide k by 2

        return result


class Montgomery:
    """Handles Montgomery multiplication for fast modular arithmetic."""

    def __init__(self, prime):
        self.p = prime
        self.r = 1 << (prime.bit_length() + 1)  # R = 2^(bit length of p + 1)
        self.r_inv = mod_inv(self.r, self.p)
        self.p_inv = -mod_inv(self.p, self.r) % self.r

    def montgomery_reduce(self, t):
        """Reduces t using Montgomery Reduction."""
        u = (t * self.p_inv) % self.r
        result = (t + u * self.p) // self.r
        return result if result < self.p else result - self.p

    def montgomery_multiply(self, a, b):
        """Performs Montgomery multiplication (a * b) in Montgomery space."""
        t = a * b
        return self.montgomery_reduce(t)

    def to_montgomery(self, x):
        """Converts x to Montgomery space (x * R mod p)."""
        return (x * self.r) % self.p

    def from_montgomery(self, x):
        """Converts x from Montgomery space back to normal representation."""
        return self.montgomery_reduce(x)


# ------------------------------------
# Pollard's Rho Algorithm for DLP
# ------------------------------------


def solve_modular_equation(v, u, mod):
    """
    Solve modular equation: v * k ≡ u mod mod

    If gcd(v, mod) > 1, multiple solutions exist.
    """
    d, s, _ = extended_gcd(v, mod)

    if d == 1:
        return [(u * mod_inv(v, mod)) % mod]  # Single solution

    # Compute multiple solutions
    u //= d
    mod //= d
    s %= mod
    w = (s * u) % mod

    return [(w + k * mod) % (mod * d) for k in range(d)]


def pollards_rho_log_small(group, target, max_iters=10**6):
    """
    Generalized Pollard’s Rho algorithm for solving discrete logarithms in modular arithmetic.

    Arguments:
    - group: Cyclic modular group (integer exponentiation group).
    - target: Target integer in the group.
    - max_iters: Maximum iterations before aborting (default: 10^6).

    Returns:
    - x such that group.generator^x = target mod group.order.
    """

    def f(x, a, b):
        """Pseudo-random function for modular arithmetic."""
        if x < group.order // 3:
            return group.multiply(x, group.generator), (a + 1) % group.order, b
        elif x < 2 * group.order // 3:
            return group.multiply(x, x), (2 * a) % group.order, (2 * b) % group.order
        else:
            return group.multiply(x, target), a, (b + 1) % group.order

    x, a, b = group.identity, 0, 0
    X, A, B = x, a, b
    iters = 0

    while iters < max_iters:
        x, a, b = f(x, a, b)
        X, A, B = f(*f(X, A, B))

        # print(f"Iteration {iters}: x={x}, X={X}")
        if x == X:
            break
        iters += 1

    if iters == max_iters:
        raise RuntimeError("Cycle detection safeguard triggered: No solution found.")

    v = (B - b) % group.order
    u = (a - A) % group.order
    d = gcd(v, group.order)

    if d == 1:
        return (u * mod_inv(v, group.order)) % group.order

    solutions = solve_modular_equation(v, u, group.order)

    for exp in solutions:
        if mod_pow_2(group.generator, exp, group.order + 1) == target:
            return exp

    raise RuntimeError("No valid solution found among candidates.")


def pollards_rho_log_large(group, target, max_iters=10**6):
    """
    Optimized Pollard’s Rho for modular discrete logs with Montgomery multiplication.

    Arguments:
    - group: Cyclic modular group.
    - target: Target integer in the group.
    - max_iters: Maximum iterations before aborting.

    Returns:
    - x such that group.generator^x ≡ target (mod group.order).
    """

    mont = Montgomery(group.field.p)  # Initialize Montgomery operations
    target_m = mont.to_montgomery(target)  # Convert target to Montgomery space

    def f(x, a, b):
        """Pseudo-random function using Montgomery multiplication."""
        x_m = mont.to_montgomery(x)  # Convert to Montgomery space

        if x_m < group.order // 3:
            return (
                mont.montgomery_multiply(x_m, group.generator),
                (a + 1) % group.order,
                b,
            )
        elif x_m < 2 * group.order // 3:
            return (
                mont.montgomery_multiply(x_m, x_m),
                (2 * a) % group.order,
                (2 * b) % group.order,
            )
        else:
            return mont.montgomery_multiply(x_m, target_m), a, (b + 1) % group.order

    x, a, b = group.identity, 0, 0
    X, A, B = x, a, b
    iters = 0

    while iters < max_iters:
        x, a, b = f(x, a, b)
        X, A, B = f(*f(X, A, B))

        # print(f"Iteration {iters}: x={x}, X={X}")
        if x == X:
            break
        iters += 1

    if iters == max_iters:
        raise RuntimeError("Cycle detection safeguard triggered: No solution found.")

    v = (B - b) % group.order
    u = (a - A) % group.order
    d = gcd(v, group.order)

    if d == 1:
        k_m = (u * mod_inv(v, group.order)) % group.order
        return mont.from_montgomery(k_m)  # Convert back from Montgomery space

    solutions = solve_modular_equation(v, u, group.order)

    for exp in solutions:
        if mod_pow_2(group.generator, exp, group.order + 1) == target:
            return exp

    raise RuntimeError("No valid solution found among candidates.")


def pollards_rho_ecdlp(group, curve, target, max_iters=10**6):
    """
    Pollard’s Rho algorithm for solving the discrete logarithm problem on elliptic curves.

    This algorithm attempts to find an integer `k` such that:
        k * G = target
    where `G` is the generator point of the elliptic curve group.

    Parameters:
    - group (CyclicGroup): The cyclic group of the elliptic curve.
    - curve (EllipticCurve): The elliptic curve instance handling arithmetic.
    - target (tuple): The target elliptic curve point Q to solve for k.
    - max_iters (int): Maximum iterations before aborting (default: 10^6).

    Returns:
    - int: The discrete logarithm k such that k * G = target, if found.

    Raises:
    - RuntimeError: If no valid k is found within max_iters iterations.
    """

    def f(X, a, b):
        """
        Pseudo-random iteration function following partitioning rules.

        Depending on the x-coordinate of X mod 3:
        - If x % 3 == 0: Add generator point G.
        - If x % 3 == 1: Add target point Q.
        - Otherwise: Double the current point.

        Parameters:
        - X (tuple): Current elliptic curve point.
        - a (int): Current coefficient tracking generator multiplications.
        - b (int): Current coefficient tracking target multiplications.

        Returns:
        - tuple: Updated (X, a, b) values.
        """
        if X[0] % 3 == 0:
            return curve.add(X, group.generator), (a + 1) % group.order, b
        elif X[0] % 3 == 1:
            return curve.add(X, target), a, (b + 1) % group.order
        else:
            return curve.add(X, X), (2 * a) % group.order, (2 * b) % group.order

    # Initialize variables
    slow_x, a_t, b_t = group.generator, 0, 0
    fast_x, a_h, b_h = f(group.generator, 0, 0)

    iters = 0
    while slow_x != fast_x and iters < max_iters:
        slow_x, a_t, b_t = f(slow_x, a_t, b_t)
        fast_x, a_h, b_h = f(*f(fast_x, a_h, b_h))  # Advance hare twice

        # print(f"Iteration {iters}: slow_x={slow_x}, fast_x={fast_x}")
        iters += 1

    if iters == max_iters:
        raise RuntimeError("No solution found: Cycle detection safeguard triggered.")

    # Solve (b_h - b_t) * k ≡ (a_t - a_h) mod group.order
    v = (b_h - b_t) % group.order
    u = (a_t - a_h) % group.order
    d = gcd(v, group.order)

    # print(f"Equation to solve: {v} * k ≡ {u} mod {group.order} (gcd={d})")

    solutions = solve_modular_equation(v, u, group.order)

    # print("Possible discrete logarithm values:")
    for k in solutions:
        # print(f"Testing k={k} → {curve.scalar_multiply(group.generator, k)}")
        if curve.scalar_multiply(group.generator, k) == target:
            print(f"Correct Elliptic Discrete logarithm found: {k}")
            return k

    raise RuntimeError("No valid k found among solutions.")


if __name__ == "__main__":
    # ------------------------------------
    # Example Usage
    # ------------------------------------
    # Multiplicative group

    field2 = Field(48611)
    multiplicative_group = CyclicGroup(
        generator=19,
        field=field2,
        operation=lambda x, y: field2.mul(x, y),
        inverse_operation=lambda x: field2.inv(x),
        identity=1,
    )
    target_value = 24717

    print(
        f"Discrete logarithm solutions: {pollards_rho_log_small(multiplicative_group, target_value)}"
    )

    # Elliptic curve group
    field3 = Field(73)
    ec = EllipticCurve(a=8, b=7, field=field3)
    elliptic_group = CyclicGroup(
        generator=(32, 53),
        field=field3,
        operation=lambda P, Q: ec.add(P, Q),
        inverse_operation=lambda P: ec.negate(P),
        identity="INF",
    )
    target_point = (39, 17)
    pollards_rho_ecdlp(elliptic_group, ec, target_point)

    # Example Usage with 56-bit Safe Prime
    large_prime = 102135195196922039
    mod_group = CyclicGroup(
        generator=7,  # Example primitive root mod p
        field=Field(large_prime),
        operation=lambda x, y: (x * y) % large_prime,  # Modular multiplication
        inverse_operation=lambda x: mod_inv(x, large_prime),
        identity=1,
        is_elliptic=False,
    )
    target_value = 23  # Example target
    k_mod = pollards_rho_log_large(mod_group, target_value, max_iters=10**20)
    print(f"The discrete logarithm k (Modular with large prime): {k_mod}")
