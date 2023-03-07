![PyPI](https://img.shields.io/pypi/v/aws_cron_expression_validator)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/aws_cron_expression_validator)
![GitHub all releases](https://img.shields.io/github/downloads/grumbit/aws_cron_expression_validator/total)
[![GitHub license](https://img.shields.io/github/license/grumbit/aws_cron_expression_validator)](https://github.com/grumbit/aws_cron_expression_validator/blob/master/LICENSE)
![PyPI - Implementation](https://img.shields.io/pypi/implementation/aws_cron_expression_validator)
![PyPI - Wheel](https://img.shields.io/pypi/wheel/aws_cron_expression_validator)
![PyPI - Status](https://img.shields.io/pypi/status/aws_cron_expression_validator)
[![GitHub issues](https://img.shields.io/github/issues/grumbit/aws_cron_expression_validator)](https://github.com/grumbit/aws_cron_expression_validator/issues)
[![GitHub forks](https://img.shields.io/github/forks/grumbit/aws_cron_expression_validator)](https://github.com/grumbit/aws_cron_expression_validator/network)
[![GitHub stars](https://img.shields.io/github/stars/grumbit/aws_cron_expression_validator)](https://github.com/grumbit/aws_cron_expression_validator/stargazers)

# AWSCronExpressionValidator

Validates these [AWS EventBridge cron expressions](https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-create-rule-schedule.html#eb-cron-expressions), which are similar to, but not compatible with Unix style cron expressions;

| Field        | Values          | Wildcards     |
| :----------: | :-------------: | :-----------: |
| Minute       | 0-59            | , - * /       |
| Hour         | 0-23            | , - * /       |
| Day-of-month | 1-31            | , - * ? / L W |
| Month        | 1-12 or JAN-DEC | , - * /       |
| Day-of-week  |  1-7 or SUN-SAT | , - * ? L #   |
| Year         | 1970-2199       | , - * /       |

This was inspired by Niloy Chakraborty's [AWSCronValidator.py](https://gist.github.com/ultrasonex/e1fdb8354408a56df91aa4902d17aa6a) project.

# Installing

To install the library run;

```bash
pip install aws-cron-expression-validator
```

# Usage

```python
from aws_cron_expression_validator.validator import AWSCronExpressionValidator, AWSCronExpressionMinuteError

my_expression = "0 180 ? * MON-FRI *"
try:
    AWSCronExpressionValidator.validate(my_expression)
except AWSCronExpressionMinuteError:
    print(f"Oh no! My expression has an invalid minute field: {e}")
except ValueError as e:
    print(f"Oh no! My expression was invalid: {e}")
```
