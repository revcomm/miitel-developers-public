resource "aws_iam_policy" "genesys_example_policy" {
  name        = var.policy_name
  description = "An IAM policy for S3"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "s3:PutObject",
          "s3:GetEncryptionConfiguration",
          "s3:GetBucketLocation",
          "s3:PutObjectAcl"
        ]
        Resource = [
          "arn:aws:s3:::*/*",
        ]
      }
    ]
  })
}

resource "aws_iam_role" "genesys_example_role" {
  name = var.role_name
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Principal = {
          AWS = "arn:aws:iam::765628985471:root" # https://help.mypurecloud.com/articles/create-iam-resources-for-aws-s3-bucket/
        }
        Action = "sts:AssumeRole"
        Condition = {
          StringEquals = {
            "sts:ExternalId" = var.genesys_cloud_organization_id
          }
        }
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "genesys_example_attachment" {
  role       = aws_iam_role.genesys_example_role.name
  policy_arn = aws_iam_policy.genesys_example_policy.arn
}