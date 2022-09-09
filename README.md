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
from aws_cron_expression_validator.validator import AWSCronExpressionValidator

my_expression = "0 18 ? * MON-FRI *"
try:
    AWSCronExpressionValidator.validate(my_expression)
except ValueError as e:
    print(f"Oh no! My expression was invalid: {e}")
```
