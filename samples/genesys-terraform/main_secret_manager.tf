resource "aws_secretsmanager_secret" "genesys_example_client_credentials" {
  name        = "GENESYS_CLOUD_CREDENTIALS"
  description = "This is an example genesys credentials"
}

resource "aws_secretsmanager_secret_version" "genesys_example_client_credentials_version" {
  secret_id = aws_secretsmanager_secret.genesys_example_client_credentials.id
  secret_string = jsonencode({
    client_id     = "GENESYS_CLOUD_CLIENT_ID"     # AWSマネジメントコンソールから値を入力 / Enter the value from the AWS management console
    client_secret = "GENESYS_CLOUD_CLIENT_SECRET" # AWSマネジメントコンソールから値を入力 / Enter the value from the AWS management console
  })
}