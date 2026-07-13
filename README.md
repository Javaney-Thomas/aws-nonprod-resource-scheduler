# CloudShift

![AWS](https://img.shields.io/badge/AWS-Cloud-orange)
![Terraform](https://img.shields.io/badge/Terraform-IaC-623CE4)
![Python](https://img.shields.io/badge/Python-3.x-blue)
![License](https://img.shields.io/badge/License-MIT-green)

## Automated Non-Production Resource Scheduler for AWS

CloudShift is a cloud automation platform that automatically starts and stops non-production AWS resources based on business schedules, reducing unnecessary cloud costs while maintaining operational safety.

This project is the first in a portfolio focused on cloud automation, cloud security, FinOps, DevOps, and enterprise AWS architecture.

Built with:

- AWS Lambda
- Amazon EventBridge Scheduler
- Terraform
- AWS IAM
- Amazon SNS
- Amazon CloudWatch

---

# Table of Contents

- Business Problem
- Business Value
- Architecture
- Solution Overview
- Request Flow
- AWS Services Used
- Features
- Security Considerations
- Cost Savings Example
- Why Terraform?
- Deployment
- Project Structure
- Lessons Learned
- Key Design Decisions
- Future Improvements

---

# Business Problem

Development, testing, and staging environments frequently remain powered on outside business hours.

Organizations often leave EC2 and RDS resources running:

- Overnight
- Weekends
- Holidays

These idle resources continue generating cloud costs despite having no active users.

CloudShift automates scheduling to reduce wasted compute time while preserving developer productivity and improving cloud cost governance.

---

# Business Value

CloudShift helps organizations:

- Reduce non-production compute costs
- Eliminate manual shutdown procedures
- Standardize scheduling policies
- Improve operational consistency
- Increase cloud cost visibility
- Support FinOps initiatives
- Reduce operational overhead through automation

---

# Architecture

<p align="center">
  <img src="diagrams/nonprod-scheduler.png" width="900" alt="AWS Automated Non-Production Scheduler Architecture">
</p>

---

# Solution Overview

CloudShift uses Amazon EventBridge Scheduler to trigger AWS Lambda functions according to predefined business schedules.

The Lambda function:

1. Discovers EC2 resources using AWS tags.
2. Determines the desired resource state.
3. Starts or stops matching instances.
4. Publishes notifications using Amazon SNS.
5. Records execution details in Amazon CloudWatch Logs.

---

# Request Flow

1. Amazon EventBridge Scheduler triggers the AWS Lambda function at the configured time.

2. AWS Lambda discovers EC2 instances tagged for automated scheduling.

3. The function evaluates whether the resources should be started or stopped.

4. Using boto3, Lambda communicates with the Amazon EC2 API.

5. Execution details are written to Amazon CloudWatch Logs.

6. Amazon SNS sends a notification confirming the completed operation.

---

# AWS Services Used

| AWS Service | Purpose |
|-------------|---------|
| AWS Lambda | Executes the scheduling logic |
| Amazon EventBridge Scheduler | Triggers automation on a schedule |
| Amazon EC2 | Target compute resources |
| Amazon SNS | Sends notifications after execution |
| Amazon CloudWatch | Centralized logging and monitoring |
| AWS IAM | Provides least-privilege access control |
| Terraform | Infrastructure as Code provisioning |

---

# Features

- Infrastructure as Code with Terraform
- Scheduled EC2 automation
- Event-driven architecture
- Least-privilege IAM permissions
- Tag-based resource management
- Amazon SNS notifications
- Amazon CloudWatch logging
- Modular infrastructure
- Version-controlled deployment using Git

---

# Security Considerations

CloudShift follows AWS security best practices by implementing:

- IAM least-privilege policies
- No hardcoded AWS credentials
- Infrastructure managed entirely through Terraform
- Centralized audit logging using CloudWatch
- Tag-based resource selection to prevent unintended operations
- Separation of infrastructure and application code

---

# Cost Savings Example

Development environments frequently run continuously even though engineers only use them during business hours.

Example:

| Schedule | Runtime |
|----------|---------:|
| 24/7 | ~730 hours/month |
| Business Hours | ~260 hours/month |

Estimated runtime reduction:

**Approximately 64%**

> Actual cost savings depend on AWS pricing, resource types, and workload utilization.

---

# Why Terraform?

Terraform was selected because it provides:

- Repeatable infrastructure deployments
- Version-controlled infrastructure
- Environment consistency
- Simplified rollback capability
- Infrastructure documentation
- Cloud-provider portability
- Scalable Infrastructure as Code practices

---

# Deployment

## Prerequisites

- AWS CLI configured
- Terraform installed
- Python 3.x
- Appropriate AWS permissions

## Deploy

```bash
git clone https://github.com/<your-username>/terraform-nonprod-scheduler.git

cd terraform-nonprod-scheduler/terraform

terraform init

terraform plan

terraform apply
```

Tag EC2 instances that should be managed automatically:

```text
AutoSchedule=true
```

---

# Project Structure

```text
terraform-nonprod-scheduler/
│
├── diagrams/
│   ├── nonprod-scheduler.drawio
│   ├── nonprod-scheduler.png
│   └── nonprod-scheduler.svg
│
├── lambda/
│   └── scheduler.py
│
├── terraform/
│   ├── iam.tf
│   ├── lambda.tf
│   ├── scheduler.tf
│   ├── sns.tf
│   ├── variables.tf
│   ├── outputs.tf
│   └── provider.tf
│
├── screenshots/
│
└── README.md
```

---

# Lessons Learned

Building CloudShift strengthened my understanding of:

- Infrastructure as Code using Terraform
- AWS Lambda development and deployment
- IAM Roles and Least Privilege
- Event-driven cloud architecture
- Amazon EventBridge Scheduler
- Amazon EC2 automation
- CloudWatch monitoring and logging
- AWS service integration
- Cloud cost optimization concepts
- Git version control and project organization

---

# Key Design Decisions

Several architectural decisions were made to keep the solution scalable, secure, and cost-effective.

- Terraform was selected to provide repeatable Infrastructure as Code deployments.
- AWS Lambda eliminates the need for continuously running compute resources.
- Amazon EventBridge Scheduler provides reliable serverless scheduling.
- Amazon SNS delivers operational visibility through notifications.
- Amazon CloudWatch centralizes monitoring and troubleshooting.
- IAM least-privilege policies reduce security risk.
- Tag-based discovery allows flexible resource management without modifying code.

---

# Future Improvements

- Support Amazon RDS scheduling
- Temporary scheduling overrides for developers
- Slack and Microsoft Teams notifications
- AWS Cost Explorer integration
- Cost savings dashboard
- Multi-account scheduling support
- GitHub Actions CI/CD pipeline
- Terraform modules
- Web-based management dashboard
- Automated tagging policies

---

# Resume Highlight

> Developed **CloudShift**, a cloud automation platform using Terraform, AWS Lambda, EventBridge Scheduler, Amazon SNS, and CloudWatch to automate non-production EC2 scheduling, reducing eligible compute runtime by approximately **64%** while implementing Infrastructure as Code, event-driven automation, and AWS security best practices.