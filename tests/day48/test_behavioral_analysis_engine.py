import unittest

from src.interview_system.behavioral_analysis_engine import (
    BehavioralAnalysisEngine,
    BehavioralObservation
)


class TestBehavioralAnalysisEngine(unittest.TestCase):

    def setUp(self):
        self.engine = BehavioralAnalysisEngine()

    def make_observation(self, **changes):

        values = {
            "observation_minutes": 20,
            "focus_observations": 50,
            "focused_observations": 40,
            "distraction_events": 4,
            "gaze_stability": 0.7,
            "head_movement_events": 10,
            "facial_engagement_observations": 30,
            "nervous_gesture_events": 5
        }

        values.update(changes)
        return BehavioralObservation(**values)

    def test_analysis_completes(self):
        result = self.engine.analyze(self.make_observation())
        self.assertEqual(result["analysis_status"], "COMPLETED")

    def test_focus_score(self):
        result = self.engine.analyze(self.make_observation())
        self.assertEqual(result["task_focus"]["score"], 80.0)

    def test_high_focus_level(self):
        result = self.engine.analyze(
            self.make_observation(focused_observations=45)
        )
        self.assertEqual(
            result["task_focus"]["level"], "HIGH_TASK_FOCUS"
        )

    def test_moderate_focus_level(self):
        result = self.engine.analyze(
            self.make_observation(focused_observations=35)
        )
        self.assertEqual(
            result["task_focus"]["level"], "MODERATE_TASK_FOCUS"
        )

    def test_low_focus_level(self):
        result = self.engine.analyze(
            self.make_observation(focused_observations=20)
        )
        self.assertEqual(
            result["task_focus"]["level"], "LOW_TASK_FOCUS"
        )

    def test_distraction_frequency(self):
        result = self.engine.analyze(self.make_observation())
        self.assertEqual(
            result["distraction_analysis"]["events_per_minute"], 0.2
        )

    def test_nervous_gestures_are_not_scored(self):
        result = self.engine.analyze(
            self.make_observation(nervous_gesture_events=100)
        )
        self.assertNotIn(
            "nervous_gesture_events",
            result["task_focus"]
        )

    def test_gaze_is_contextual(self):
        result = self.engine.analyze(self.make_observation())
        self.assertIn(
            "gaze_stability",
            result["contextual_behavioral_signals"]
        )

    def test_hiring_decision_disabled(self):
        result = self.engine.analyze(self.make_observation())
        self.assertFalse(
            result["decision_policy"]["automatic_hiring_decision"]
        )

    def test_invalid_duration(self):
        with self.assertRaises(ValueError):
            self.engine.analyze(
                self.make_observation(observation_minutes=0)
            )

    def test_invalid_focus_count(self):
        with self.assertRaises(ValueError):
            self.engine.analyze(
                self.make_observation(
                    focus_observations=10,
                    focused_observations=20
                )
            )

    def test_invalid_gaze_value(self):
        with self.assertRaises(ValueError):
            self.engine.analyze(
                self.make_observation(gaze_stability=1.5)
            )


if __name__ == "__main__":
    unittest.main()
