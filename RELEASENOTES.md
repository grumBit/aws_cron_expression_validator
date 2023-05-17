
# Release History

## v1.1.4

- New;
  - Add these project release notes

## v1.1.3

- Fixes;
  - [Year checking is incorrectly allowing ? and L](https://github.com/grumBit/aws_cron_expression_validator/issues/7)

## v1.1.2

- Fixes;
  - [It should be possible to precede a slash with a range](https://github.com/grumBit/aws_cron_expression_validator/issues/6#issuecomment-1547031279)

## v1.0.10 to v1.0.11

- New;
  - Adds community standards documentation suggested by GitHub.  _No functional changes_

## v1.0.9

- Fixes;
  - [Address security alert from dependabot regarding a ReDoS vulnerability](https://github.com/grumBit/aws_cron_expression_validator/pull/4) in svnurl.py when running unit tests. _NB: The vulnerability only related to unit testing. The aws-cron-expression-validator package itself was not impacted._

## v1.0.8

- New;
  - Adds exceptions for each field (e.g. `AWSCronExpressionMinuteError`).

## v1.0.7

- New;
  - [Relaxes Python language dependency from v3.9 to v3.7](https://github.com/grumBit/aws_cron_expression_validator/issues/1#issuecomment-1265588982). _No functional changes_

## v1.0.6

- Fixes;
  - [Cron does not correctly validate CloudWatch expressions where the minutes field contains a /](https://github.com/grumBit/aws_cron_expression_validator/issues/1)

## v1.0.0 to v1.0.5

- Internal non-functional changes;
  - Relax Python language dependency from v3.9 to v3.7.
  - Code linting.
  - Fix PyPI link to source.
  - Additional automated CI/CD testing.
  - Updated docs
