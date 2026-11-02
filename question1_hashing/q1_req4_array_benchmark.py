"""Question 1 - Requirement 4: Search Performance Comparison (Hash Table vs. 1D Array).

Compares lookup execution times between LinearProbingHashTable and a 1D Python list
storing the exact same MedicineProduct records. Includes single-query CLI timing
and multi-scale batch benchmarking across table sizes and load factors.
"""

from __future__ import annotations
import sys as _sys
from pathlib import Path as _Path
for _p in (_Path(__file__).resolve().parent, _Path(__file__).resolve().parents[1]):
    if str(_p) not in _sys.path:
        _sys.path.insert(0, str(_p))

from decimal import Decimal
from time import perf_counter_ns
from typing import Any
from question1_hashing.q1_req1_hash_table import LinearProbingHashTable
from question1_hashing.q1_req2_pharmacy_entity import MedicineProduct, validate_product_id


def array_linear_search(records: list[MedicineProduct], product_id: str) -> MedicineProduct | None:
    """Sequential O(n) linear scan through a 1D array of MedicineProduct objects."""
    target = validate_product_id(product_id)
    for item in records:
        if item.product_id == target:
            return item
    return None


def compare_single_search(
    hash_table: LinearProbingHashTable[MedicineProduct],
    array_records: list[MedicineProduct],
    product_id: str,
    iterations: int = 500,
) -> dict[str, Any]:
    """Compare Hash Table vs. 1D Array search for a single key over repeated trials."""
    clean_id = validate_product_id(product_id)

    # 1. Measure Hash Table lookup
    found_ht: MedicineProduct | None = None
    slot_idx: int = -1
    probe_path: list[int] = []
    ht_start = perf_counter_ns()
    for _ in range(iterations):
        try:
            found_ht, slot_idx, probe_path = hash_table.search_with_trace(clean_id)
        except KeyError:
            found_ht = None
    ht_elapsed_ns = (perf_counter_ns() - ht_start) / iterations

    # 2. Measure 1D Array sequential lookup
    found_arr: MedicineProduct | None = None
    arr_start = perf_counter_ns()
    for _ in range(iterations):
        found_arr = array_linear_search(array_records, clean_id)
    arr_elapsed_ns = (perf_counter_ns() - arr_start) / iterations

    return {
        "product_id": clean_id,
        "found": found_ht is not None,
        "product": found_ht,
        "slot_index": slot_idx,
        "probe_path": probe_path,
        "probe_count": len(probe_path),
        "hash_table_ns": ht_elapsed_ns,
        "hash_table_sec": ht_elapsed_ns / 1e9,
        "array_ns": arr_elapsed_ns,
        "array_sec": arr_elapsed_ns / 1e9,
        "speedup_ratio": (arr_elapsed_ns / ht_elapsed_ns) if ht_elapsed_ns > 0 else 1.0,
        "same_result": found_ht == found_arr,
    }


def _next_prime(n: int) -> int:
    candidate = max(2, n)
    while True:
        is_p = True
        d = 2
        while d * d <= candidate:
            if candidate % d == 0:
                is_p = False
                break
            d += 1
        if is_p:
            return candidate
        candidate += 1


