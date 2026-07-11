resource "aws_sns_topic" "scheduler_notifications" {
  name = "nonprod-scheduler-notifications"
}