variable "role_name" {
  description = "The name of the IAM role for S3"
  type        = string
  default     = "genesys-example-role"
}

variable "policy_name" {
  description = "The name of the IAM policy for S3"
  type        = string
  default     = "genesys-example-policy"
}

variable "bucket_name" {
  description = "The name of the S3 bucket for storing Genesys audio files"
  type        = string
  default     = "genesys-example-bucket"
}

variable "genesys_cloud_organization_id" {
  description = "The Genesys Cloud organization ID"
  type        = string
  default     = "{genesys-cloud-organization-id}"
}

variable "genesys_cloud_token_url" {
  description = "URL to obtain Genesys Cloud token. The Auth Server location may vary (e.g., .jp, .com). Please refer to the documentation for details: https://developer.genesys.cloud/platform/api/"
  type        = string
  default     = "https://login.mypurecloud.jp/oauth/token"
}

variable "lambda_exec_role_name" {
  description = "Role of lambda function"
  type        = string
  default     = "genesys-example-lambda-exec-role"
}

variable "lambda_policy_name" {
  description = "Policy of lambda function"
  type        = string
  default     = "genesys-example-lambda-policy"
}

variable "lambda_function_name" {
  description = "Name of lambda function"
  type        = string
  default     = "genesys-example-lambda-function"
}

variable "lambda_miitel_incoming_webhook_url" {
  description = "URL for miitel's incoming webhook"
  type        = string
  default     = "https://{miitel-incoming-webhook-url}"
}