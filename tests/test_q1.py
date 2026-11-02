"""Automated unit tests for Question 1 (Hashing & Pharmacy Inventory System)."""

from decimal import Decimal
import unittest
from question1_hashing.q1_req1_hash_table import HashTableFullError, LinearProbingHashTable, SlotState
from question1_hashing.q1_req2_pharmacy_entity import MedicineProduct, seed_pharmacy_storage
from question1_hashing.q1_req3_inventory_cli import PharmacyInventorySystem, run_inventory_cli
from question1_hashing.q1_req4_array_benchmark import array_linear_search, compare_single_search


class TestQuestion1Hashing(unittest.TestCase):
    def test_linear_probing_and_tombstone_reuse(self) -> None:
        ht: LinearProbingHashTable[str] = LinearProbingHashTable(capacity=5)
        idx1, _ = ht.insert("KEY1", "Alpha")
        idx2, _ = ht.insert("KEY6", "Beta")
        self.assertEqual(ht.search("KEY1"), "Alpha")
        self.assertEqual(ht.search("KEY6"), "Beta")
        ht.delete("KEY1")
        self.assertEqual(ht.search("KEY6"), "Beta")
        idx3, _ = ht.insert("KEY11", "Gamma")
        self.assertIn(idx3, range(5))
        self.assertEqual(ht.search("KEY11"), "Gamma")

    def test_full_table_and_duplicate_rejection(self) -> None:
        ht: LinearProbingHashTable[int] = LinearProbingHashTable(capacity=3)
        ht.insert("A1", 10)
        with self.assertRaises(ValueError):
            ht.insert("A1", 20)
        ht.insert("B2", 30)
        ht.insert("C3", 40)
        with self.assertRaises(HashTableFullError):
            ht.insert("D4", 50)

    def test_pharmacy_inventory_crud_and_cli(self) -> None:
        inv = PharmacyInventorySystem(capacity=23, seed=True)
        self.assertEqual(len(inv.hash_table), 7)
        new_med = MedicineProduct("MED199", "Vitamin C 1000mg", "Tablet", Decimal("15.00"), 90, "Blackmores")
        slot_idx, _ = inv.insert_product(new_med)
        self.assertTrue(0 <= slot_idx < 23)
        comp = inv.search_product_with_comparison("MED199")
        self.assertTrue(comp["found"])
        self.assertTrue(comp["same_result"])

        # Edit and delete
        updated = MedicineProduct("MED199", "Vitamin C 1000mg Forte", "Tablet", Decimal("16.50"), 110, "Blackmores")
        inv.edit_product("MED199", updated)
        self.assertEqual(inv.hash_table.search("MED199").unit_price, Decimal("16.50"))
        inv.delete_product("MED199")
        with self.assertRaises(KeyError):
            inv.hash_table.search("MED199")

        # Simulated CLI session
        inputs = iter(["1", "MED205", "Aspirin 100mg", "Tablet", "6.80", "75", "2", "MED205", "0"])
        outputs: list[str] = []
        run_inventory_cli(inv, input_fn=lambda _: next(inputs), output_fn=outputs.append)
        joined = "\n".join(outputs)
        self.assertIn("Product inserted successfully", joined)
        self.assertIn("Product Found!", joined)


if __name__ == "__main__":
    unittest.main()
