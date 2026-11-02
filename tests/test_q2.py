"""Automated unit tests for Question 2 (Directed Graph & Course Prerequisite System)."""

import unittest
from question2_graph.q2_req1_directed_graph import DirectedGraph
from question2_graph.q2_req2_course_entity import Course
from question2_graph.q2_req3_prerequisite_graph import CoursePrerequisiteSystem
from question2_graph.q2_req4_menu_interface import run_course_menu_cli


class TestQuestion2Graph(unittest.TestCase):
    def test_generic_directed_graph(self) -> None:
        g: DirectedGraph[int] = DirectedGraph()
        for v in (10, 20, 30):
            g.addVertex(v)
        g.addEdge(10, 30)
        g.addEdge(20, 30)
        self.assertEqual(g.listIncomingAdjacentVertex(30), [10, 20])
        self.assertEqual(g.listOutgoingAdjacentVertex(10), [30])
        g.removeEdge(10, 30)
        self.assertEqual(g.listIncomingAdjacentVertex(30), [20])

    def test_course_prerequisite_mandatory_and_advanced_features(self) -> None:
        sys_cat = CoursePrerequisiteSystem(seed=True)
        self.assertEqual(len(sys_cat.list_all_courses()), 8)
        prereqs_301 = [c.course_code for c in sys_cat.get_prerequisites_for("CS301")]
        self.assertEqual(prereqs_301, ["CS102", "CS201"])
        unlocked_201 = [c.course_code for c in sys_cat.get_courses_unlocked_by("CS201")]
        self.assertEqual(unlocked_201, ["CS301", "CS302", "CS305"])

        # Optional Advanced Feature 1: Add Course on-demand
        sys_cat.add_course_on_demand(Course("CS402", "Deep Learning", 4, "Elective"))
        self.assertEqual(len(sys_cat.list_all_courses()), 9)

        # Optional Advanced Feature 2: Level-based profile visibility
        elective_view = sys_cat.view_level_filtered_profile("CS305")
        self.assertIn("Cloud Computing Architecture", elective_view)
        self.assertNotIn("Credit Hours", elective_view)
        core_view = sys_cat.view_level_filtered_profile("CS301")
        self.assertIn("Credit Hours : 4", core_view)

        # Optional Advanced Feature 3 & 4: Add & remove prerequisite on-demand + cycle prevention
        sys_cat.add_prerequisite_on_demand("CS402", "CS301")
        self.assertIn("CS301", [c.course_code for c in sys_cat.get_prerequisites_for("CS402")])
        with self.assertRaises(ValueError):
            sys_cat.add_prerequisite_on_demand("CS101", "CS301")  # Would create a cycle
        sys_cat.remove_prerequisite_on_demand("CS402", "CS301")
        self.assertEqual(sys_cat.get_prerequisites_for("CS402"), [])

        # CLI walkthrough
        inputs = iter(["1", "2", "CS305", "3", "CS301", "4", "CS201", "5", "2", "CS305", "0", "0"])
        outputs: list[str] = []
        run_course_menu_cli(sys_cat, input_fn=lambda _: next(inputs), output_fn=outputs.append)
        joined = "\n".join(outputs)
        self.assertIn("Prerequisites for CS301", joined)
        self.assertIn("Courses unlocked by CS201", joined)


if __name__ == "__main__":
    unittest.main()
