"""Question 2 - Requirement 1: Generic Unweighted Directed Graph Data Structure.

Implements a reusable, domain-agnostic unweighted directed graph G = (V, E)
using adjacency lists. Strictly decoupled from any Course entity logic so that
it can store vertices of any hashable type T.

Required methods implemented:
  - addVertex(vertex)
  - addEdge(source, destination)
  - listIncomingAdjacentVertex(vertex)
Additional helper methods for complete graph operations:
  - listOutgoingAdjacentVertex(vertex)
  - removeEdge(source, destination)
  - hasPath(source, destination)
"""

from __future__ import annotations
import sys as _sys
from pathlib import Path as _Path
for _p in (_Path(__file__).resolve().parent, _Path(__file__).resolve().parents[1]):
    if str(_p) not in _sys.path:
        _sys.path.insert(0, str(_p))

from collections import deque
from typing import Generic, Hashable, TypeVar

V = TypeVar("V", bound=Hashable)


class DirectedGraph(Generic[V]):
    """Generic unweighted directed graph using deterministic adjacency lists."""

    def __init__(self) -> None:
        self._adjacency: dict[V, list[V]] = {}

    def _require_vertex(self, vertex: V) -> None:
        if vertex not in self._adjacency:
            raise KeyError(f"Vertex '{vertex}' does not exist in the graph.")

    def addVertex(self, vertex: V) -> None:
        """Add a new vertex to the graph. Raises ValueError if it already exists."""
        if vertex in self._adjacency:
            raise ValueError(f"Vertex '{vertex}' already exists.")
        self._adjacency[vertex] = []

    def addEdge(self, source: V, destination: V) -> None:
        """Create a directed edge (source -> destination)."""
        self._require_vertex(source)
        self._require_vertex(destination)
        if destination in self._adjacency[source]:
            raise ValueError(f"Directed edge '{source} -> {destination}' already exists.")
        self._adjacency[source].append(destination)

    def removeEdge(self, source: V, destination: V) -> None:
        """Remove an existing directed edge (source -> destination)."""
        self._require_vertex(source)
        self._require_vertex(destination)
        if destination not in self._adjacency[source]:
            raise ValueError(f"Directed edge '{source} -> {destination}' does not exist.")
        self._adjacency[source].remove(destination)

    def listIncomingAdjacentVertex(self, vertex: V) -> list[V]:
        """Return all vertices u such that a directed edge (u -> vertex) exists."""
        self._require_vertex(vertex)
        return [
            src
            for src, outgoing_list in self._adjacency.items()
            if vertex in outgoing_list
        ]

    def listOutgoingAdjacentVertex(self, vertex: V) -> list[V]:
        """Return all vertices w such that a directed edge (vertex -> w) exists."""
        self._require_vertex(vertex)
        return list(self._adjacency[vertex])

    def vertices(self) -> list[V]:
        """Return all vertices in insertion order."""
        return list(self._adjacency.keys())

    def edges(self) -> list[tuple[V, V]]:
        """Return all directed edges (u, v) in insertion order."""
        return [
            (src, dst)
            for src, targets in self._adjacency.items()
            for dst in targets
        ]

    def hasPath(self, start: V, target: V) -> bool:
        """Breadth-first reachability check from start to target (O(V + E))."""
        self._require_vertex(start)
        self._require_vertex(target)
        visited: set[V] = {start}
        queue: deque[V] = deque([start])
        while queue:
            current = queue.popleft()
            if current == target:
                return True
            for nxt in self._adjacency[current]:
                if nxt not in visited:
                    visited.add(nxt)
                    queue.append(nxt)
        return False
