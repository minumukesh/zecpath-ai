import unittest

from src.interview_system.malpractice_detection_engine import (
    MalpracticeDetectionEngine,
    InterviewIntegrityEvents
)


class TestMalpracticeDetectionEngine(unittest.TestCase):

    def setUp(self):
        self.engine = MalpracticeDetectionEngine()

    def make_events(self, **changes):

        values = {
            "interview_id": "TEST-049",
            "duration_minutes": 30,
            "tab_switches": 1,
            "screen_focus_losses": 1,
            "external_voice_events": 0,
            "looking_away_events": 1,
            "repeated_event_intervals": 0,
            "consent_confirmed": True
        }

        values.update(changes)

        return InterviewIntegrityEvents(**values)

    def test_analysis_completes(self):
        result = self.engine.analyze(self.make_events())
        self.assertEqual(result["analysis_status"], "COMPLETED")

    def test_no_threshold_flags(self):
        result = self.engine.analyze(self.make_events())
        self.assertEqual(len(result["threshold_flags"]), 0)

    def test_tab_switch_threshold(self):
        result = self.engine.analyze(
            self.make_events(tab_switches=5)
        )
        self.assertIn(
            "tab_switches",
            result["pattern_analysis"]["exceeded_signals"]
        )

    def test_screen_focus_threshold(self):
        result = self.engine.analyze(
            self.make_events(screen_focus_losses=5)
        )
        self.assertTrue(
            any(
                flag["signal"] == "screen_focus_losses"
                for flag in result["threshold_flags"]
            )
        )

    def test_external_voice_threshold(self):
        result = self.engine.analyze(
            self.make_events(external_voice_events=3)
        )
        self.assertTrue(
            any(
                flag["signal"] == "external_voice_events"
                for flag in result["threshold_flags"]
            )
        )

    def test_looking_away_threshold(self):
        result = self.engine.analyze(
            self.make_events(looking_away_events=8)
        )
        self.assertTrue(
            any(
                flag["signal"] == "looking_away_events"
                for flag in result["threshold_flags"]
            )
        )

    def test_multiple_signal_pattern(self):
        result = self.engine.analyze(
            self.make_events(
                tab_switches=6,
                screen_focus_losses=6
            )
        )
        self.assertEqual(
            result["pattern_analysis"]["status"],
            "MULTI_SIGNAL_PATTERN_DETECTED"
        )

    def test_human_review_required(self):
        result = self.engine.analyze(self.make_events())
        self.assertTrue(result["human_review"]["required"])

    def test_automatic_rejection_disabled(self):
        result = self.engine.analyze(self.make_events())
        self.assertFalse(
            result["human_review"]["automatic_candidate_rejection"]
        )

    def test_missing_consent_blocks_assessment(self):
        result = self.engine.analyze(
            self.make_events(consent_confirmed=False)
        )
        self.assertEqual(
            result["analysis_status"],
            "BLOCKED_CONSENT_REQUIRED"
        )
        self.assertIsNone(
            result["risk_assessment"]["review_indicator"]
        )
        self.assertEqual(result["threshold_flags"], [])

    def test_invalid_duration(self):
        with self.assertRaises(ValueError):
            self.engine.analyze(
                self.make_events(duration_minutes=0)
            )

    def test_negative_event_count(self):
        with self.assertRaises(ValueError):
            self.engine.analyze(
                self.make_events(tab_switches=-1)
            )

    def test_empty_interview_id(self):
        with self.assertRaises(ValueError):
            self.engine.analyze(
                self.make_events(interview_id="")
            )


if __name__ == "__main__":
    unittest.main()
