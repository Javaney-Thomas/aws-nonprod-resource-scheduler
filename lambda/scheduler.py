import json
import logging
import os
from typing import Any

import boto3
from botocore.exceptions import ClientError


logger = logging.getLogger()
logger.setLevel(logging.INFO)

ec2 = boto3.client("ec2")
sns = boto3.client("sns")

VALID_ACTIONS = {"start", "stop"}


def lambda_handler(event: dict[str, Any], context: Any) -> dict[str, Any]:
    """Start or stop non-production EC2 instances based on the event action."""

    action = str(event.get("action", "stop")).lower()
    topic_arn = os.environ["SNS_TOPIC_ARN"]
    environment_tags = get_environment_tags()

    logger.info(
        "Scheduler invoked with action=%s and environment_tags=%s",
        action,
        environment_tags,
    )

    if action not in VALID_ACTIONS:
        message = f"Invalid action '{action}'. Expected 'start' or 'stop'."
        logger.error(message)
        raise ValueError(message)

    try:
        instance_ids = find_nonprod_instance_ids(action, environment_tags)

        if not instance_ids:
            message = (
                f"No eligible non-production EC2 instances found "
                f"for action: {action}"
            )
            logger.info(message)
            publish_message(topic_arn, message)

            return build_response(200, message)

        perform_instance_action(action, instance_ids)

        past_tense = "Started" if action == "start" else "Stopped"
        message = (
            f"{past_tense} {len(instance_ids)} non-production "
            f"EC2 instance(s): {instance_ids}"
        )

        logger.info(message)
        publish_message(topic_arn, message)

        return build_response(200, message)

    except ClientError as error:
        error_message = (
            f"AWS API error while attempting to {action} "
            f"non-production EC2 instances: {error}"
        )

        logger.exception(error_message)

        try:
            publish_message(topic_arn, error_message)
        except ClientError:
            logger.exception("Unable to publish failure notification to SNS")

        raise


def get_environment_tags() -> list[str]:
    """Read the managed environment tag values from an environment variable."""

    raw_tags = os.getenv("ENVIRONMENT_TAG_VALUES", "dev,test,qa")

    tags = [
        tag.strip()
        for tag in raw_tags.split(",")
        if tag.strip()
    ]

    if not tags:
        raise ValueError("ENVIRONMENT_TAG_VALUES must contain at least one tag")

    return tags


def find_nonprod_instance_ids(
    action: str,
    environment_tags: list[str],
) -> list[str]:
    """Find EC2 instances eligible for the requested action."""

    required_state = "running" if action == "stop" else "stopped"

    filters = [
        {
            "Name": "tag:Environment",
            "Values": environment_tags,
        },
        {
            "Name": "instance-state-name",
            "Values": [required_state],
        },
    ]

    instance_ids: list[str] = []

    paginator = ec2.get_paginator("describe_instances")

    for page in paginator.paginate(Filters=filters):
        for reservation in page.get("Reservations", []):
            for instance in reservation.get("Instances", []):
                instance_ids.append(instance["InstanceId"])

    logger.info(
        "Found %d instance(s) in state=%s",
        len(instance_ids),
        required_state,
    )

    return instance_ids


def perform_instance_action(
    action: str,
    instance_ids: list[str],
) -> None:
    """Start or stop the supplied EC2 instances."""

    logger.info(
        "Performing action=%s on instance_ids=%s",
        action,
        instance_ids,
    )

    if action == "stop":
        ec2.stop_instances(InstanceIds=instance_ids)
    else:
        ec2.start_instances(InstanceIds=instance_ids)


def publish_message(topic_arn: str, message: str) -> None:
    """Publish an execution summary to SNS."""

    sns.publish(
        TopicArn=topic_arn,
        Subject="Non-Prod Scheduler Notification",
        Message=message,
    )

    logger.info("SNS notification published successfully")


def build_response(status_code: int, message: str) -> dict[str, Any]:
    """Create a consistent Lambda response."""

    return {
        "statusCode": status_code,
        "body": json.dumps(message),
    }