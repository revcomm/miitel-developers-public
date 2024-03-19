# Outgoing Webhook to Salesforce Custom Items using ChatGPT

## !!!Attention

- When you use this repository, please replace settings below in serverless framework
  - service name
  - domain name
  - api key name

## Overview

Outgoing Webhook を API Gateway ＋ Lambda（FastAPI）で受け付けて、それを SQS+Lambda の構成に投げる構成。
API Gateway の制約にて、30秒以内で処理を負えないといけないので、長時間処理のかかる可能性のあるもの（今回は ChatGPT へのリクエスト）などはSQS配下のLambda（最長15分）に処理してもらう。

## Prerequisites / 必要条件

Install serverless framework (version3)

```sh
npm install -g serverless@3
```

please refer: <https://www.serverless.com/framework/docs/getting-started>

## Deploy / デプロイ手順

### create .env.dev / .env ファイルの準備

```sh
cp app/envs/.env.example app/envs/.env.dev
# 必要に応じて中身を編集
```

### Initial setup for domain / ドメインおよび証明書の準備

```sh
 # Certification
SLS_DEBUG=* npx sls create-cert --stage dev --aws-profile <your-profile>
 # Domain
SLS_DEBUG=* npx sls create_domain --stage dev --aws-profile <your-profile>
```

### Deploy to AWS / AWSへのデプロイ

```sh
SLS_DEBUG=* npx sls deploy --stage dev --aws-profile <your-profile>
```

## Local Development / ローカルで開発する場合

if you want to wake up api in local.

```sh
STAGE=local docker compose up --build
```

Then, you can access api via `http://localhost:5000/api/v1/gpt-custom/add`

### folder structures

```sh
.
├── Dockerfile # ローカルで開発するときのDockerfile
├── docker-compose.yml # ローカル開発用
├── README.md
├── app # fast api in lambda Outgoing Webhook を受け付けるAPI
│   ├── __init__.py
│   ├── api
│   ├── common
│   ├── config
│   ├── envs
│   ├── exception_handler.py
│   ├── log.py
│   ├── main.py
│   ├── router.py
│   └── settings.py
├── gpt_app # SQS配下のLambda。長時間動作する可能性のあるものはここで。
│   ├── Dockerfile
│   ├── __init__.py
│   ├── func_items.py
│   ├── handler.py
│   └── requirements.txt
├── package.json
├── pyproject.toml
├── requirements.txt
├── send_api_request.py # APIにリクエストを投げる動作検証用スクリプト
├── send_sqs_request.py # SQSにリクエストを投げる動作検証用スクリプト
├── serverless.yml
└── yarn.lock
```
