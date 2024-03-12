# Outgoing Webhook to BigQuery API test

## Prerequisites / 必要条件

Install serverless framework (version3)

```sh
npm install -g serverless@3
```

please refer: <https://www.serverless.com/framework/docs/getting-started>

## Deploy / デプロイ手順

### Initial setup for domain / ドメインおよび証明書の準備

```sh
SLS_DEBUG=* npx sls create-cert --stage dev --aws-profile <your-profile> # Certification
SLS_DEBUG=* npx sls create_domain --stage dev --aws-profile <your-profile> # Domain
```

### Deploy to AWS / AWSへのデプロイ

```sh
SLS_DEBUG=* npx sls deploy --stage dev --aws-profile <your-profile>
```

## Local Development / ローカルで開発する場合

```sh
STAGE=local docker compose up --build
```

Then, you can access api via `http://localhost:5000/api/v1/bigquery/add`
