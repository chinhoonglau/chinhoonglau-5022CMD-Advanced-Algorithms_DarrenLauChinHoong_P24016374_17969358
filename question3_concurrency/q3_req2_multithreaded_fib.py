"""Question 3 - Requirement 2: Multithreaded Fibonacci Calculation (3 Threads, 10 Rounds, Nanoseconds).

Creates 3 separate threads per round (one thread each for Fibonacci(35), Fibonacci(38),
and Fibonacci(40)) and computes the elapsed time in nanoseconds using the exact
coursework formula:
    Time_Elapsed = End_Time_Of_Thread_Finished_Last - Start_Time_Of_Thread_That_Started_First
"""

from __future__ import annotations
import sys as _sys
from pathlib import Path as _Path
for _p in (_Path(__file__).resolve().parent, _Path(__file__).resolve().parents[1]):
    if str(_p) not in _sys.path:
        _sys.path.insert(0, str(_p))

from dataclasses import dataclass
from statistics import mean
import threading
from time import perf_counter_ns
from question3_concurrency.q3_req1_fibonacci_complexity import DEFAULT_ROUNDS, FIBONACCI_TARGETS, calculate_fibonacci


@dataclass(frozen=True)
class ThreadWorkerRecord:
    """Stores timing and result for a single worker thread."""
    thread_name: str
    n: int
    result: int
    start_time_ns: int
    end_time_ns: int

    @property
    def thread_duration_ns(self) -> int:
        return self.end_time_ns - self.start_time_ns


@dataclass(frozen=True)
class MultithreadedRoundResult:
    """Stores the 3 worker thread measurements and the round elapsed time T = t2 - t1."""
    round_number: int
    workers: tuple[ThreadWorkerRecord, ...]

    @property
    def t1_first_started_ns(self) -> int:
        return min(w.start_time_ns for w in self.workers)

    @property
    def t2_last_finished_ns(self) -> int:
        return max(w.end_time_ns for w in self.workers)

    @property
    def elapsed_ns(self) -> int:
        """T = t2 - t1 (End_Time_Of_Thread_Finished_Last - Start_Time_Of_Thread_That_Started_First)."""
        return self.t2_last_finished_ns - self.t1_first_started_ns


def run_single_multithreaded_round(
    round_number: int,
    inputs: tuple[int, ...] = FIBONACCI_TARGETS,
) -> MultithreadedRoundResult:
    """Execute one multithreaded round using one dedicated thread per Fibonacci input."""
    worker_records: list[ThreadWorkerRecord | None] = [None] * len(inputs)
    threads: list[threading.Thread] = []

    def worker_task(slot_index: int, target_n: int, label: str) -> None:
        t_start = perf_counter_ns()
        fib_val = calculate_fibonacci(target_n)
        t_end = perf_counter_ns()
        worker_records[slot_index] = ThreadWorkerRecord(
            thread_name=label,
            n=target_n,
            result=fib_val,
            start_time_ns=t_start,
            end_time_ns=t_end,
        )

    for idx, n_val in enumerate(inputs):
        t_name = f"Thread-{chr(65 + idx)}-Fib({n_val})"
        thread = threading.Thread(target=worker_task, args=(idx, n_val, t_name), name=t_name)
        threads.append(thread)

    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    completed = tuple(r for r in worker_records if r is not None)
    assert len(completed) == len(inputs), "All worker threads must complete."
    return MultithreadedRoundResult(round_number=round_number, workers=completed)


def run_multithreaded_experiment(
    rounds: int = DEFAULT_ROUNDS,
    inputs: tuple[int, ...] = FIBONACCI_TARGETS,
) -> tuple[list[MultithreadedRoundResult], float]:
    """Run 10 rounds of multithreaded Fibonacci calculation and compute average T in ns."""
    round_results = [
        run_single_multithreaded_round(r_num, inputs)
        for r_num in range(1, rounds + 1)
    ]
    avg_ns = float(mean(r.elapsed_ns for r in round_results))
    return round_results, avg_ns
