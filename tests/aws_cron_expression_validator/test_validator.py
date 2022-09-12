import re
from typing import List
from unittest import TestCase

from src.aws_cron_expression_validator.validator import AWSCronExpressionValidator


class TestAWSCronExpressionValidator(TestCase):
    def _then_matches(self, regex: str, matches: List[str]):
        for match in matches:
            self._check_match(regex, match)

    def _check_match(self, regex: str, match: str):
        assert re.fullmatch(regex, match)

    def _then_does_not_match(self, regex: str, matches: List[str]):
        for match in matches:
            self._check_non_match(regex, match)

    def _check_non_match(self, regex: str, match: str):
        assert not re.fullmatch(regex, match)

    def test_slash_regex(self):
        given_regex = AWSCronExpressionValidator.slash_regex("")
        given_valid_matches = ["/", "*/", "1/", "01/", "10/", "010/", "123/", "0123/"]
        given_invalid_matches = ["", "1", "0/", "-1/", "*1/", "1*/", "asdf/", "*asdf/", "asdf*/"]
        self._then_matches(given_regex, given_valid_matches)
        self._then_does_not_match(given_regex, given_invalid_matches)

    def test_range_regex(self):
        given_regex = AWSCronExpressionValidator.range_regex(r"[B-Y]")
        given_valid_matches = ["B", "*-D", "D-*", "B-Y", "D-F", "D-B"]
        given_invalid_matches = ["*-*", "*B", "A-D", "D-Z", "B-C-D", ""]
        self._then_matches(given_regex, given_valid_matches)
        self._then_does_not_match(given_regex, given_invalid_matches)

    def test_list_regex(self):
        given_regex = AWSCronExpressionValidator.list_regex(r"[B-Y]")
        given_valid_matches = ["D", "D,F", "F-D", "D,F,C,J", "D-F,J", "B,D-F,J", "D,F-J", "*-R,X", "R,X-*", "*-R,T,X-*"]
        given_invalid_matches = ["*,P", "P,*,Q", "Q-P,*", "", "D,F,", ",D,F", ""]
        self._then_matches(given_regex, given_valid_matches)
        self._then_does_not_match(given_regex, given_invalid_matches)

    def test_common_regex(self):

        given_regex = AWSCronExpressionValidator.common_regex(r"[B-Y]")

        given_valid_matches = ["*", "*/D", "/D", "D", "D,F", "F-D", "D-F,J"]
        given_invalid_matches = ["", "A", "Z", "/", "*B/", "B*/", "BCD/", "*BCD/", "BCD*/"]
        self._then_matches(given_regex, given_valid_matches)
        self._then_does_not_match(given_regex, given_invalid_matches)

    def test_minute_regex(self):
        given_regex = AWSCronExpressionValidator.minute_regex()

        given_valid_matches = ["*", "0", "1", "01", "10", "59"]
        given_invalid_matches = ["60", "600", "-1", ""]

        self._then_matches(given_regex, given_valid_matches)
        self._then_does_not_match(given_regex, given_invalid_matches)

    def test_hour_regex(self):
        given_regex = AWSCronExpressionValidator.hour_regex()
        given_valid_matches = ["*", "0", "1", "01", "10", "23"]
        given_invalid_matches = ["24", "600", "001", "-1"]
        self._then_matches(given_regex, given_valid_matches)
        self._then_does_not_match(given_regex, given_invalid_matches)

    def test_day_of_month_regex(self):
        given_regex = AWSCronExpressionValidator.day_of_month_regex()
        given_valid_matches = ["*", "1", "01", "10", "23", "31", "?", "L", "1W", "31W", "11W"]
        given_invalid_matches = [
            "0",
            "32",
            "600",
            "-1",
            "?10",
            "8?",
            "8L",
            "8-L",
            "L8",
            "W",
            "8-W",
            "-1W",
            "/8W",
            "*/8W",
            "?W",
            "",
        ]

        self._then_matches(given_regex, given_valid_matches)
        self._then_does_not_match(given_regex, given_invalid_matches)

    def test_month_regex(self):
        given_regex = AWSCronExpressionValidator.month_regex()

        given_valid_matches = ["*", "1", "01", "10", "12", "JAN", "FEB", "DEC", "JAN-MAR", "02-MAR", "*-MAR", "2/FEB"]
        given_invalid_matches = ["0", "13", "600", "-1", "XZY", "JANUARY", ""]

        self._then_matches(given_regex, given_valid_matches)
        self._then_does_not_match(given_regex, given_invalid_matches)

    def test_day_of_week_regex(self):
        given_regex = AWSCronExpressionValidator.day_of_week_regex()
        given_valid_matches = ["*", "1", "5", "7", "MON", "?", "L", "3#2", "MON-FRI"]
        given_invalid_matches = [
            "Monday",
            "0",
            "01",
            "8",
            "?5",
            "5?",
            "5L",
            "5-L",
            "L5",
            "#",
            "0#2",
            "8#2",
            "600#2",
            "-1#2",
            "3#0",
            "3#6",
            "3#600",
            "3#-1",
            "3#",
            "#2",
            "3-#2",
            "2/MON",
            "/3#2",
            "*/3#2",
            "3#2,5#3",
            "3#2-4#2",
            "",
        ]
        self._then_matches(given_regex, given_valid_matches)
        self._then_does_not_match(given_regex, given_invalid_matches)

    def test_year_regex(self):
        given_regex = AWSCronExpressionValidator.year_regex()

        given_valid_matches = ["*", "1970", "2199", "2022", "1992"]
        given_invalid_matches = ["1969", "2200", "2222", "1111", "20221", "0", "1", "", "*1970", "19*70"]

        self._then_matches(given_regex, given_valid_matches)
        self._then_does_not_match(given_regex, given_invalid_matches)

    def test_validator(self):
        valid_expressions = [
            "0 18 ? * MON-FRI *",
            "0 18 ? * L *",
            "0 18 L * ? *",
            "0 18 31W * ? *",
            "0 10 * * ? *",
            "15 12 * * ? *",
            "0 8 1 * ? *",
            "1/5 8-17 ? * MON-FRI *",
            "0 9 ? * 2#1 *",
            "0 07/12 ? * * *",
            "10,20,30,40 07/12 ? * * *",
            "10 10,15,20,23 ? * * *",
            "10 10 15,30,31 * ? *",
            "10 10 15 JAN,JUL,DEC ? *",
            "10 10 31 04,09,12 ? *",
            "0,5 07/12 ? * 1,5,7 *",
            "0,5 07/12 ? * 1,5,7 2020,2021,2028,2199",
            "0,5 07/12 ? * 1,5,7 2020-2021,2028-2199",
            "0,5 07/12 ? * 1,5,7 2000-2199",
            "0 9-5 ? * MON-FRI *",
            "30 0 ? * MON *",
            "30 7 ? * MON#1 *",
            "30 0 1 JAN,APR,JUL,OCT ? *",
        ]

        invalid_expressions = [
            "0 18 ? * MON-FRI",
            "0 18 * * * *",
            "0 65 * * ? *",
            "0 18 32W * ? *",
            "0 18 W * ? *",
            "89 10 * * ? *",
            "15/65 10 * * ? *",
            "15/30 10 * * ? 2400",
            "0 9 ? * 2#6 *",
            "0 9 ? * ? *",
            "10 10 31 04,09,13 ? *",
            "0,5 07/12 ? * 01,05,8 *",
            "0,5 07/12 ? * 01,05,7 2000-2200",
        ]

        for valid_expression in valid_expressions:
            self.assertEqual(AWSCronExpressionValidator.validate(valid_expression), valid_expression)

        for invalid_expression in invalid_expressions:
            print(invalid_expression)
            with self.assertRaises(ValueError):
                AWSCronExpressionValidator.validate(invalid_expression)
