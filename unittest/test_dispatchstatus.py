import unittest
import sys

sys.path.insert(1, '../')
from enums.dispatchstatus import DispatchStatus


class MyTestCase(unittest.TestCase):

    def test_stringToEnum(self):
        enum = DispatchStatus.translate('queued')
        self.assertEqual(DispatchStatus.QUEUED, enum)
        enum = DispatchStatus.translate('QUEUED')
        self.assertEqual(DispatchStatus.QUEUED, enum)
        enum = DispatchStatus.translate('quEued')
        self.assertEqual(DispatchStatus.QUEUED, enum)
        try:
            enum = DispatchStatus.translate('wqeq')
        except ValueError as ve:
            print(ve)
            print('found ve')

    def test_queued(self):
        enum = DispatchStatus.QUEUED
        self.assertEqual('QUEUED', enum.name)
        self.assertEqual(1, enum.value)

    def testing_running(self):
        enum = DispatchStatus.RUNNING
        self.assertEqual('RUNNING', enum.name)
        self.assertEqual(2, enum.value)

    def test_done(self):
        enum = DispatchStatus.DONE
        self.assertEqual('DONE', enum.name)
        self.assertEqual(3, enum.value)


if __name__ == '__main__':
    unittest.main()
