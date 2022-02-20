import unittest
from ispchecker.main import Framework


class TestFramework(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.framework = Framework()

    def test_instantiation(self):
        self.assertTrue(type(self.framework) == Framework)


if __name__ == "__main__":

    unittest.main()
