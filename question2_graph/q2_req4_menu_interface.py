"""Question 2 - Requirement 4: Menu-Driven CLI for Mandatory & Optional Advanced Features.

Provides the interactive command-line menu for the University Course Prerequisite
System covering all 4 Mandatory Features and a submenu for all 4 Optional Advanced Features.
"""

from __future__ import annotations
import sys as _sys
from pathlib import Path as _Path
for _p in (_Path(__file__).resolve().parent, _Path(__file__).resolve().parents[1]):
    if str(_p) not in _sys.path:
        _sys.path.insert(0, str(_p))

from typing import Callable
from question2_graph.q2_req2_course_entity import Course
from question2_graph.q2_req3_prerequisite_graph import CoursePrerequisiteSystem


MAIN_MENU = """
==== University Course Prerequisite System ====
1. View All Courses (Mandatory)
2. View Course Details - Full View (Mandatory)
3. View Prerequisites of a Course [Incoming Edges] (Mandatory)
4. View Courses Unlocked by a Course [Outgoing Edges] (Mandatory)
5. Advanced Features Submenu (Optional Features 1-4)
0. Exit"""

ADVANCED_SUBMENU = """
--- Advanced Course & Prerequisite Features ---
1. Add a Course On-Demand (New Vertex)
2. View Course Profile by Level Visibility (Core vs. Elective)
3. Add Prerequisite Y to Course X On-Demand (New Incoming Edge Y -> X)
4. Remove Prerequisite Y from Course X On-Demand (Remove Edge Y -> X)
0. Return to Main Menu"""


def _run_advanced_submenu(
    system: CoursePrerequisiteSystem,
    input_fn: Callable[[str], str],
    output_fn: Callable[[str], None],
) -> None:
    while True:
        output_fn(ADVANCED_SUBMENU)
        try:
            sub_choice = input_fn("Enter advanced choice: ").strip()
        except EOFError:
            return
        if sub_choice == "0":
            return
        try:
            if sub_choice == "1":
                code = input_fn("Enter new Course Code (e.g. CS402): ")
                name = input_fn("Enter Course Name: ")
                credits_str = input_fn("Enter Credit Hours: ")
                level = input_fn("Enter Level (Core/Elective): ")
                new_course = Course(code, name, int(credits_str.strip()), level)
                system.add_course_on_demand(new_course)
                output_fn(f"Course {new_course.course_code} - {new_course.course_name} added to graph.")
            elif sub_choice == "2":
                code = input_fn("Enter Course Code for level-based profile: ")
                output_fn(system.view_level_filtered_profile(code))
            elif sub_choice == "3":
                cx = input_fn("Enter target Course X Code: ")
                cy = input_fn("Enter prerequisite Course Y Code to add: ")
                system.add_prerequisite_on_demand(cx, cy)
                output_fn(f"Added prerequisite edge: {cy.strip().upper()} -> {cx.strip().upper()}.")
            elif sub_choice == "4":
                cx = input_fn("Enter target Course X Code: ")
                cy = input_fn("Enter prerequisite Course Y Code to remove: ")
                system.remove_prerequisite_on_demand(cx, cy)
                output_fn(f"Removed prerequisite edge: {cy.strip().upper()} -> {cx.strip().upper()}.")
            else:
                output_fn("Invalid choice. Enter 0-4.")
        except Exception as exc:
            output_fn(f"Error: {exc}")


def run_course_menu_cli(
    system: CoursePrerequisiteSystem | None = None,
    input_fn: Callable[[str], str] = input,
    output_fn: Callable[[str], None] = print,
) -> CoursePrerequisiteSystem:
    """Run the main menu loop for Question 2."""
    catalog = system or CoursePrerequisiteSystem(seed=True)

    while True:
        output_fn(MAIN_MENU)
        try:
            choice = input_fn("Enter choice: ").strip()
        except EOFError:
            output_fn("Exiting program. Goodbye!")
            break

        if choice == "0":
            output_fn("Exiting program. Goodbye!")
            break

        try:
            if choice == "1":
                output_fn("Available Courses:")
                for idx, c in enumerate(catalog.list_all_courses(), start=1):
                    output_fn(f"{idx}. {c.course_code} - {c.course_name}")
            elif choice == "2":
                code = input_fn("Enter Course Code: ")
                output_fn(catalog.view_full_course_details(code))
            elif choice == "3":
                code = input_fn("Enter Course Code: ")
                target = catalog.get_course(code)
                prereqs = catalog.get_prerequisites_for(target.course_code)
                output_fn(f"Prerequisites for {target.course_code} - {target.course_name}:")
                if prereqs:
                    for p in prereqs:
                        output_fn(f"- {p.course_code} ({p.course_name})")
                else:
                    output_fn("- None (No prerequisites required)")
            elif choice == "4":
                code = input_fn("Enter Course Code: ")
                source = catalog.get_course(code)
                unlocked = catalog.get_courses_unlocked_by(source.course_code)
                output_fn(f"Courses unlocked by {source.course_code} - {source.course_name}:")
                if unlocked:
                    for u in unlocked:
                        output_fn(f"- {u.course_code} ({u.course_name})")
                else:
                    output_fn("- None (Does not directly unlock any course)")
            elif choice == "5":
                _run_advanced_submenu(catalog, input_fn, output_fn)
            else:
                output_fn("Invalid choice. Please select 0-5.")
        except Exception as exc:
            output_fn(f"Error: {exc}")

    return catalog
