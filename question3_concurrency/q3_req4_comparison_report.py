"""Question 3 - Requirement 4: Comparative Output Formatter & Concurrency Analysis.

Formats the 10-round multithreaded and non-multithreaded Fibonacci experiments,
computes the nanosecond averages and relative difference, and includes a supplementary
I/O-bound benchmark illustrating when Python multithreading improves throughput.
"""

from __future__ import annotations
import sys as _sys
from pathlib import Path as _Path
for _p in (_Path(__file__).resolve().parent, _Path(__file__).resolve().parents[1]):
    if str(_p) not in _sys.path:
        _sys.path.insert(0, str(_p))

import threading
import time
from time import perf_counter_ns
from typing import Any
from question3_concurrency.q3_req1_fibonacci_complexity import FIBONACCI_TARGETS, count_fibonacci_primitive_ops
from question3_concurrency.q3_req2_multithreaded_fib import MultithreadedRoundResult, run_multithreaded_experiment
from question3_concurrency.q3_req3_sequential_fib import SequentialRoundResult, run_sequential_experiment


def run_io_bound_comparison(task_count: int = 3, simulated_io_wait_sec: float = 0.015) -> dict[str, Any]:
    """Demonstrate a situation where multithreading significantly improves performance (I/O wait)."""
    seq_start = perf_counter_ns()
    for _ in range(task_count):
        time.sleep(simulated_io_wait_sec)
    seq_ns = perf_counter_ns() - seq_start

    mt_start = perf_counter_ns()
    threads = [
        threading.Thread(target=time.sleep, args=(simulated_io_wait_sec,))
        for _ in range(task_count)
    ]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    mt_ns = perf_counter_ns() - mt_start

    return {
        "task_count": task_count,
        "io_wait_ms": simulated_io_wait_sec * 1000,
        "sequential_io_ns": seq_ns,
        "multithreaded_io_ns": mt_ns,
        "io_speedup_factor": round(seq_ns / mt_ns, 2) if mt_ns > 0 else 1.0,
    }


def format_q3_experiment_output(
    mt_rounds: list[MultithreadedRoundResult],
    mt_avg_ns: float,
    seq_rounds: list[SequentialRoundResult],
    seq_avg_ns: float,
    io_demo: dict[str, Any] | None = None,
) -> str:
    """Format the complete Question 3 console report matching the assignment brief."""
    lines: list[str] = []
    lines.append("=== Fibonacci Computation (With Multithreading - 3 Threads) ===")
    for r in mt_rounds:
        fib_str = ", ".join(f"Fib({w.n})={w.result}" for w in r.workers)
        lines.append(f"Round {r.round_number:>2}: {fib_str} | T = {r.elapsed_ns:>10,d} ns")
        for w in r.workers:
            s_off = w.start_time_ns - r.t1_first_started_ns
            e_off = w.end_time_ns - r.t1_first_started_ns
            lines.append(
                f"   -> {w.thread_name}: start=+{s_off:,d} ns, end=+{e_off:,d} ns, duration={w.thread_duration_ns:,d} ns")
    lines.append(f"Average T (With Multithreading)    : {round(mt_avg_ns):,d} ns")
    lines.append("")
    lines.append("=== Fibonacci Computation (Without Multithreading - Sequential) ===")
    for r in seq_rounds:
        fib_str = ", ".join(f"Fib({n})={val}" for n, val in zip(r.inputs, r.results))
        lines.append(f"Round {r.round_number:>2}: {fib_str} | T = {r.elapsed_ns:>10,d} ns")
    lines.append(f"Average T (Without Multithreading) : {round(seq_avg_ns):,d} ns")
    lines.append("")

    if mt_avg_ns < seq_avg_ns:
        pct = ((seq_avg_ns - mt_avg_ns) / seq_avg_ns) * 100.0
        lines.append(
            f"Observation: Multithreading reduced the average completion time by {pct:.2f}%."
        )
    else:
        ratio = mt_avg_ns / seq_avg_ns if seq_avg_ns > 0 else 1.0
        overhead_ns = mt_avg_ns - seq_avg_ns
        lines.append(
            f"Observation: For this CPU-bound O(n) iterative task, multithreading took "
            f"{overhead_ns:,.0f} ns longer on average ({ratio:.2f}x of sequential time) "
            f"because CPython's Global Interpreter Lock (GIL) serializes bytecode execution "
            f"and OS thread creation/context-switching overhead dominates sub-millisecond work."
        )

    lines.append("")
    lines.append("=== Complexity & Primitive Operation Summary ===")
    for n_val in FIBONACCI_TARGETS:
        trace = count_fibonacci_primitive_ops(n_val)
        lines.append(
            f"n={trace.n}: Fib({trace.n})={trace.fibonacci_value} | "
            f"Primitive Ops T({trace.n}) = 4({trace.n}) + 3 = {trace.total_primitive_ops} -> {trace.big_o_notation}"
        )

    if io_demo is not None:
        lines.append("")
        lines.append("=== Supplementary Example: When Multithreading Improves Performance (I/O-Bound) ===")
        lines.append(
            f"{io_demo['task_count']} concurrent {io_demo['io_wait_ms']:.0f}ms I/O waits: "
            f"Sequential = {io_demo['sequential_io_ns']:,d} ns vs "
            f"Multithreaded = {io_demo['multithreaded_io_ns']:,d} ns "
            f"(Speedup = {io_demo['io_speedup_factor']:.2f}x)"
        )

    return "\n".join(lines)


def execute_full_q3_benchmark() -> dict[str, Any]:
    """Run both required 10-round experiments plus the I/O-bound comparison."""
    mt_rounds, mt_avg = run_multithreaded_experiment()
    seq_rounds, seq_avg = run_sequential_experiment()
    io_demo = run_io_bound_comparison()
    formatted = format_q3_experiment_output(mt_rounds, mt_avg, seq_rounds, seq_avg, io_demo)
    return {
        "mt_rounds": mt_rounds,
        "mt_avg_ns": mt_avg,
        "seq_rounds": seq_rounds,
        "seq_avg_ns": seq_avg,
        "io_demo": io_demo,
        "formatted_output": formatted,
    }
