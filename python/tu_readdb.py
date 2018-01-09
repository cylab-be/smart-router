import unittest
from tu_basics import tu_basics

class Executetu_readdb(unittest.TestCase):
    def testTablesExistence(self):
        self.assertTrue(tu_basics.testTablesExistence(self), "Tables do not exist")

if __name__ == '__main__':
    unittest.main()


