import unittest
from final_assignment import *

class TestNewAlgorithm(unittest.TestCase):
    def test_sort(self):
        combo_sort.set('Name')
        array_test=[('103','harish','dhangadhi','9876543232','computing'),
                    ('104', 'kale', 'dang','9823659824', 'computing')]
        expected_result = [('103','harish','dhangadhi','9876543232','computing'),
                    ('104', 'kale', 'dang','9823659824', 'computing')]

        quickSort(array_test, 0, len(array_test) - 1)
        self.assertEqual(array_test, expected_result)

    def test_search(self):
        combo_search.set('Name')
        entry_search.insert(0, 'harish')

        test_array=[('103','harish','dhangadhi','9876543232','computing'),
                    ('104', 'kale', 'dang','9823659824', 'computing')]

        expected_result=[('103','harish','dhangadhi','9876543232','computing')]
        mylist = search(test_array)

        self.assertEqual(mylist, expected_result)
if __name__ == '__main__':
    unittest.main()