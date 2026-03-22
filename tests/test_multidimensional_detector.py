import unittest

from haribo_orom.multidimensional_detector import MultidimensionalDetector


class TestMultidimensionalDetector(unittest.TestCase):
    def setUp(self) -> None:
        self.detector = MultidimensionalDetector(owner="Ibrahim Sakarya")

    def test_scan_dimensions_returns_dict(self) -> None:
        result = self.detector.scan_dimensions()
        self.assertIsInstance(result, dict)
        self.assertIn("physique", result)
        self.assertIn("quantique", result)
        self.assertIn("conscience", result)

    def test_detect_threats_returns_list(self) -> None:
        threats = self.detector.detect_threats()
        self.assertIsInstance(threats, list)

    def test_owner_identity(self) -> None:
        self.assertEqual(self.detector.owner, "Ibrahim Sakarya")


if __name__ == "__main__":
    unittest.main()
