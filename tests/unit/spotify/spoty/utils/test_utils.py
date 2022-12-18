import unittest
from spotify.spoty.utils import time_format


class TestUtils(unittest.TestCase):
    
    def test_time_format(self):
        self.assertEqual(time_format(1000), "00:01")
        self.assertIn(":", time_format(1000))
        self.assertEqual(time_format(4753479347), "1320:24:39")
        self.assertEqual(time_format(0), "00:00")


if __name__ == "__main__":
    unittest.main()
