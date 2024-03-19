import json
import uuid

import requests

# header
headers = {
    "Content-Type": "application/json",
    "X-API-KEY": "<your-api-key>",
}

call_id = str(uuid.uuid4())

# body
body = {
    "call": {
        "id": call_id,
        "tenant_code": "miitel-test",
        "details": [
            {
                "id": call_id,
                "dial_starts_at": "2022-12-09T03:41:48+00:00",
                "dial_answered_at": "2022-12-09T03:41:54+00:00",
                "dial_ends_at": "2022-12-09T03:42:17+00:00",
                "queueing_starts_at": None,
                "queueing_answered_at": None,
                "queueing_ends_at": None,
                "call_type": "OUTGOING_CALL",
                "circuit_number": "050-0000-0000",
                "circuit_name": "050-0000-0000",
                "from_number": None,
                "to_number": "09000001111",
                "previous_id": None,
                "dtmf": "0",
                "analysis": {
                    "score": 313.3515187539091,
                    "tlr": 0.8095,
                    "rally_count": 5,
                    "overlap_count": 0,
                    "silence_count": 0,
                },
                "participants": [
                    {
                        "id": "0184f502-8b66-4ab1-10d3-34c0049a9100",
                        "from_to": "FROM",
                        "name": "鈴木 太郎",
                        "company_name": None,
                        "analysis": {
                            "f0": 116.8819,
                            "speechrate": 8.8416,
                            "variance": 22.803,
                            "filler_count": 2,
                            "positive_score": 0,
                            "negative_score": 0,
                        },
                    },
                    {
                        "id": "0184f502-8b66-1a28-3896-550ac23b8e34",
                        "from_to": "TO",
                        "name": None,
                        "company_name": None,
                        "analysis": {
                            "f0": 234.0116,
                            "speechrate": 6.3676,
                            "variance": None,
                            "filler_count": 5,
                            "positive_score": 0,
                            "negative_score": 0,
                        },
                    },
                ],
                "tags": [
                    {"created_by": "鈴木 太郎", "creator_type": "TENANT_USER", "value": "大項目①"},
                    {
                        "created_by": "鈴木 太郎",
                        "creator_type": "TENANT_USER",
                        "value": "詳細項目①",
                    },
                ],
                "comments": [
                    {
                        "created_at": "2022-12-09T04:45:13.732021+00:00",
                        "created_by": "鈴木 太郎",
                        "value": "コメント",
                    }
                ],
                "keywords": [
                    {
                        "starts_at": 2,
                        "participant_id": "0184f502-8b66-1a28-3896-550ac23b8e34",
                        "value": "みーてる",
                    },
                    {
                        "starts_at": 2,
                        "participant_id": "0184f502-8b66-1a28-3896-550ac23b8e34",
                        "value": "でんわ",
                    },
                ],
                "phrases": [
                    {
                        "participant_id": "0184f502-8b66-1a28-3896-550ac23b8e34",
                        "raw": [
                            {
                                "order": 1,
                                "phrase": "お世話になります。IP電話ミーテルの鈴木と申します。",
                                "phrase_nofiller": "お世話になります。IP電話ミーテルの鈴木と申します。",
                                "start_at": 2.16,
                                "end_at": 5.345,
                                "filler_num": 0,
                            },
                            {
                                "order": 3,
                                "phrase": "恐れ入ります、高橋様お手すきでいらっしゃいますか。",
                                "phrase_nofiller": "恐れ入ります、高橋様お手すきでいらっしゃいますか。",
                                "start_at": 6.835,
                                "end_at": 9.425,
                                "filler_num": 0,
                            },
                            {
                                "order": 4,
                                "phrase": "あっそうだったんですね。わかりました。また来週改めさしていただきます。",
                                "phrase_nofiller": "そうだったんですね。わかりました。また来週改めさしていただきます。",
                                "start_at": 13.39,
                                "end_at": 17.935,
                                "filler_num": 1,
                            },
                            {
                                "order": 6,
                                "phrase": "はい、よろしくお願いいたしますー。",
                                "phrase_nofiller": "よろしくお願いいたしますー。",
                                "start_at": 18.85,
                                "end_at": 20.745,
                                "filler_num": 1,
                            },
                        ],
                        "summary": [
                            {
                                "order": 0,
                                "phrase": "お電話ありがとうございます、MiiTelの田中です。先程は資料請求いただき、ありがとうございました。MiiTelにご興味をお持ちいただけたこと、大変嬉しく思います。",
                                "phrase_nofiller": "お電話ありがとうございます、MiiTelの田中です。先程は資料請求いただき、ありがとうございました。MiiTelにご興味をお持ちいただけたこと、大変嬉しく思います。",
                                "start_at": 2.16,
                                "end_at": 5.345,
                                "filler_num": None,
                            },
                            {
                                "order": 2,
                                "phrase": "それは良いタイミングですね。具体的に、MiiTelにどのような機能や価値を期待されていますか？",
                                "phrase_nofiller": "それは良いタイミングですね。具体的に、MiiTelにどのような機能や価値を期待されていますか？",
                                "start_at": 6.835,
                                "end_at": 9.425,
                                "filler_num": None,
                            },
                            {
                                "order": 4,
                                "phrase": "承知しました。MiiTelでは、コールログの分析やチームの活動の可視化を通じて、コミュニケーションの改善と透明性の向上をサポートします。また、営業チームのパフォーマンス管理にも役立つ機能を備えています。",
                                "phrase_nofiller": "承知しました。MiiTelでは、コールログの分析やチームの活動の可視化を通じて、コミュニケーションの改善と透明性の向上をサポートします。また、営業チームのパフォーマンス管理にも役立つ機能を備えています。",
                                "start_at": 13.39,
                                "end_at": 17.935,
                                "filler_num": None,
                            },
                            {
                                "order": 6,
                                "phrase": "まさにその通りです。こちらの機能を実際にご覧いただければと思います。Web会議を通じたデモンストレーションを設定させていただいてもよろしいでしょうか？",
                                "phrase_nofiller": "まさにその通りです。こちらの機能を実際にご覧いただければと思います。Web会議を通じたデモンストレーションを設定させていただいてもよろしいでしょうか？",
                                "start_at": 13.39,
                                "end_at": 17.935,
                                "filler_num": None,
                            },
                            {
                                "order": 8,
                                "phrase": "ありがとうございます。それでは、ご都合の良い日時をお知らせいただけますか？",
                                "phrase_nofiller": "ありがとうございます。それでは、ご都合の良い日時をお知らせいただけますか？",
                                "start_at": 13.39,
                                "end_at": 17.935,
                                "filler_num": None,
                            },
                            {
                                "order": 10,
                                "phrase": "了解しました、来週の月曜日にWeb会議でのデモを行います。詳細はメールでお送りいたします。今日はお時間をいただき、ありがとうございました。",
                                "phrase_nofiller": "了解しました、来週の月曜日にWeb会議でのデモを行います。詳細はメールでお送りいたします。今日はお時間をいただき、ありがとうございました。",
                                "start_at": 13.39,
                                "end_at": 17.935,
                                "filler_num": None,
                            },
                        ],
                    },
                    {
                        "participant_id": "0184f502-8b66-4ab1-10d3-34c0049a9100",
                        "raw": [
                            {
                                "order": 1,
                                "phrase": "こんにちは。MiiTelの詳細を知りたくて資料を頼みました。弊社では現在、業務の効率化とコミュニケーションの改善を目指しています。",
                                "phrase_nofiller": "こんにちは。MiiTelの詳細を知りたくて資料を頼みました。弊社では現在、業務の効率化とコミュニケーションの改善を目指しています。",
                                "start_at": 0.545,
                                "end_at": 2.025,
                                "filler_num": 1,
                            },
                            {
                                "order": 3,
                                "phrase": "特に、チームのコミュニケーションを強化し、業務の透明性を高めたいんです。また、営業チームのパフォーマンス追跡も重要ですね。",
                                "phrase_nofiller": "特に、チームのコミュニケーションを強化し、業務の透明性を高めたいんです。また、営業チームのパフォーマンス追跡も重要ですね。",
                                "start_at": 5.555,
                                "end_at": 7.05,
                                "filler_num": 1,
                            },
                            {
                                "order": 5,
                                "phrase": "それは魅力的ですね。コールログの詳細な分析ができれば、チームの課題をより明確に把握できそうです。",
                                "phrase_nofiller": "それは魅力的ですね。コールログの詳細な分析ができれば、チームの課題をより明確に把握できそうです。",
                                "start_at": 17.07,
                                "end_at": 19.03,
                                "filler_num": 3,
                            },
                            {
                                "order": 7,
                                "phrase": "はい、ぜひお願いします。デモを通して詳細を確認したいです。",
                                "phrase_nofiller": "はい、ぜひお願いします。デモを通して詳細を確認したいです。",
                                "start_at": 17.07,
                                "end_at": 19.03,
                                "filler_num": 3,
                            },
                            {
                                "order": 9,
                                "phrase": "来週の月曜日なら大丈夫です。",
                                "phrase_nofiller": "来週の月曜日なら大丈夫です。",
                                "start_at": 17.07,
                                "end_at": 19.03,
                                "filler_num": 3,
                            },
                            {
                                "order": 11,
                                "phrase": "ありがとうございます。デモを楽しみにしています。",
                                "phrase_nofiller": "ありがとうございます。デモを楽しみにしています。",
                                "start_at": 17.07,
                                "end_at": 19.03,
                                "filler_num": 3,
                            },
                        ],
                        "summary": [
                            {
                                "order": 0,
                                "phrase": "はい。結構ですー。",
                                "phrase_nofiller": "結構ですー。",
                                "start_at": 0.545,
                                "end_at": 2.025,
                                "filler_num": None,
                            },
                            {
                                "order": 2,
                                "phrase": "はい。お世話になります。",
                                "phrase_nofiller": "お世話になります。",
                                "start_at": 5.555,
                                "end_at": 7.05,
                                "filler_num": None,
                            },
                            {
                                "order": 5,
                                "phrase": "あっ、はい。お願いしまーす。",
                                "phrase_nofiller": "お願いしす。",
                                "start_at": 17.07,
                                "end_at": 19.03,
                                "filler_num": None,
                            },
                        ],
                    },
                ],
                "speech_recognition": {
                    "raw": "0:00 (ユーザー) 結構ですー。\n0:02 (取引先) お世話になります。IP電話ミーテルの鈴木と申します。\n0:05 (ユーザー) お世話になります。\n0:06 (取引先) 恐れ入ります、高橋様お手すきでいらっしゃいますか。\n0:13 (取引先) そうだったんですね。わかりました。また来週改めさしていただきます。\n0:17 (ユーザー) お願いしす。\n0:18 (取引先) よろしくお願いいたしますー。",
                    "summary": "0:00 (ユーザー) 結構ですー。\n0:02 (取引先) お世話になります。IP電話ミーテルの鈴木と申します。\n0:05 (ユーザー) お世話になります。\n0:06 (取引先) 恐れ入ります、高橋様お手すきでいらっしゃいますか。\n0:13 (取引先) そうだったんですね。わかりました。また来週改めさしていただきます。\n0:17 (ユーザー) お願いしす。",
                },
            }
        ],
    },
    "params_key": "z&aH+&Kz8saC",
}

response = requests.post(
    "<your-api-url>/api/v1/gpt-custom/add",
    headers=headers,
    data=json.dumps(body),
)

print(response)
