# 5022CMD Advanced Algorithms Portfolio (PyCharm Modular Project)

This repository contains the complete, modular Python implementation, automated test suite, executed benchmark evidence, PyCharm code/console captures, and portfolio PDF report for **5022CMD Advanced Algorithms**.

## Project Directory Layout (4 Requirement Modules + 1 Master Runner per Question)

```text
5022CMD_Advanced_Algorithms_Portfolio/
├── README.md
├── q1_master.py                              # Top-level Master Launcher for Question 1
├── q2_master.py                              # Top-level Master Launcher for Question 2
├── q3_master.py                              # Top-level Master Launcher for Question 3
├── question1_hashing/
│   ├── __init__.py
│   ├── __main__.py
│   ├── q1_req1_hash_table.py                 # Req 1: Open Addressing + Linear Probing Hash Table
│   ├── q1_req2_pharmacy_entity.py            # Req 2: MedicineProduct Entity & Predefined Seeding
│   ├── q1_req3_inventory_cli.py              # Req 3: Command-Line Inventory System (Insert/Search/Edit/Delete)
│   ├── q1_req4_array_benchmark.py            # Req 4: Hash Table vs. 1D Array Search Benchmark
│   └── q1_master.py                          # Question 1 Master Runner linking Requirements 1-4
├── question2_graph/
│   ├── __init__.py
│   ├── __main__.py
│   ├── q2_req1_directed_graph.py             # Req 1: Generic Unweighted DirectedGraph (addVertex, addEdge, listIncomingAdjacentVertex)
│   ├── q2_req2_course_entity.py              # Req 2: University Course Entity & 8 Predefined Courses (5-10 limit)
│   ├── q2_req3_prerequisite_graph.py         # Req 3: Course-Prerequisite Network & All 4 Optional Advanced Features
│   ├── q2_req4_menu_interface.py             # Req 4: Menu-Driven CLI (Mandatory Features 1-4 + Advanced Submenu 1-4)
│   └── q2_master.py                          # Question 2 Master Runner linking Requirements 1-4
├── question3_concurrency/
│   ├── __init__.py
│   ├── __main__.py
│   ├── q3_req1_fibonacci_complexity.py       # Req 1-2: Iterative Fibonacci & O(n) Primitive Operation Counter
│   ├── q3_req2_multithreaded_fib.py          # Req 3: 3-Thread Execution across 10 Rounds (T = t2 - t1 in ns)
│   ├── q3_req3_sequential_fib.py             # Req 4: Non-Multithreaded Execution across 10 Rounds (in ns)
│   ├── q3_req4_comparison_report.py          # Req 5: Comparative Timing Formatter & I/O-Bound Speedup Demo
│   └── q3_master.py                          # Question 3 Master Runner linking Requirements 1-4
├── tests/
│   ├── test_q1.py
│   ├── test_q2.py
│   └── test_q3.py
├── scripts/
│   └── generate_evidence.py                  # Runs all 20 test cases, benchmarks, charts, and screenshots
├── evidence/                                 # Saved JSON/TXT outputs from real executions
├── docs/
│   ├── test_case_matrix.md                   # Complete 8-column test-case matrix
│   ├── pycharm_screenshot_and_execution_guide.md
│   ├── viva_preparation_guide.md
│   └── personal_reflection_template.md
└── output/
    ├── pdf/5022CMD_Portfolio_Report.pdf      # Complete compiled PDF report
    └── screenshots/                          # PyCharm IDE code & console output captures + charts
```

## Quick Start in PyCharm or Terminal

```bash
# Run Master Files for Each Question
python3 q1_master.py
python3 q2_master.py
python3 q3_master.py

# Run Unit Tests
python3 -m unittest discover -s tests -v

# Regenerate All Executed Evidence, Screenshots, and Charts
python3 scripts/generate_evidence.py
```
