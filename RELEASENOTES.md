# Release History

### v1.1.9 [2024-02-01]

- Fixes;
  - [Does not support "last day of the week" suffixes](https://github.com/grumBit/aws_cron_expression_validator/issues/12#issuecomment-1920567609)

### v1.1.8 [2024-02-01]

- Fixes;
  - [Does not support "last Wednesday of the month" syntax](https://github.com/grumBit/aws_cron_expression_validator/issues/12)
  - [Does not support lists that include slashes](https://github.com/grumBit/aws_cron_expression_validator/issues/13)

### v1.1.6 [2023-05-17]

- New;
  - Add these project release notes

### v1.1.3 [2023-05-17]

- Fixes;
  - [Year checking is incorrectly allowing ? and L](https://github.com/grumBit/aws_cron_expression_validator/issues/7)

### v1.1.2 [2023-05-15]

- Fixes;
  - [It should be possible to precede a slash with a range](https://github.com/grumBit/aws_cron_expression_validator/issues/6#issuecomment-1547031279)

### v1.0.10 to v1.0.11 [2023-03-07]

- New;
  - Adds community standards documentation suggested by GitHub. _No functional changes_

### v1.0.9 [2023-03-07]

- Fixes;
  - [Address security alert from dependabot regarding a ReDoS vulnerability](https://github.com/grumBit/aws_cron_expression_validator/pull/4) in svnurl.py when running unit tests. _NB: The vulnerability only related to unit testing. The aws-cron-expression-validator package itself was not impacted._

### v1.0.8 [2022-10-08]

- New;
  - Adds exceptions for each field (e.g. `AWSCronExpressionMinuteError`).

### v1.0.7 [2023-03-04]

- New;
  - [Relaxes Python language dependency from v3.9 to v3.7](https://github.com/grumBit/aws_cron_expression_validator/issues/1#issuecomment-1265588982). _No functional changes_

### v1.0.6 [2023-09-29]

- Fixes;
  - [Cron does not correctly validate CloudWatch expressions where the minutes field contains a /](https://github.com/grumBit/aws_cron_expression_validator/issues/1)

### v1.0.0 to v1.0.4 [2023-09-10]

- Internal non-functional changes;
  - Relax Python language dependency from v3.9 to v3.7.
  - Code linting.
  - Fix PyPI link to source.
  - Additional automated CI/CD testing.
  - Updated docs
