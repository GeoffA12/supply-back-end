import unittest
import sys

sys.path.insert(1, '../')
from enums.dispatchstatus import DispatchStatus


class MyTestCase(unittest.TestCase):
    
    def test_queued(self):
        self.assertEqual('queued', DispatchStatus.QUEUED.value)
        self.assertTrue(isinstance(DispatchStatus.QUEUED, DispatchStatus))
        print(DispatchStatus.QUEUED.name)
    
    def test_running(self):
        self.assertEqual('running', DispatchStatus.RUNNING.value)
        self.assertTrue(isinstance(DispatchStatus.RUNNING, DispatchStatus))
        print(DispatchStatus.RUNNING.name)
    
    def test_maintenance(self):
        self.assertEqual('done', DispatchStatus.DONE.value)
        self.assertTrue(isinstance(DispatchStatus.DONE, DispatchStatus))
        print(DispatchStatus.DONE.name)


if __name__ == '__main__':
    unittest.main()
