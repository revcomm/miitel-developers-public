resource "aws_iam_role" "lambda_role" {
  name = var.lambda_exec_role_name

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
        Action = "sts:AssumeRole"
      }
    ]
  })
}

resource "aws_iam_policy" "lambda_policy" {
  name        = var.lambda_policy_name
  description = "Basic execution policy for Lambda"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "s3:GetObject",
          "s3:ListBucket",
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ]
        Resource = [
          "${aws_s3_bucket.genesys_example_bucket.arn}",
          "${aws_s3_bucket.genesys_example_bucket.arn}/*"
        ]
      },
      {
        Effect = "Allow"
        Action = [
          "secretsmanager:GetSecretValue"
        ]
        Resource = aws_secretsmanager_secret.genesys_example_client_credentials.arn
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "lambda_basic_execution" {
  role       = aws_iam_role.lambda_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

resource "null_resource" "install_dependencies" {
  provisioner "local-exec" {
    command = <<EOT
      rm -rf ${path.module}/deployment_package
      mkdir -p ${path.module}/deployment_package
      pip install -r ${path.module}/src/requirements.txt -t ${path.module}/deployment_package
      cp -r ${path.module}/src/* ${path.module}/deployment_package/
    EOT
  }

  triggers = {
    src_hash = md5(join("", [
      for file in fileset("${path.module}/src", "**/*")
      : filemd5("${path.module}/src/${file}")
    ]))
  }
}

data "archive_file" "lambda_zip" {
  type        = "zip"
  source_dir  = "${path.module}/deployment_package"
  output_path = "${path.module}/zip/lambda_function.zip"

  depends_on = [null_resource.install_dependencies]
}

resource "aws_lambda_function" "genesys_example_lambda" {
  function_name = var.lambda_function_name
  runtime       = "python3.12"
  role          = aws_iam_role.lambda_role.arn
  handler       = "lambda_function.lambda_handler"
  timeout       = 300
  memory_size   = 512

  source_code_hash = data.archive_file.lambda_zip.output_base64sha256

  filename = data.archive_file.lambda_zip.output_path

  environment {
    variables = {
      GENESYS_CLOUD_TOKEN_URL     = var.genesys_cloud_token_url
      MIITEL_INCOMING_WEBHOOK_URL = var.lambda_miitel_incoming_webhook_url
    }
  }
}

resource "aws_iam_role_policy_attachment" "lambda_attach" {
  role       = aws_iam_role.lambda_role.name
  policy_arn = aws_iam_policy.lambda_policy.arn
}

resource "aws_lambda_permission" "allow_s3" {
  statement_id  = "AllowS3Invoke"
  action        = "lambda:InvokeFunction"
  function_name = var.lambda_function_name
  principal     = "s3.amazonaws.com"
  source_arn    = aws_s3_bucket.genesys_example_bucket.arn
}