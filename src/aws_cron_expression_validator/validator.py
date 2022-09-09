from __future__ import annotations

import re


class AWSCronExpressionValidator:

    """
    Validates these AWS EventBridge cron expressions, which are similar to, but not compatible with unix cron expressions:
    https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-create-rule-schedule.html#eb-cron-expressions

    | Field        | Values          | Wildcards     |
    | :----------: | :-------------: | :-----------: |
    | Minute       | 0-59            | , - * /       |
    | Hour         | 0-23            | , - * /       |
    | Day-of-month | 1-31            | , - * ? / L W |
    | Month        | 1-12 or JAN-DEC | , - * /       |
    | Day-of-week  |  1-7 or SUN-SAT | , - * ? L #   |
    | Year         | 1970-2199       | , - * /       |
    """

    minute_values = r"(0?[0-9]|[1-5][0-9])"  # [0]0-59
    hour_values = r"(0?[0-9]|1[0-9]|2[0-3])"  # [0]0-23
    month_of_day_values = r"(0?[1-9]|[1-2][0-9]|3[0-1])"  # [0]1-31
    month_values = r"(0?[1-9]|1[0-2]|JAN|FEB|MAR|APR|MAY|JUN|JUL|AUG|SEP|OCT|NOV|DEC)"  # [0]1-12 or JAN-DEC
    day_of_week_values = r"([1-7]|SUN|MON|TUE|WED|THU|FRI|SAT)"  # 1-7 or SAT-SUN
    day_of_week_hash = rf"({day_of_week_values}#[1-5])"  # Day of the week in the Nth week of the month
    year_values = r"((19[7-9][0-9])|(2[0-1][0-9][0-9]))"  # 1970-2199

    @classmethod
    def validate(cls, expression: str) -> str:

        value_count = len(expression.split(" "))
        if value_count != 6:
            raise ValueError(f"Incorrect number of values in '{expression}'. 6 required, {value_count} provided.")

        minute, hour, day_of_month, month, day_of_week, year = expression.split(" ")

        if not ((day_of_month == "?" and day_of_week != "?") or (day_of_month != "?" and day_of_week == "?")):
            raise ValueError(
                f"Invalid combination of day-of-month '{day_of_month}' and day-of-week '{day_of_week}'. One must be a question mark (?)"
            )

        if not re.fullmatch(cls.minute_regex(), minute):
            raise ValueError(f"Invalid minute value '{minute}'.")
        if not re.fullmatch(cls.hour_regex(), hour):
            raise ValueError(f"Invalid hour value '{hour}'.")
        if not re.fullmatch(cls.day_of_month_regex(), day_of_month):
            raise ValueError(f"Invalid day-of-month value '{day_of_month}'.")
        if not re.fullmatch(cls.month_regex(), month):
            raise ValueError(f"Invalid month value '{month}'.")
        if not re.fullmatch(cls.day_of_week_regex(), day_of_week):
            raise ValueError(f"Invalid day-of-week value '{day_of_week}'.")
        if not re.fullmatch(cls.year_regex(), year):
            raise ValueError(f"Invalid year value '{year}'.")

        return expression

    @classmethod
    def range_regex(cls, values) -> str:
        return rf"({values}|(\*\-{values})|({values}\-{values})|({values}\-\*))"  # v , *-v , v-v or v-*

    @classmethod
    def list_regex(cls, values):
        range_ = cls.range_regex(values)
        return rf"({range_}(\,{range_})*)"  # One or more ranges separated by a comma

    @classmethod
    def slash_regex(cls, values):
        return rf"((\*|[0-9]*[1-9][0-9]*)?\/{values})"  # Slash can be preceded by nothing, * or a natural number

    @classmethod
    def common_regex(cls, values):
        return rf"({cls.list_regex(values)}|\*|{cls.slash_regex(values)})"  # values , - * /

    @classmethod
    def minute_regex(cls):
        return rf"^({cls.common_regex(cls.minute_values)})$"  # values , - * /

    @classmethod
    def hour_regex(cls):
        return rf"^({cls.common_regex(cls.hour_values)})$"  # values , - * /

    @classmethod
    def day_of_month_regex(cls):
        return (
            rf"^({cls.common_regex(cls.month_of_day_values)}|\?|L|{cls.month_of_day_values}W)$"  # values , - * / ? L W
        )

    @classmethod
    def month_regex(cls):
        return rf"^({cls.common_regex(cls.month_values)})$"  # values , - * /

    @classmethod
    def day_of_week_regex(cls):
        return rf"^({cls.list_regex(cls.day_of_week_values)}|\*|\?|L|{cls.day_of_week_hash})$"  # values , - * ? L #

    @classmethod
    def year_regex(cls):
        return rf"^({cls.common_regex(cls.year_values)}|\?|L)$"  # values , - * /
