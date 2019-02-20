import unittest

import xbox360controller


class TestMethods(unittest.TestCase):
    def test_add(self):
        self.assertEqual(xbox360controller.Xbox360Controller.LED_OFF, 0)


if __name__ == "__main__":
    unittest.main()
