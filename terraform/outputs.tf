output "lambda_function_name" {
  description = "Name of the scheduler Lambda function"
  value       = aws_lambda_function.nonprod_scheduler.function_name
}

output "lambda_function_arn" {
  description = "ARN of the scheduler Lambda function"
  value       = aws_lambda_function.nonprod_scheduler.arn
}

output "sns_topic_arn" {
  description = "ARN of the SNS topic"
  value       = aws_sns_topic.scheduler_notifications.arn
}

output "iam_role_arn" {
  description = "ARN of the Lambda IAM role"
  value       = aws_iam_role.scheduler_lambda_role.arn
}