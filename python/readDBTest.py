import unittest
from SniffTests import SniffTests

class ExecuteSniffTests(unittest.TestCase):
    def testTablesExistence(self):
        self.assertTrue(SniffTests.testTablesExistence(self), "Tables do not exist")

if __name__ == '__main__':
    unittest.main()


