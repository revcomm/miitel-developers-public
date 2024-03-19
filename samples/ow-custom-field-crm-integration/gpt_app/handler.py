import json
import os

import requests
import simple_salesforce
from func_items import get_custom_integration_functions
from openai import OpenAI


def lambda_handler(event, context):
    body = json.loads(event["Records"][0]["body"])

    # Salesforceのデータを取得する
    sf = simple_salesforce.Salesforce(
        username=os.environ["SF_USER"],
        password=os.environ["SF_PASSWORD"],
        security_token=None,
        organizationId="",
        domain=os.environ["SF_DOMAIN"],
    )
    tel_number = body["tel_number"]

    # 電話番号からリードを取得する
    lead = sf.query(
        f"SELECT Id, Name, NextAction__c, ExpectedValue__c FROM Lead WHERE Phone = '{tel_number}'"
    )
    lead_id = lead["records"][0]["Id"]

    messages = []
    for phrase in body["phrases"]:
        messages.append({"role": "user", "content": phrase["phrase"]})

    messages.append(
        {
            "role": "user",
            "content": "このやり取りは、営業担当と顧客の間で行われた電話の録音です。こちらを参考に、指定した項目に情報を入力してください。",
        }
    )

    openai_client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    items = [
        {
            "name": "NextAction__c",
            "description": "ネクストアクションの内容",
        },
        {
            "name": "ExpectedValue__c",
            "description": "お客様が MiiTel に期待している価値や課題のヒアリング結果",
        },
    ]
    response = openai_client.chat.completions.create(
        model="gpt-4",
        messages=messages,
        functions=get_custom_integration_functions(items),
        function_call="auto",
    )
    response_message = response.choices[0].message
    response_text = response_message.function_call

    if response_text:
        response_text = json.loads(response_text.arguments)
        # リードの項目に値を入力する
        sf.Lead.update(
            lead_id,
            {
                "NextAction__c": response_text["NextAction__c"],
                "ExpectedValue__c": response_text["ExpectedValue__c"],
            },
        )
        return response_text
    else:
        return response_message.model_dump_json()
