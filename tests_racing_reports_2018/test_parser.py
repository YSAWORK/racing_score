from unittest.mock import patch
import os, unittest, argparse
import racing_reports_2018 as code

BASE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)))
HOME_DIR = BASE_DIR.replace('/tests_racing_reports_2018', '')

class TestParserMain(unittest.TestCase):
    def setUp(self):
        self.test_cases = [
            (f'{HOME_DIR}/log_data', 'Lewis Hamilton', None),
            (f'{HOME_DIR}/log_data', None, None),
            (f'{HOME_DIR}/log_data', None, True),]

    # testing create_parser in parser_main.py
    def test_create_parser(self):
        for case in self.test_cases:
            @patch('argparse.ArgumentParser.parse_args',
                   return_value=argparse.Namespace(files=case[0],driver=case[1],desc=case[2]))
            def get_test_create_parser(mock_args):
                assert code.create_parser().parse_args(mock_args) == argparse.Namespace(files=case[0],driver=case[1],desc=case[2])
            get_test_create_parser()

    # testing choose_and_format_data in parser_main.py
    def test_choose_and_format_data(self):
        for case in self.test_cases:
            @patch('argparse.ArgumentParser.parse_args',
                        return_value=argparse.Namespace(files=case[0],driver=case[1],desc=case[2]))
            def get_test_choose_and_format_data(mock_args):
                with open(f'{case[0]}/abbreviations.txt') as file_drivers, open(f'{case[0]}/start.log') as file_start, open(f'{case[0]}/end.log') as file_end:
                    test_driver = file_drivers.read().splitlines()
                    test_start = file_start.read().splitlines()
                    test_end = file_end.read().splitlines()
                    testing_code = code.choose_and_format_data(code.create_parser().parse_args())
                    with open(f'{testing_code[0].name}') as file_drivers_2, open(f'{testing_code[1].name}') as file_start_2, open(f'{testing_code[2].name}') as file_end_2:
                        assert (file_drivers_2.read().splitlines(),
                                file_start_2.read().splitlines(),
                                file_end_2.read().splitlines(),
                                testing_code[3],
                                testing_code[4]) == (test_driver, test_start, test_end, case[2], case[1])
            get_test_choose_and_format_data()
