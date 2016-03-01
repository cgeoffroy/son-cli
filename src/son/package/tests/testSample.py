import unittest


class MyTestCase(unittest.TestCase):
    def test_something(self):
        """Dummy test on something"""
        self.assertEqual(True, True)

class MyTestCase2(unittest.TestCase):
    def test_something2(self):
        self.assertEqual(True, True)


if __name__ == '__main__':
    unittest.main()
