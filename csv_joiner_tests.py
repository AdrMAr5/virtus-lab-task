import unittest
from csv_joiner import Parser


class CSVJoinerTest(unittest.TestCase):
    def test_parser(self):
        input_data = ['314,752,81,""vcbc""', '43.03,0.47,2076.45,22884',
                        '22893,29672,ios,10.1,"iPhone9,3",3', '317,222,29,"""."',
                        '312,102,32,"r,,,""bb"', '314,752,81,""vcbc""']

        expected_output = [['314', '752', '81', '""vcbc""'], ['43.03', '0.47', '2076.45', '22884'],
                           ['22893', '29672', 'ios', '10.1', '"iPhone9,3"', '3'], ['317', '222', '29', '"""."'],
                           ['312', '102', '32', '"r,,,""bb"'], ['314', '752', '81', '""vcbc""']]

        for i in range(len(input_data)):
            self.assertEqual(expected_output[i], Parser.parse_line(input_data[i]))


