"""Question 1 - Requirement 2: Pharmacy Product Entity Class & Predefined Storage Seeding.

Defines the MedicineProduct entity class representing items in a pharmacy / medicine
retail outlet and seeds predefined records into both the LinearProbingHashTable
and a companion 1D array for performance benchmarking.
"""

from __future__ import annotations
import sys as _sys
from pathlib import Path as _Path
for _p in (_Path(__file__).resolve().parent, _Path(__file__).resolve().parents[1]):
    if str(_p) not in _sys.path:
        _sys.path.insert(0, str(_p))

from dataclasses import dataclass
from decimal import Decimal, InvalidOperation
import re
from question1_hashing.q1_req1_hash_table import LinearProbingHashTable


def validate_product_id(product_id: str) -> str:
    if not isinstance(product_id, str):
        raise ValueError("Product ID must be a string.")
    cleaned = product_id.strip().upper()
    if not re.fullmatch(r"[A-Z0-9][A-Z0-9_-]{1,15}", cleaned):
        raise ValueError("Product ID must be 2-16 alphanumeric characters (e.g., MED101).")
    return cleaned


@dataclass(frozen=True)
class MedicineProduct:
    """Entity class representing a pharmacy retail medicine product."""
    product_id: str
    name: str
    dosage_form: str
    unit_price: Decimal
    stock_quantity: int
    manufacturer: str

    def __post_init__(self) -> None:
        object.__setattr__(self, "product_id", validate_product_id(self.product_id))
        if not isinstance(self.name, str) or not self.name.strip():
            raise ValueError("Product name cannot be empty.")
        if not isinstance(self.dosage_form, str) or not self.dosage_form.strip():
            raise ValueError("Dosage form cannot be empty.")
        if not isinstance(self.manufacturer, str) or not self.manufacturer.strip():
            raise ValueError("Manufacturer cannot be empty.")
        object.__setattr__(self, "name", self.name.strip())
        object.__setattr__(self, "dosage_form", self.dosage_form.strip())
        object.__setattr__(self, "manufacturer", self.manufacturer.strip())

        if not isinstance(self.unit_price, Decimal) or self.unit_price < Decimal("0.00"):
            raise ValueError("Unit price must be a non-negative Decimal.")
        if type(self.stock_quantity) is not int or self.stock_quantity < 0:
            raise ValueError("Stock quantity must be a non-negative integer.")

    @classmethod
    def from_user_input(
        cls,
        product_id: str,
        name: str,
        dosage_form: str,
        price_str: str,
        stock_str: str,
        manufacturer: str = "Standard Pharma",
    ) -> "MedicineProduct":
        try:
            price = Decimal(price_str.strip()).quantize(Decimal("0.01"))
        except (InvalidOperation, ValueError) as exc:
            raise ValueError("Invalid price format. Enter a numeric value such as 8.50.") from exc
        try:
            stock = int(stock_str.strip())
        except ValueError as exc:
            raise ValueError("Invalid stock quantity. Enter a whole integer such as 120.") from exc
        return cls(product_id, name, dosage_form, price, stock, manufacturer)

    def format_row(self) -> str:
        return (
            f"ID: {self.product_id:<8} | Name: {self.name:<24} | "
            f"Form: {self.dosage_form:<10} | Price: RM{self.unit_price:>6.2f} | "
            f"Stock: {self.stock_quantity:>4}"
        )


def get_predefined_medicines() -> list[MedicineProduct]:
    """Return predefined pharmacy medicine records for seeding the local storage system."""
    return [
        MedicineProduct("MED101", "Paracetamol 500mg", "Tablet", Decimal("5.90"), 120, "Pharmaniaga"),
        MedicineProduct("MED102", "Amoxicillin 250mg", "Capsule", Decimal("18.50"), 85, "Duopharma"),
        MedicineProduct("MED103", "Cetirizine 10mg", "Tablet", Decimal("9.20"), 200, "Hovid"),
        MedicineProduct("MED104", "Omeprazole 20mg", "Capsule", Decimal("24.00"), 60, "Kotra Pharma"),
        MedicineProduct("MED105", "Salbutamol 100mcg", "Inhaler", Decimal("32.80"), 45, "GSK"),
        MedicineProduct("MED106", "Loratadine 10mg", "Tablet", Decimal("11.40"), 150, "Apex Pharma"),
        MedicineProduct("MED107", "Ibuprofen 400mg", "Tablet", Decimal("7.60"), 180, "Pharmaniaga"),
    ]


def seed_pharmacy_storage(
    capacity: int = 23,
) -> tuple[LinearProbingHashTable[MedicineProduct], list[MedicineProduct]]:
    """Create and populate both the Hash Table and 1D Array with predefined records."""
    hash_table: LinearProbingHashTable[MedicineProduct] = LinearProbingHashTable(capacity=capacity)
    array_storage: list[MedicineProduct] = []

    for item in get_predefined_medicines():
        hash_table.insert(item.product_id, item)
        array_storage.append(item)

    return hash_table, array_storage
