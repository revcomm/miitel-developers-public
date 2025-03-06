import datetime


class SegmentUtils:
    @staticmethod
    def _matches_criteria(segment, criteria):
        """
        セグメントが指定されたcriteriaを満たすかをチェックする関数

        Function to check if a segment meets the specified criteria
        """
        return all(segment.get(key) == value for key, value in criteria.items())

    @classmethod
    def get_segment(cls, flatten_segments, criteria):
        """
        criteriaを持つsegmentを1つ返す関数

        Function to return a segment that matches the criteria
        """
        matching_segments = [
            segment
            for segment in flatten_segments
            if cls._matches_criteria(segment, criteria)
        ]
        return matching_segments[0] if len(matching_segments) == 1 else None

    @classmethod
    def get_segments(cls, flatten_segments, criteria):
        """
        criteriaを持つsegmentをリストとして返す関数

        Function to return a list of segments that match the criteria
        """
        matching_segments = [
            segment
            for segment in flatten_segments
            if cls._matches_criteria(segment, criteria)
        ]
        return matching_segments

    @classmethod
    def find_next_criteria_segment(cls, flatten_segments, target_segment, criteria):
        """
        target_segment以降で条件にマッチする次のセグメントを取得する関数

        Function to get the next segment that matches the criteria after the target_segment
        """
        while target_segment:
            next_segment = cls.find_adjacent_segment(
                flatten_segments, target_segment, "next"
            )
            if next_segment and cls._matches_criteria(next_segment, criteria):
                return next_segment
            target_segment = next_segment
        return None

    @staticmethod
    def find_adjacent_segment(flatten_segments, target_segment, direction="next"):
        """
        指定されたsegmentの次のsegmentまたは前のsegmentを取得する関数
        directionが"next"の場合は次のsegment、"previous"の場合は前のsegmentを取得する

        Function to get the next or previous segment of the specified segment
        If direction is "next", get the next segment, if "previous", get the previous segment
        """
        target_time = (
            datetime.datetime.fromisoformat(target_segment["segmentEnd"])
            if direction == "next"
            else datetime.datetime.fromisoformat(target_segment["segmentStart"])
        )
        closest_segment = None
        closest_time_diff = datetime.timedelta.max

        for segment in flatten_segments:
            segment_start_time = datetime.datetime.fromisoformat(
                segment["segmentStart"]
            )
            segment_end_time = datetime.datetime.fromisoformat(segment["segmentEnd"])

            if direction == "next" and segment_start_time >= target_time:
                time_diff = segment_start_time - target_time
                if time_diff < closest_time_diff:
                    closest_time_diff = time_diff
                    closest_segment = segment
            elif direction == "previous" and segment_end_time <= target_time:
                time_diff = target_time - segment_end_time
                if time_diff < closest_time_diff:
                    closest_time_diff = time_diff
                    closest_segment = segment

        return closest_segment

    @staticmethod
    def create_flatten_segments(genesys_conversation_data):
        """
        Genesysの通話履歴データをセグメント単位に分解し、ネストをflatにする

        Function to decompose Genesys call history data into segments and flatten nested data
        """
        results = []
        participants = genesys_conversation_data["participants"]

        for participant in participants:
            participant_id = participant["participantId"]
            participant_name = participant.get("participantName", "Unknown")
            sessions = participant["sessions"]
            purpose = participant.get("purpose", "Unknown")

            for session in sessions:
                ani = session.get("ani", "Unknown")
                dnis = session.get("dnis", "Unknown")
                destination_addresses = session.get("destinationAddresses", "Unknown")
                direction = session.get("direction", "Unknown")
                media_type = session.get("mediaType", "Unknown")
                segments = session.get("segments", [])

                for segment in segments:
                    segment_type = segment.get("segmentType", "Unknown")
                    segment_start = segment.get("segmentStart", "Unknown")
                    segment_end = segment.get("segmentEnd", "Unknown")
                    # https://help.mypurecloud.com/articles/disconnect-reasons/
                    disconnect_type = segment.get("disconnectType", "Unknown")

                    result = {
                        "participantId": participant_id,
                        "from": ani,
                        "to": dnis,
                        "destinationAddresses": destination_addresses,
                        "purpose": purpose,
                        "participant": participant_name,
                        "direction": direction,
                        "media_type": media_type,
                        "segmentType": segment_type,
                        "segmentStart": segment_start,
                        "segmentEnd": segment_end,
                        "disconnectType": disconnect_type,
                    }
                    results.append(result)
        return results


class Utils:
    @staticmethod
    def extract_object_key(audio_path):
        """
        S3パスからバケット名を取り除き、オブジェクトキーを取得する関数

        Function to remove the bucket name from the S3 path and get the object key
        """
        # "s3://"を取り除く / Remove "s3://"
        path_without_scheme = audio_path.replace("s3://", "")
        # バケット名とオブジェクトキーを分割 / Split bucket name and object key
        _, object_key = path_without_scheme.split("/", 1)
        return object_key

    @staticmethod
    def format_phone_number(phone_number):
        """
        "tel:+81"を取り除き、先頭に"0"を追加

        Remove "tel:+81" and add "0" at the beginning
        """
        if phone_number.startswith("tel:+81"):
            domestic_number = "0" + phone_number[7:]
            return domestic_number
        return phone_number
