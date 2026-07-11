data "archive_file" "scheduler_lambda_zip" {
  type        = "zip"
  source_file = "${path.module}/../lambda/scheduler.py"
  output_path = "${path.module}/scheduler.zip"
}

resource "aws_lambda_function" "nonprod_scheduler" {
  function_name = "nonprod-scheduler"
  role          = aws_iam_role.scheduler_lambda_role.arn
  handler       = "scheduler.lambda_handler"
  runtime       = "python3.12"
  timeout       = 15

  filename         = data.archive_file.scheduler_lambda_zip.output_path
  source_code_hash = data.archive_file.scheduler_lambda_zip.output_base64sha256

  environment {
    variables = {
      SNS_TOPIC_ARN          = aws_sns_topic.scheduler_notifications.arn
      ENVIRONMENT_TAG_VALUES = "dev,test,qa"
    }
  }
}