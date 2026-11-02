"""Question 1 - Requirement 1: Hash Table with Open Addressing and Linear Probing.

Implements a generic, fixed-capacity Hash Table without using Python's built-in dict
for storage. Uses a two-stage hash function (Horner's method polynomial hash code
followed by modulo compression) and resolves collisions via linear probing:
    h_i(k) = (h(k) + i) mod M,  for i = 0, 1, ..., M - 1
"""

from __future__ import annotations
import sys as _sys
from pathlib import Path as _Path
for _p in (_Path(__file__).resolve().parent, _Path(__file__).resolve().parents[1]):
    if str(_p) not in _sys.path:
        _sys.path.insert(0, str(_p))

from dataclasses import dataclass
from enum import Enum
from typing import Generic, Iterator, TypeVar

T = TypeVar("T")


class SlotState(Enum):
    """Represents the lifecycle state of a slot in an open-addressed hash table."""
    EMPTY = "EMPTY"        # Never occupied; terminates an unsuccessful search
    OCCUPIED = "OCCUPIED"  # Currently holds an active (key, value) record
    DELETED = "DELETED"    # Tombstone; preserves probe chains across deletions


@dataclass
class HashSlot(Generic[T]):
    """Single bucket/slot inside the open-addressed hash table array."""
    state: SlotState = SlotState.EMPTY
    key: str | None = None
    value: T | None = None


class HashTableFullError(OverflowError):
    """Raised when attempting to insert a new key into a completely full hash table."""


class LinearProbingHashTable(Generic[T]):
    """Generic Hash Table using Open Addressing with Linear Probing."""

    def __init__(self, capacity: int = 23) -> None:
        if type(capacity) is not int or capacity < 1:
            raise ValueError("Table capacity must be a positive integer.")
        self.capacity: int = capacity
        self._slots: list[HashSlot[T]] = [HashSlot() for _ in range(capacity)]
        self._size: int = 0

    def __len__(self) -> int:
        return self._size

    @property
    def load_factor(self) -> float:
        return self._size / self.capacity

    @staticmethod
    def _validate_key(key: str) -> str:
        if not isinstance(key, str) or not key.strip():
            raise ValueError("Key must be a non-empty string.")
        return key.strip().upper()

    @staticmethod
    def compute_hash_code(key: str) -> int:
        """Stage 1: Compute polynomial string hash code via Horner's rule (base 31)."""
        clean_key = LinearProbingHashTable._validate_key(key)
        hash_val = 0
        for ch in clean_key:
            hash_val = (hash_val * 31) + ord(ch)
        return hash_val

    def compress_index(self, key: str) -> int:
        """Stage 2: Compress integer hash code into valid slot range [0, capacity - 1]."""
        return self.compute_hash_code(key) % self.capacity

    def insert(self, key: str, value: T) -> tuple[int, int]:
        """Insert (key, value) using linear probing.

        Returns (slot_index, probe_count). Raises ValueError on duplicate key
        or HashTableFullError when no empty/tombstone slot is available.
        """
        clean_key = self._validate_key(key)
        home_idx = self.compress_index(clean_key)
        first_tombstone: int | None = None

        for step in range(self.capacity):
            idx = (home_idx + step) % self.capacity
            slot = self._slots[idx]

            if slot.state is SlotState.EMPTY:
                target_idx = first_tombstone if first_tombstone is not None else idx
                self._slots[target_idx] = HashSlot(SlotState.OCCUPIED, clean_key, value)
                self._size += 1
                return target_idx, step + 1

            if slot.state is SlotState.DELETED:
                if first_tombstone is None:
                    first_tombstone = idx
            elif slot.key == clean_key:
                raise ValueError(f"Duplicate key '{clean_key}' already exists at slot [{idx}].")

        if first_tombstone is not None:
            self._slots[first_tombstone] = HashSlot(SlotState.OCCUPIED, clean_key, value)
            self._size += 1
            return first_tombstone, self.capacity

        raise HashTableFullError(f"Hash table is full (capacity={self.capacity}).")

    def search_with_trace(self, key: str) -> tuple[T, int, list[int]]:
        """Search for key and return (value, found_slot, visited_slots_trace)."""
        clean_key = self._validate_key(key)
        home_idx = self.compress_index(clean_key)
        visited: list[int] = []

        for step in range(self.capacity):
            idx = (home_idx + step) % self.capacity
            visited.append(idx)
            slot = self._slots[idx]

            if slot.state is SlotState.EMPTY:
                break
            if slot.state is SlotState.OCCUPIED and slot.key == clean_key:
                assert slot.value is not None
                return slot.value, idx, visited

        raise KeyError(f"Key '{clean_key}' not found (probed slots: {visited}).")

    def search(self, key: str) -> T:
        """Return value associated with key or raise KeyError."""
        value, _, _ = self.search_with_trace(key)
        return value

    def update(self, key: str, new_value: T) -> int:
        """Update the value of an existing key in place and return its slot index."""
        clean_key = self._validate_key(key)
        _, slot_idx, _ = self.search_with_trace(clean_key)
        self._slots[slot_idx].value = new_value
        return slot_idx


    def replace(self, old_key: str, new_key: str, new_value: T) -> int:
        """Update an existing record, rehashing if new_key differs from old_key."""
        clean_old = self._validate_key(old_key)
        clean_new = self._validate_key(new_key)
        if clean_old == clean_new:
            return self.update(clean_old, new_value)
        # Ensure new_key does not already exist before mutating
        try:
            _, dup_slot, _ = self.search_with_trace(clean_new)
            raise ValueError(f"Duplicate key '{clean_new}' already exists at slot [{dup_slot}].")
        except KeyError:
            pass
        old_val, old_slot = self.delete(clean_old)
        try:
            new_slot, _ = self.insert(clean_new, new_value)
            return new_slot
        except Exception:
            self._slots[old_slot] = HashSlot(SlotState.OCCUPIED, clean_old, old_val)
            self._size += 1
            raise

    def delete(self, key: str) -> tuple[T, int]:
        """Mark the slot holding key as DELETED (tombstone) and return (value, slot_index)."""
        clean_key = self._validate_key(key)
        value, slot_idx, _ = self.search_with_trace(clean_key)
        self._slots[slot_idx] = HashSlot(SlotState.DELETED, None, None)
        self._size -= 1
        return value, slot_idx

    def items(self) -> Iterator[tuple[int, str, T]]:
        """Yield (slot_index, key, value) for all currently occupied slots."""
        for idx, slot in enumerate(self._slots):
            if slot.state is SlotState.OCCUPIED and slot.key is not None and slot.value is not None:
                yield idx, slot.key, slot.value

    def snapshot_slots(self) -> list[tuple[int, str, str | None, T | None]]:
        """Return a complete view of all table slots for inspection and reporting."""
        return [(idx, s.state.value, s.key, s.value) for idx, s in enumerate(self._slots)]
