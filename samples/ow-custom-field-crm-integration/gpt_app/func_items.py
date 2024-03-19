def get_custom_integration_functions(items: list):
    item_properties = {}
    for item in items:
        # items.properties に追加する。dict形式で追加する。
        item_properties[item["name"]] = {
            "type": "string",
            "description": item["description"],
        }

    return [
        {
            "name": "create_custom_integration",
            "description": "Custom integration function to CRM items",
            "parameters": {
                "type": "object",
                "properties": item_properties,
                "required": [item["name"] for item in items],
            },
        },
    ]
