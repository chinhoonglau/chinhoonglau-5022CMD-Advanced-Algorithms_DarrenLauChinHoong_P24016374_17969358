"""Question 3 Master Runner File (q3_master.py).

Imports and links all four Question 3 requirement modules:
  1. q3_req1_fibonacci_complexity  (calculate_fibonacci, count_fibonacci_primitive_ops)
  2. q3_req2_multithreaded_fib     (run_multithreaded_experiment)
  3. q3_req3_sequential_fib        (run_sequential_experiment)
  4. q3_req4_comparison_report     (execute_full_q3_benchmark, format_q3_experiment_output)
"""

from __future__ import annotations
import sys as _sys
from pathlib import Path as _Path
for _p in (_Path(__file__).resolve().parent, _Path(__file__).resolve().parents[1]):
    if str(_p) not in _sys.path:
        _sys.path.insert(0, str(_p))

from question3_concurrency.q3_req1_fibonacci_complexity import calculate_fibonacci, count_fibonacci_primitive_ops
from question3_concurrency.q3_req2_multithreaded_fib import run_multithreaded_experiment
from question3_concurrency.q3_req3_sequential_fib import run_sequential_experiment
from question3_concurrency.q3_req4_comparison_report import execute_full_q3_benchmark, format_q3_experiment_output


def main() -> None:
    """Execute the complete Question 3 multithreaded and sequential benchmark automatically."""
    summary = execute_full_q3_benchmark()
    print(summary["formatted_output"])


if __name__ == "__main__":
    main()
