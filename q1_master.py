"""Question 1 Master Runner File (q1_master.py).

Imports and links all four Question 1 requirement modules:
  1. q1_req1_hash_table       (LinearProbingHashTable, SlotState, HashSlot)
  2. q1_req2_pharmacy_entity  (MedicineProduct, seed_pharmacy_storage)
  3. q1_req3_inventory_cli    (PharmacyInventorySystem, run_inventory_cli)
  4. q1_req4_array_benchmark  (compare_single_search, run_scaling_benchmark)
"""

from __future__ import annotations
import sys as _sys
from pathlib import Path as _Path
for _p in (_Path(__file__).resolve().parent, _Path(__file__).resolve().parents[1]):
    if str(_p) not in _sys.path:
        _sys.path.insert(0, str(_p))

from question1_hashing.q1_req1_hash_table import HashSlot, LinearProbingHashTable, SlotState
from question1_hashing.q1_req2_pharmacy_entity import MedicineProduct, get_predefined_medicines, seed_pharmacy_storage
from question1_hashing.q1_req3_inventory_cli import PharmacyInventorySystem, run_inventory_cli
from question1_hashing.q1_req4_array_benchmark import array_linear_search, compare_single_search, run_scaling_benchmark


def main() -> None:
    """Initialize the Pharmacy Inventory System and launch the interactive CLI."""
    inventory_system = PharmacyInventorySystem(capacity=23, seed=True)
    run_inventory_cli(inventory_system)


if __name__ == "__main__":
    main()
