"""Automated unit tests for Question 3 (Concurrent Fibonacci & Timing Analysis)."""

import unittest
from question3_concurrency.q3_req1_fibonacci_complexity import (
    FIBONACCI_TARGETS,
    calculate_fibonacci,
    count_fibonacci_primitive_ops,
)
from question3_concurrency.q3_req2_multithreaded_fib import run_multithreaded_experiment
from question3_concurrency.q3_req3_sequential_fib import run_sequential_experiment
from question3_concurrency.q3_req4_comparison_report import execute_full_q3_benchmark


class TestQuestion3Concurrency(unittest.TestCase):
    def test_fibonacci_values_and_complexity_formula(self) -> None:
        self.assertEqual(calculate_fibonacci(0), 0)
        self.assertEqual(calculate_fibonacci(1), 1)
        self.assertEqual(calculate_fibonacci(10), 55)
        self.assertEqual(calculate_fibonacci(35), 9227465)
        self.assertEqual(calculate_fibonacci(38), 39088169)
        self.assertEqual(calculate_fibonacci(40), 102334155)
        trace_40 = count_fibonacci_primitive_ops(40)
        self.assertEqual(trace_40.total_primitive_ops, 4 * 40 + 3)

    def test_multithreaded_and_sequential_10_rounds(self) -> None:
        mt_rounds, mt_avg = run_multithreaded_experiment(rounds=10, inputs=FIBONACCI_TARGETS)
        seq_rounds, seq_avg = run_sequential_experiment(rounds=10, inputs=FIBONACCI_TARGETS)
        self.assertEqual(len(mt_rounds), 10)
        self.assertEqual(len(seq_rounds), 10)
        for r in mt_rounds:
            self.assertEqual(len(r.workers), 3)
            self.assertEqual(
                r.elapsed_ns,
                max(w.end_time_ns for w in r.workers) - min(w.start_time_ns for w in r.workers),
            )
            self.assertGreater(r.elapsed_ns, 0)
        self.assertGreater(mt_avg, 0)
        self.assertGreater(seq_avg, 0)

    def test_full_benchmark_formatter(self) -> None:
        summary = execute_full_q3_benchmark()
        self.assertIn("Average T (With Multithreading)", summary["formatted_output"])
        self.assertIn("Average T (Without Multithreading)", summary["formatted_output"])


if __name__ == "__main__":
    unittest.main()
