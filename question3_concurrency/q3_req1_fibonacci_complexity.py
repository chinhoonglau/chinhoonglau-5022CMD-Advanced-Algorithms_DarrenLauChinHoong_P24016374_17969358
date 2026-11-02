"""Question 3 - Requirement 1: Fibonacci Function, Primitive Operation Count & Big-O Analysis.

Implements the iterative nth Fibonacci algorithm (F(0)=0, F(1)=1) and provides an
exact primitive-operation counter demonstrating T(n) = 4n + 3 -> O(n) linear time
complexity and O(1) auxiliary variable space.
"""

from __future__ import annotations
import sys as _sys
from pathlib import Path as _Path
for _p in (_Path(__file__).resolve().parent, _Path(__file__).resolve().parents[1]):
    if str(_p) not in _sys.path:
        _sys.path.insert(0, str(_p))

from dataclasses import dataclass

FIBONACCI_TARGETS: tuple[int, int, int] = (35, 38, 40)
DEFAULT_ROUNDS: int = 10


def calculate_fibonacci(n: int) -> int:
    """Calculate the nth Fibonacci number iteratively (F(0)=0, F(1)=1).

    Primitive operation breakdown:
      - Initialization `prev, curr = 0, 1`: 2 assignments
      - Loop runs n iterations; each iteration performs:
          1 loop variable advance/check,
          1 addition (`prev + curr`),
          2 variable rebindings (`prev = curr`, `curr = next_val`) -> 4 primitive ops/iter
      - Final `return prev`: 1 return operation
      Total primitive operations: T(n) = 4n + 3 = O(n).
    """
    if isinstance(n, bool) or not isinstance(n, int):
        raise TypeError("Fibonacci index n must be an integer.")
    if n < 0:
        raise ValueError("Fibonacci index n must be non-negative.")

    prev, curr = 0, 1
    for _ in range(n):
        prev, curr = curr, prev + curr
    return prev


@dataclass(frozen=True)
class ComplexityTrace:
    n: int
    fibonacci_value: int
    init_ops: int
    loop_iterations: int
    ops_per_iteration: int
    return_ops: int
    total_primitive_ops: int
    big_o_notation: str


def count_fibonacci_primitive_ops(n: int) -> ComplexityTrace:
    """Return the exact primitive operation breakdown for calculate_fibonacci(n)."""
    val = calculate_fibonacci(n)
    init_ops = 2
    ops_per_iter = 4
    ret_ops = 1
    total_ops = init_ops + (ops_per_iter * n) + ret_ops
    return ComplexityTrace(
        n=n,
        fibonacci_value=val,
        init_ops=init_ops,
        loop_iterations=n,
        ops_per_iteration=ops_per_iter,
        return_ops=ret_ops,
        total_primitive_ops=total_ops,
        big_o_notation="O(n)",
    )
