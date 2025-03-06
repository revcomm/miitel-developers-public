from libs.incoming_webhook import IncomingWebhook
from libs.search_conditions import OUTGOING_EXTERNAL_CRITERIA
from libs.util import SegmentUtils, Utils


class OutgoingCall:
    """
    genesysユーザーからの発信に該当するsegmentを抽出してincoming webhookに送信する関数
    通話中の転送、割り込み等のないシンプルな発信を想定。着信時のフローなども設定無し

    Function to extract segments corresponding to outgoing calls from Genesys users and send them to the incoming webhook.
    Assumes simple outgoing calls without transfers or barge-in during the call. No flow settings for outgoing calls.
    """

    @staticmethod
    def create_call(genesys_conversation_data, bucket_name, genesys_audio_meta_data):
        flatten_segments = SegmentUtils.create_flatten_segments(
            genesys_conversation_data
        )
        # Genesysの通話履歴データから発信に該当するsegmentを抽出。ユースケースに沿って複数segment取得はしない / Extract segments corresponding to outgoing calls from Genesys call history data. Multiple segments are not retrieved depending on the use case.
        segment = SegmentUtils.get_segment(flatten_segments, OUTGOING_EXTERNAL_CRITERIA)

        # 該当がない場合はNoneを返す / Return None if no matching segment is found
        if segment is None:
            return None

        # 転送元の前のセグメントの開始時刻をcall_starts_atとして設定 / Set the start time of the previous segment as call_starts_at
        previous_segment = SegmentUtils.find_adjacent_segment(
            flatten_segments, segment, "previous"
        )
        if previous_segment:
            segment["callStartsAt"] = previous_segment["segmentStart"]

        genesys_miitel_mapped_data = [
            ("OUTGOING_CALL", segment),
        ]
        payload = IncomingWebhook.create_payload(genesys_miitel_mapped_data)
        audio_upload_urls = IncomingWebhook.post_incoming_webhook(payload)

        response = None
        for audio_url in (
            audio_upload_urls
        ):  # genesys_miitel_mapped_dataが一つなので、このループは一回しか実行されない / Since genesys_miitel_mapped_data has only one item, this loop will only execute once
            audio_path = Utils.extract_object_key(genesys_audio_meta_data["filePath"])
            response = IncomingWebhook.upload_audio_file(
                audio_url, bucket_name, audio_path
            )
        # 実行されたかどうかを確認するために返す / Return the response to check if it was executed
        return response
