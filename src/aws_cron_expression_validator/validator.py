from __future__ import annotations

import re


class AWSCronExpressionError(ValueError):
    pass


class AWSCronExpressionMinuteError(AWSCronExpressionError):
    pass


class AWSCronExpressionHourError(AWSCronExpressionError):
    pass


class AWSCronExpressionMonthError(AWSCronExpressionError):
    pass


class AWSCronExpressionYearError(AWSCronExpressionError):
    pass


class AWSCronExpressionDayOfMonthError(AWSCronExpressionError):
    pass


class AWSCronExpressionDayOfWeekError(AWSCronExpressionError):
    pass


class AWSCronExpressionValidator:

    """
    Validates these AWS EventBridge cron expressions, which are similar to, but not compatible with standard
    unix cron expressions:
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
    month_values = r"(?i)(0?[1-9]|1[0-2]|JAN|FEB|MAR|APR|MAY|JUN|JUL|AUG|SEP|OCT|NOV|DEC)"  # [0]1-12 or JAN-DEC
    day_of_week_values = r"(?i)([1-7]|SUN|MON|TUE|WED|THU|FRI|SAT)"  # 1-7 or SAT-SUN
    day_of_week_hash = rf"({day_of_week_values}#[1-5])"  # Day of the week in the Nth week of the month
    year_values = r"((19[7-9][0-9])|(2[0-1][0-9][0-9]))"  # 1970-2199
    natural_number = r"([0-9]*[1-9][0-9]*)"  # Integers greater than 0

    @classmethod
    def validate(cls, expression: str) -> str:

        value_count = len(expression.split(" "))
        if value_count != 6:
            raise AWSCronExpressionError(
                f"Incorrect number of values in '{expression}'. 6 required, {value_count} provided."
            )

        minute, hour, day_of_month, month, day_of_week, year = expression.split(" ")

        if not ((day_of_month == "?" and day_of_week != "?") or (day_of_month != "?" and day_of_week == "?")):
            raise AWSCronExpressionError(
                f"Invalid combination of day-of-month '{day_of_month}' and day-of-week '{day_of_week}'."
                "One must be a question mark (?)"
            )

        if not re.fullmatch(cls.minute_regex(), minute):
            raise AWSCronExpressionMinuteError(f"Invalid minute value '{minute}'.")
        if not re.fullmatch(cls.hour_regex(), hour):
            raise AWSCronExpressionHourError(f"Invalid hour value '{hour}'.")
        if not re.fullmatch(cls.day_of_month_regex(), day_of_month):
            raise AWSCronExpressionDayOfMonthError(f"Invalid day-of-month value '{day_of_month}'.")
        if not re.fullmatch(cls.month_regex(), month):
            raise AWSCronExpressionMonthError(f"Invalid month value '{month}'.")
        if not re.fullmatch(cls.day_of_week_regex(), day_of_week):
            raise AWSCronExpressionDayOfWeekError(f"Invalid day-of-week value '{day_of_week}'.")
        if not re.fullmatch(cls.year_regex(), year):
            raise AWSCronExpressionYearError(f"Invalid year value '{year}'.")

        return expression

    @classmethod
    def range_regex(cls, values: str) -> str:
        return rf"({values}|(\*\-{values})|({values}\-{values})|({values}\-\*))"  # v , *-v , v-v or v-*

    @classmethod
    def list_range_regex(cls, values: str) -> str:
        range_ = cls.range_regex(values)
        return rf"({range_}(\,{range_})*)"  # One or more ranges separated by a comma

    @classmethod
    def slash_regex(cls, values: str) -> str:
        range_ = cls.range_regex(values)
        return rf"((\*|{range_}|{values})\/{cls.natural_number})"
        # Slash can be preceded by *, range, or a valid value and must be followed by a natural
        # number as the increment.

    @classmethod
    def list_slash_regex(cls, values: str) -> str:
        slash = cls.slash_regex(values)
        slash_or_range = rf"({slash}|{cls.range_regex(values)})"
        return rf"({slash_or_range}(\,{slash_or_range})*)"  # One or more separated by a comma

    @classmethod
    def common_regex(cls, values: str) -> str:
        return rf"({cls.list_range_regex(values)}|\*|{cls.list_slash_regex(values)})"  # values , - * /

    @classmethod
    def minute_regex(cls) -> str:
        return rf"^({cls.common_regex(cls.minute_values)})$"  # values , - * /

    @classmethod
    def hour_regex(cls) -> str:
        return rf"^({cls.common_regex(cls.hour_values)})$"  # values , - * /

    @classmethod
    def day_of_month_regex(cls) -> str:
        return (
            rf"^({cls.common_regex(cls.month_of_day_values)}|\?|L|LW|{cls.month_of_day_values}W)$"
            # values , - * / ? L W
        )

    @classmethod
    def month_regex(cls):
        return rf"^({cls.common_regex(cls.month_values)})$"  # values , - * /

    @classmethod
    def day_of_week_regex(cls):
        range_list = cls.list_range_regex(cls.day_of_week_values)
        return rf"^({range_list}|\*|\?|{cls.day_of_week_values}L|L|L-[1-7]|{cls.day_of_week_hash})$"
        # values , - * ? L #

    @classmethod
    def year_regex(cls):
        return rf"^({cls.common_regex(cls.year_values)})$"  # values , - * /
