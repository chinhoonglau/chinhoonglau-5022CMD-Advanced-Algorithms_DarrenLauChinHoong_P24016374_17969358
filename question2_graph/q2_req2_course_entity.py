"""Question 2 - Requirement 2: University Course Entity Class & Course Profiles (5 to 10 Courses).

Defines the Course domain class with course_code, course_name, credit_hours, and level
('Core' or 'Elective'), plus helper methods for mandatory full-detail display and
optional level-based profile visibility. Seeds 8 predefined university courses (within
the required 5-10 course range).
"""

from __future__ import annotations
import sys as _sys
from pathlib import Path as _Path
for _p in (_Path(__file__).resolve().parent, _Path(__file__).resolve().parents[1]):
    if str(_p) not in _sys.path:
        _sys.path.insert(0, str(_p))

from dataclasses import dataclass


@dataclass(frozen=True)
class Course:
    """University course entity class."""
    course_code: str
    course_name: str
    credit_hours: int
    level: str  # "Core" or "Elective"

    def __post_init__(self) -> None:
        if not isinstance(self.course_code, str) or not self.course_code.strip():
            raise ValueError("Course code cannot be empty.")
        if not isinstance(self.course_name, str) or not self.course_name.strip():
            raise ValueError("Course name cannot be empty.")
        if type(self.credit_hours) is not int or self.credit_hours <= 0:
            raise ValueError("Credit hours must be a positive integer.")
        normalized_level = self.level.strip().capitalize() if isinstance(self.level, str) else ""
        if normalized_level not in {"Core", "Elective"}:
            raise ValueError("Course level must be either 'Core' or 'Elective'.")
        object.__setattr__(self, "course_code", self.course_code.strip().upper())
        object.__setattr__(self, "course_name", self.course_name.strip())
        object.__setattr__(self, "level", normalized_level)

    def format_full_details(self) -> str:
        """Mandatory Feature 2: Ignore level/visibility setting and display all fields."""
        return (
            f"Course Code  : {self.course_code}\n"
            f"Course Name  : {self.course_name}\n"
            f"Credit Hours : {self.credit_hours}\n"
            f"Course Level : {self.level}"
        )

    def format_visibility_profile(self) -> str:
        """Optional Advanced Feature 2: Elective shows only course name; Core shows all details."""
        if self.level == "Elective":
            return f"{self.course_name} (Elective - additional details hidden by visibility policy)"
        return self.format_full_details()


def create_predefined_courses() -> list[Course]:
    """Create 8 predefined university courses (satisfying the 5 to 10 course constraint)."""
    return [
        Course("CS101", "Introduction to Programming", 4, "Core"),
        Course("CS102", "Discrete Mathematics", 3, "Core"),
        Course("CS201", "Data Structures and Algorithms", 4, "Core"),
        Course("CS202", "Computer Organization", 3, "Core"),
        Course("CS301", "Advanced Algorithms", 4, "Core"),
        Course("CS302", "Database Systems", 3, "Core"),
        Course("CS305", "Cloud Computing Architecture", 3, "Elective"),
        Course("CS401", "Machine Learning Foundations", 3, "Elective"),
    ]
