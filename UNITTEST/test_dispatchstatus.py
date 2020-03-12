import unittest
import sys

sys.path.insert(1, '../')
from ENUMS.dispatchstatus import status


class MyTestCase(unittest.TestCase):
    
    def test_queued(self):
        self.assertEqual('queued', status.QUEUED.value)
        self.assertTrue(isinstance(status.QUEUED, status))
        print(status.QUEUED.name)
    
    def test_running(self):
        self.assertEqual('running', status.RUNNING.value)
        self.assertTrue(isinstance(status.RUNNING, status))
        print(status.RUNNING.name)
    
    def test_maintenance(self):
        self.assertEqual('done', status.DONE.value)
        self.assertTrue(isinstance(status.DONE, status))
        print(status.DONE.name)


if __name__ == '__main__':
    unittest.main()
