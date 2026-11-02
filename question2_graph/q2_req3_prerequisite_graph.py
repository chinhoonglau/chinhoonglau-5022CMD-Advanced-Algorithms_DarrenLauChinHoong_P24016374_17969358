"""Question 2 - Requirement 3: Course-Prerequisite System & Optional Advanced Graph Operations.

Connects the generic DirectedGraph[str] with Course objects.
Edge semantics:
  A directed edge (Y -> X) means Course Y is a direct prerequisite of Course X,
  and completing Course Y directly unlocks Course X.
  - Incoming edges of X (`listIncomingAdjacentVertex(X)`) = Prerequisites required by X.
  - Outgoing edges of Y (`listOutgoingAdjacentVertex(Y)`) = Courses unlocked by Y.
"""

from __future__ import annotations
import sys as _sys
from pathlib import Path as _Path
for _p in (_Path(__file__).resolve().parent, _Path(__file__).resolve().parents[1]):
    if str(_p) not in _sys.path:
        _sys.path.insert(0, str(_p))

from question2_graph.q2_req1_directed_graph import DirectedGraph
from question2_graph.q2_req2_course_entity import Course, create_predefined_courses


class CoursePrerequisiteSystem:
    """Manages university courses and their directed prerequisite relationships."""

    MIN_COURSES = 5
    MAX_COURSES = 10

    def __init__(self, seed: bool = True) -> None:
        self.graph: DirectedGraph[str] = DirectedGraph()
        self.courses: dict[str, Course] = {}
        if seed:
            self._seed_default_network()

    def _seed_default_network(self) -> None:
        for course in create_predefined_courses():
            self.courses[course.course_code] = course
            self.graph.addVertex(course.course_code)

        # Directed edges: Prerequisite Y -> Target Course X
        default_prerequisites = [
            ("CS101", "CS201"),  # Intro to Programming -> Data Structures
            ("CS102", "CS201"),  # Discrete Math -> Data Structures
            ("CS101", "CS202"),  # Intro to Programming -> Computer Organization
            ("CS201", "CS301"),  # Data Structures -> Advanced Algorithms
            ("CS102", "CS301"),  # Discrete Math -> Advanced Algorithms
            ("CS201", "CS302"),  # Data Structures -> Database Systems
            ("CS201", "CS305"),  # Data Structures -> Cloud Computing (Elective)
            ("CS301", "CS401"),  # Advanced Algorithms -> Machine Learning (Elective)
        ]
        for prereq_code, target_code in default_prerequisites:
            self.graph.addEdge(prereq_code, target_code)

    def get_course(self, code: str) -> Course:
        if not isinstance(code, str) or not code.strip():
            raise ValueError("Course code cannot be blank.")
        clean_code = code.strip().upper()
        if clean_code not in self.courses:
            raise KeyError(f"Course '{clean_code}' is not registered.")
        return self.courses[clean_code]

    # --- Mandatory Features ---
    def list_all_courses(self) -> list[Course]:
        return [self.courses[code] for code in self.graph.vertices()]

    def view_full_course_details(self, code: str) -> str:
        return self.get_course(code).format_full_details()

    def get_prerequisites_for(self, code: str) -> list[Course]:
        target = self.get_course(code)
        incoming_codes = self.graph.listIncomingAdjacentVertex(target.course_code)
        return [self.courses[c] for c in incoming_codes]

    def get_courses_unlocked_by(self, code: str) -> list[Course]:
        source = self.get_course(code)
        outgoing_codes = self.graph.listOutgoingAdjacentVertex(source.course_code)
        return [self.courses[c] for c in outgoing_codes]

    # --- Optional Advanced Features ---
    def add_course_on_demand(self, course: Course) -> None:
        """Advanced Feature 1: Add a new course vertex on-demand (up to MAX_COURSES=10)."""
        if course.course_code in self.courses:
            raise ValueError(f"Course '{course.course_code}' already exists.")
        if len(self.courses) >= self.MAX_COURSES:
            raise ValueError(f"Cannot exceed the maximum of {self.MAX_COURSES} courses.")
        self.courses[course.course_code] = course
        self.graph.addVertex(course.course_code)

    def view_level_filtered_profile(self, code: str) -> str:
        """Advanced Feature 2: Elective shows only name; Core shows all details."""
        return self.get_course(code).format_visibility_profile()

    def add_prerequisite_on_demand(self, course_x_code: str, prereq_y_code: str) -> None:
        """Advanced Feature 3: Add Course Y as a prerequisite for Course X (edge Y -> X)."""
        course_x = self.get_course(course_x_code)
        prereq_y = self.get_course(prereq_y_code)
        if course_x.course_code == prereq_y.course_code:
            raise ValueError("A course cannot be a prerequisite of itself.")
        if self.graph.hasPath(course_x.course_code, prereq_y.course_code):
            raise ValueError(
                f"Cycle detected: '{course_x.course_code}' is already a prerequisite of '{prereq_y.course_code}'."
            )
        self.graph.addEdge(prereq_y.course_code, course_x.course_code)

    def remove_prerequisite_on_demand(self, course_x_code: str, prereq_y_code: str) -> None:
        """Advanced Feature 4: Remove Course Y as a prerequisite for Course X (remove edge Y -> X)."""
        course_x = self.get_course(course_x_code)
        prereq_y = self.get_course(prereq_y_code)
        self.graph.removeEdge(prereq_y.course_code, course_x.course_code)
