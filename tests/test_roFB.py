import os
import sys


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

import roFB
# ...existing code...
import unittest

class TestRoFBFunctions(unittest.TestCase):
    def test_sizen(self, size):
        self.assertEqual(roFB.main(f'src/test_{size}.txt'), 366)

    sizes = [10, 100, 1000, 10000, 50000]
    
    def testSizes(self):
        for size in self.sizes:
            with self.subTest(size=size):
                self.test_sizen(size)

if __name__ == '__main__':
    unittest.main()