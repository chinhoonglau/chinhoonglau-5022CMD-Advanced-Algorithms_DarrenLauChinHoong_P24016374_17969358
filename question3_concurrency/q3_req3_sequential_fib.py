"""Question 3 - Requirement 3: Non-Multithreaded (Sequential) Fibonacci Calculation.

Computes Fibonacci(35), Fibonacci(38), and Fibonacci(40) sequentially in a single
thread over 10 rounds, measuring each round's elapsed time in nanoseconds and
computing the 10-round average.
"""

from __future__ import annotations
import sys as _sys
from pathlib import Path as _Path
for _p in (_Path(__file__).resolve().parent, _Path(__file__).resolve().parents[1]):
    if str(_p) not in _sys.path:
        _sys.path.insert(0, str(_p))

from dataclasses import dataclass
from statistics import mean
from time import perf_counter_ns
from question3_concurrency.q3_req1_fibonacci_complexity import DEFAULT_ROUNDS, FIBONACCI_TARGETS, calculate_fibonacci


@dataclass(frozen=True)
class SequentialRoundResult:
    """Stores timing and computed values for one sequential round."""
    round_number: int
    inputs: tuple[int, ...]
    results: tuple[int, ...]
    start_time_ns: int
    end_time_ns: int

    @property
    def elapsed_ns(self) -> int:
        return self.end_time_ns - self.start_time_ns


def run_single_sequential_round(
    round_number: int,
    inputs: tuple[int, ...] = FIBONACCI_TARGETS,
) -> SequentialRoundResult:
    """Execute one sequential round computing all three Fibonacci numbers on the main thread."""
    t_start = perf_counter_ns()
    computed = tuple(calculate_fibonacci(n) for n in inputs)
    t_end = perf_counter_ns()
    return SequentialRoundResult(
        round_number=round_number,
        inputs=inputs,
        results=computed,
        start_time_ns=t_start,
        end_time_ns=t_end,
    )


def run_sequential_experiment(
    rounds: int = DEFAULT_ROUNDS,
    inputs: tuple[int, ...] = FIBONACCI_TARGETS,
) -> tuple[list[SequentialRoundResult], float]:
    """Run 10 rounds of sequential Fibonacci calculation and compute average T in ns."""
    round_results = [
        run_single_sequential_round(r_num, inputs)
        for r_num in range(1, rounds + 1)
    ]
    avg_ns = float(mean(r.elapsed_ns for r in round_results))
    return round_results, avg_ns