def run_scaling_benchmark(
    dataset_sizes: tuple[int, ...] = (100, 500, 2000),
    load_factors: tuple[float, ...] = (0.50, 0.75, 0.90),
    batch_repeats: int = 200,
) -> list[dict[str, Any]]:
    """Run controlled benchmark across dataset sizes and load factors."""
    results: list[dict[str, Any]] = []

    for n in dataset_sizes:
        records = [
            MedicineProduct(
                f"MED{i + 1000:05d}",
                f"Formula-{i + 1}",
                "Tablet",
                Decimal("12.50"),
                100,
                "LabCorp",
            )
            for i in range(n)
        ]
        # Query mix: 80% existing keys across start/middle/end + 20% missing keys
        step = max(1, n // 40)
        hit_keys = [records[i].product_id for i in range(0, n, step)][:40]
        miss_keys = [f"MISS{i:05d}" for i in range(10)]
        queries = hit_keys + miss_keys

        # Measure 1D array search across query set
        arr_start = perf_counter_ns()
        arr_hits = 0
        for _ in range(batch_repeats):
            for q in queries:
                if array_linear_search(records, q) is not None:
                    arr_hits += 1
        arr_total_ns = perf_counter_ns() - arr_start
        arr_mean_ns = arr_total_ns / (batch_repeats * len(queries))

        for alpha in load_factors:
            capacity = _next_prime(int(n / alpha) + 1)
            ht: LinearProbingHashTable[MedicineProduct] = LinearProbingHashTable(capacity)
            total_insert_probes = 0
            for item in records:
                _, probes = ht.insert(item.product_id, item)
                total_insert_probes += probes

            ht_start = perf_counter_ns()
            ht_hits = 0
            for _ in range(batch_repeats):
                for q in queries:
                    try:
                        ht.search(q)
                        ht_hits += 1
                    except KeyError:
                        pass
            ht_total_ns = perf_counter_ns() - ht_start
            ht_mean_ns = ht_total_ns / (batch_repeats * len(queries))

            assert arr_hits == ht_hits, "Hit count mismatch between Hash Table and 1D Array!"
            results.append({
                "records_n": n,
                "target_load": alpha,
                "prime_capacity": capacity,
                "actual_load": round(len(ht) / capacity, 4),
                "avg_insert_probes": round(total_insert_probes / n, 2),
                "ht_mean_ns": round(ht_mean_ns, 1),
                "ht_mean_sec": ht_mean_ns / 1e9,
                "array_mean_ns": round(arr_mean_ns, 1),
                "array_mean_sec": arr_mean_ns / 1e9,
                "speedup_factor": round(arr_mean_ns / ht_mean_ns, 2) if ht_mean_ns > 0 else 1.0,
            })

    return results


def run_detailed_query_group_benchmark(
    dataset_sizes: tuple[int, ...] = (100, 500, 2000),
    load_factors: tuple[float, ...] = (0.50, 0.75, 0.90),
    batch_repeats: int = 80,
) -> list[dict[str, Any]]:
    """Benchmark successful (hit), unsuccessful (miss), and mixed query workloads (27 configurations)."""
    rows: list[dict[str, Any]] = []
    for n in dataset_sizes:
        records = [
            MedicineProduct(
                f"MED{i + 1000:05d}",
                f"Formula-{i + 1}",
                "Tablet",
                Decimal("12.50"),
                100,
                "LabCorp",
            )
            for i in range(n)
        ]
        step = max(1, n // 50)
        hits = [records[i].product_id for i in range(0, n, step)][:50]
        misses = [f"ABSENT{i:05d}" for i in range(50)]
        groups = {
            "hit (existing IDs)": hits,
            "miss (absent IDs)": misses,
            "mixed (50% hit / 50% miss)": hits[:25] + misses[:25],
        }
        for alpha in load_factors:
            capacity = _next_prime(int(n / alpha) + 1)
            ht: LinearProbingHashTable[MedicineProduct] = LinearProbingHashTable(capacity)
            for item in records:
                ht.insert(item.product_id, item)

            for group_name, queries in groups.items():
                # Measure probes
                total_probes = 0
                for q in queries:
                    try:
                        _, _, path = ht.search_with_trace(q)
                        total_probes += len(path)
                    except KeyError as exc:
                        # Count visited slots from trace
                        msg = str(exc)
                        total_probes += msg.count(",") + 1

                ht_start = perf_counter_ns()
                for _ in range(batch_repeats):
                    for q in queries:
                        try:
                            ht.search(q)
                        except KeyError:
                            pass
                ht_ns = (perf_counter_ns() - ht_start) / (batch_repeats * len(queries))

                arr_start = perf_counter_ns()
                for _ in range(batch_repeats):
                    for q in queries:
                        array_linear_search(records, q)
                arr_ns = (perf_counter_ns() - arr_start) / (batch_repeats * len(queries))

                rows.append({
                    "records_n": n,
                    "target_load": alpha,
                    "prime_capacity": capacity,
                    "actual_load": round(len(ht) / capacity, 5),
                    "query_group": group_name,
                    "mean_probes": round(total_probes / len(queries), 2),
                    "ht_mean_ns": round(ht_ns, 1),
                    "array_mean_ns": round(arr_ns, 1),
                    "speedup_factor": round(arr_ns / ht_ns, 2) if ht_ns > 0 else 1.0,
                })
    return rows


def run_capacity_clustering_diagnostic() -> list[dict[str, Any]]:
    """Compare composite capacity (1000) vs prime capacity (1009) with 500 identical records."""
    records = [
        MedicineProduct(f"SKU{i * 15 + 100:05d}", f"Med-{i}", "Tablet", Decimal("9.50"), 50, "Pharma")
        for i in range(500)
    ]
    queries = [r.product_id for r in records[:75]] + [f"NONE{i:05d}" for i in range(25)]
    diag: list[dict[str, Any]] = []
    for cap, label in ((1000, "Composite (1000)"), (1009, "Prime (1009)")):
        ht: LinearProbingHashTable[MedicineProduct] = LinearProbingHashTable(cap)
        seen_homes: set[int] = set()
        home_collisions = 0
        insert_probes = 0
        for r in records:
            h = ht.compress_index(r.product_id)
            if h in seen_homes:
                home_collisions += 1
            else:
                seen_homes.add(h)
            _, p_cnt = ht.insert(r.product_id, r)
            insert_probes += p_cnt

        query_probes = 0
        for q in queries:
            try:
                _, _, trace = ht.search_with_trace(q)
                query_probes += len(trace)
            except KeyError as exc:
                query_probes += str(exc).count(",") + 1

        diag.append({
            "capacity_label": label,
            "capacity": cap,
            "records": len(records),
            "load_factor": round(len(records) / cap, 5),
            "home_collisions": home_collisions,
            "mean_insert_probes": round(insert_probes / len(records), 2),
            "mean_query_probes": round(query_probes / len(queries), 2),
        })
    return diag
