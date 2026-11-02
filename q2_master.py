"""Question 2 Master Runner File (q2_master.py).

Imports and links all four Question 2 requirement modules:
  1. q2_req1_directed_graph      (DirectedGraph)
  2. q2_req2_course_entity       (Course, create_predefined_courses)
  3. q2_req3_prerequisite_graph  (CoursePrerequisiteSystem)
  4. q2_req4_menu_interface      (run_course_menu_cli)
"""

from __future__ import annotations
import sys as _sys
from pathlib import Path as _Path
for _p in (_Path(__file__).resolve().parent, _Path(__file__).resolve().parents[1]):
    if str(_p) not in _sys.path:
        _sys.path.insert(0, str(_p))

from question2_graph.q2_req1_directed_graph import DirectedGraph
from question2_graph.q2_req2_course_entity import Course, create_predefined_courses
from question2_graph.q2_req3_prerequisite_graph import CoursePrerequisiteSystem
from question2_graph.q2_req4_menu_interface import run_course_menu_cli


def main() -> None:
    """Initialize the Course Prerequisite System and launch the CLI menu."""
    prereq_system = CoursePrerequisiteSystem(seed=True)
    run_course_menu_cli(prereq_system)


if __name__ == "__main__":
    main()
