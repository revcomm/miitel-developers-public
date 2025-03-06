# Genesys Example Project

This project provides Terraform scripts to integrate Genesys Cloud with AWS services.

## Environment

- python 3.12.5
- pip 24.2
- Terraform v1.9.2

## Directory Structure

- `main_iam.tf`: Definition of IAM roles and policies
- `main_lambda.tf`: Definition of Lambda functions
- `main_s3.tf`: Definition of S3 buckets
- `main_secret_manager.tf`: Definitions of Secrets Manager
- `outputs.tf`: Definitions of output variables
- `provider.tf`: Provider configuration
- `variables.tf`: Definitions of input variables
- `src/`: Source code

## Setup

1. Install the required providers.
    ```sh
    terraform init
    ```

2. Check the Terraform plan.
    ```sh
    terraform plan
    ```

3. Apply Terraform to create resources.
    ```sh
    terraform apply
    ```

## Infrastructure Resources

### IAM

- `main_iam.tf` defines IAM roles and policies for accessing the S3 bucket.
  - `aws_iam_policy.genesys_example_policy`: Policy allowing access to the S3 bucket
  - `aws_iam_role.genesys_example_role`: IAM role to attach the above policy

### Lambda

- `main_lambda.tf` defines the Lambda function, its execution role, and policies.
  - `aws_iam_role.lambda_role`: Execution role for the Lambda functions
  - `aws_iam_policy.lambda_policy`: IAM policy for the Lambda functions
  - `aws_lambda_function.genesys_example_lambda`: Definition of the Lambda functions
  - `null_resource.install_dependencies`: Dependencies for the Lambda functions
  - `data.archive_file.lambda_zip`: Package of the Lambda function source codes into a ZIP archive

### S3

- `main_s3.tf` defines the S3 bucket for storing Genesys audio files.
  - `aws_s3_bucket.genesys_example_bucket`: S3 bucket for storing Genesys audio files

### Secrets Manager

- `main_secret_manager.tf` defines the Secrets Manager for storing Genesys Cloud client ID and client secret.
  - `aws_secretsmanager_secret.genesys_example_secret`: Secrets Manager secret for storing Genesys Cloud client ID and client secret

## Variables

- `role_name`: Name of the IAM role
- `policy_name`: Name of the IAM policy
- `bucket_name`: Name of the S3 bucket
- `genesys_cloud_organization_id`: Organization ID of Genesys Cloud
- `lambda_exec_role_name`: Name of the Lambda execution role
- `lambda_policy_name`: Name of the Lambda policy
- `lambda_function_name`: Name of the Lambda function
- `genesys_cloud_token_url`: Token URL of Genesys Cloud
- `lambda_miitel_incoming_webhook_url`: Incoming Webhook URL of MiiTel