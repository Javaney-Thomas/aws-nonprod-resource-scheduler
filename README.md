# Automated AWS Non-Production Scheduler

## Overview

This project is an event-driven AWS automation platform built with Terraform and Python that automatically starts and stops non-production EC2 instances based on a schedule.

The goal is to reduce unnecessary cloud spending by ensuring development, test, and QA infrastructure does not remain running outside business hours.

The entire infrastructure is provisioned using Infrastructure as Code (Terraform) and follows AWS security best practices using IAM least privilege.

---
## Architecture

![AWS Automated Non-Production Scheduler Architecture](diagrams/nonprod-scheduler.png)

## Business Problem

Development and testing environments are frequently left running overnight and during weekends.

Although they are not serving production traffic, these resources continue to generate AWS charges.

For organizations with dozens or hundreds of development servers, this becomes a significant source of unnecessary cloud spending.

---

## Solution

This solution automatically:

- Finds EC2 instances tagged as development resources
- Starts or stops them on a schedule
- Sends notifications through Amazon SNS
- Records execution logs in CloudWatch
- Uses IAM least privilege permissions
- Is fully deployed using Terraform

---

## How it Works

EventBridge Scheduler

↓

AWS Lambda (Python)

↓

EC2 API

↓

Start / Stop Tagged Instances

↓

SNS Notification

↓

CloudWatch Logs

---

## AWS Services Used

- AWS Lambda
- Amazon EC2
- Amazon EventBridge Scheduler
- Amazon SNS
- Amazon CloudWatch
- AWS IAM

---

## Terraform Concepts

- Providers
- Resources
- Variables
- Outputs
- Data Sources
- State Management

---

## Technologies

- Terraform
- Python
- boto3
- Git
- AWS CLI

---

## Project Structure

terraform-nonprod-scheduler/

├── lambda/

├── terraform/

├── screenshots/

├── docs/

└── README.md

---

## Features

- Infrastructure as Code
- Scheduled automation
- Least privilege IAM
- Configurable environment tags
- CloudWatch logging
- SNS notifications
- Version controlled with Git

---

## Lessons Learned

During this project I learned how multiple AWS services integrate to build a real-world cloud automation solution including:

- Infrastructure as Code with Terraform
- IAM Roles and Policies
- Event-driven architecture
- AWS Lambda deployment
- EC2 automation
- CloudWatch logging
- Git version control

---

## Future Improvements

- Support RDS start/stop
- Slack notifications
- Cost estimation reporting
- Multi-account support
- Terraform modules
- CI/CD deployment using GitHub Actions
