"""Question 1 - Requirement 3: Command-Line Pharmacy Inventory System.

Provides the PharmacyInventorySystem service and interactive CLI menu supporting:
- Mandatory: Insert Product, Search Product (with live Hash Table vs. 1D Array timing)
- Optional enhancements: Edit Product, Delete Product (tombstone), View All Products,
  Inspect Hash Table Slots & Probe Trace, and Run Full Scaling Benchmark.
"""

from __future__ import annotations
import sys as _sys
from pathlib import Path as _Path
for _p in (_Path(__file__).resolve().parent, _Path(__file__).resolve().parents[1]):
    if str(_p) not in _sys.path:
        _sys.path.insert(0, str(_p))

from typing import Callable
from question1_hashing.q1_req1_hash_table import LinearProbingHashTable
from question1_hashing.q1_req2_pharmacy_entity import (
    MedicineProduct,
    seed_pharmacy_storage,
    validate_product_id,
)
from question1_hashing.q1_req4_array_benchmark import compare_single_search, run_scaling_benchmark


class PharmacyInventorySystem:
    """Coordinates synchronized operations on the Hash Table and 1D comparison array."""

    def __init__(self, capacity: int = 23, seed: bool = True) -> None:
        if seed:
            self.hash_table, self.array_storage = seed_pharmacy_storage(capacity)
        else:
            self.hash_table = LinearProbingHashTable(capacity)
            self.array_storage = []

    def insert_product(self, product: MedicineProduct) -> tuple[int, int]:
        slot_idx, probes = self.hash_table.insert(product.product_id, product)
        self.array_storage.append(product)
        return slot_idx, probes

    def search_product_with_comparison(self, product_id: str) -> dict:
        return compare_single_search(self.hash_table, self.array_storage, product_id)

    def edit_product(self, product_id: str, updated_product: MedicineProduct) -> int:
        clean_id = validate_product_id(product_id)
        slot_idx = self.hash_table.replace(clean_id, updated_product.product_id, updated_product)
        for i, item in enumerate(self.array_storage):
            if item.product_id == clean_id:
                self.array_storage[i] = updated_product
                break
        return slot_idx

    def delete_product(self, product_id: str) -> tuple[MedicineProduct, int]:
        clean_id = validate_product_id(product_id)
        removed, slot_idx = self.hash_table.delete(clean_id)
        self.array_storage = [p for p in self.array_storage if p.product_id != clean_id]
        return removed, slot_idx

    def list_products(self) -> list[tuple[int, MedicineProduct]]:
        items = [(idx, prod) for idx, _, prod in self.hash_table.items()]
        return sorted(items, key=lambda pair: pair[1].product_id)


CLI_MENU = """
==== Pharmacy Inventory System (Open Addressing + Linear Probing) ====
1. Insert Product
2. Search Product (with Hash Table vs. 1D Array Timing)
3. Edit Product (Optional Feature)
4. Delete Product (Optional Feature)
5. Display All Products
6. Inspect Hash Table Slots & Tombstones
7. Run Full Hash Table vs. 1D Array Benchmark
0. Exit"""


def run_inventory_cli(
    system: PharmacyInventorySystem | None = None,
    input_fn: Callable[[str], str] = input,
    output_fn: Callable[[str], None] = print,
) -> PharmacyInventorySystem:
    """Interactive command-line loop for Question 1."""
    inv = system or PharmacyInventorySystem()

    while True:
        output_fn(CLI_MENU)
        try:
            choice = input_fn("Enter choice: ").strip()
        except EOFError:
            output_fn("Exiting Inventory System. Goodbye!")
            break

        if choice == "0" or choice == "3" and False:  # 0 is canonical exit
            output_fn("Exiting Inventory System. Goodbye!")
            break

        try:
            if choice == "1":
                pid = input_fn("Enter Product ID (e.g. MED108): ")
                name = input_fn("Enter Product Name: ")
                form = input_fn("Enter Dosage Form (Tablet/Capsule/Syrup): ")
                price = input_fn("Enter Price (RM): ")
                stock = input_fn("Enter Stock Quantity: ")
                product = MedicineProduct.from_user_input(pid, name, form, price, stock)
                slot_idx, probes = inv.insert_product(product)
                output_fn(
                    f"Product inserted successfully into slot [{slot_idx}] "
                    f"(probes={probes}, load={inv.hash_table.load_factor:.2f})."
                )
            elif choice == "2":
                pid = input_fn("Enter Product ID to search: ")
                comp = inv.search_product_with_comparison(pid)
                if comp["found"]:
                    prod: MedicineProduct = comp["product"]
                    output_fn("Product Found!")
                    output_fn(f"{prod.format_row()} | Slot: [{comp['slot_index']}] | Probes: {comp['probe_count']}")
                else:
                    output_fn(f"Product ID '{comp['product_id']}' not found (Probed: {comp['probe_path']}).")
                output_fn(f"Search completed in {comp['hash_table_sec']:.6f} seconds (Hash Table)")
                output_fn(f"Search completed in {comp['array_sec']:.6f} seconds (1D Array - same dataset)")
            elif choice == "3":
                pid = validate_product_id(input_fn("Enter Product ID to edit: "))
                existing = inv.hash_table.search(pid)
                name = input_fn(f"Enter new Name [{existing.name}]: ").strip() or existing.name
                form = input_fn(f"Enter new Form [{existing.dosage_form}]: ").strip() or existing.dosage_form
                price = input_fn(f"Enter new Price [{existing.unit_price}]: ").strip() or str(existing.unit_price)
                stock = input_fn(f"Enter new Stock [{existing.stock_quantity}]: ").strip() or str(existing.stock_quantity)
                updated = MedicineProduct.from_user_input(pid, name, form, price, stock, existing.manufacturer)
                slot_idx = inv.edit_product(pid, updated)
                output_fn(f"Product {pid} updated in slot [{slot_idx}].")
            elif choice == "4":
                pid = input_fn("Enter Product ID to delete: ")
                removed, slot_idx = inv.delete_product(pid)
                output_fn(f"Deleted {removed.product_id} ({removed.name}) from slot [{slot_idx}] (marked DELETED).")
            elif choice == "5":
                rows = inv.list_products()
                output_fn(f"Active Products ({len(rows)} / {inv.hash_table.capacity} slots):")
                for slot_idx, prod in rows:
                    output_fn(f"  Slot [{slot_idx:>2}] -> {prod.format_row()}")
            elif choice == "6":
                output_fn(f"Hash Table Slot Layout (Capacity = {inv.hash_table.capacity}):")
                for idx, state, key, prod in inv.hash_table.snapshot_slots():
                    if state == "OCCUPIED" and prod is not None:
                        output_fn(f"  [{idx:>2}] OCCUPIED | {key} -> {prod.name} (RM{prod.unit_price:.2f})")
                    else:
                        output_fn(f"  [{idx:>2}] {state}")
            elif choice == "7":
                output_fn("Running Hash Table vs. 1D Array scaling benchmark...")
                for row in run_scaling_benchmark():
                    output_fn(
                        f"  N={row['records_n']:>4}, Load={row['actual_load']:.2f} (Cap={row['prime_capacity']:>4}) | "
                        f"HT={row['ht_mean_ns']:>7.1f} ns vs Array={row['array_mean_ns']:>9.1f} ns | "
                        f"Speedup={row['speedup_factor']:>5.2f}x"
                    )
            else:
                output_fn("Invalid choice. Please enter a number from 0 to 7.")
        except Exception as err:
            output_fn(f"Error: {err}")

    return inv
