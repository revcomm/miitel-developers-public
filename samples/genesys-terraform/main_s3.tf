resource "aws_s3_bucket" "genesys_example_bucket" {
  bucket = var.bucket_name
}

resource "aws_s3_bucket_notification" "bucket_notification" {
  bucket = var.bucket_name

  lambda_function {
    lambda_function_arn = aws_lambda_function.genesys_example_lambda.arn
    events              = ["s3:ObjectCreated:*"]

    filter_suffix = ".json"
  }
}