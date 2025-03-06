# 着信 / Incoming call
INCOMING_USER_INTERACT_CRITERIA = {
    "purpose": "user",
    "segmentType": "interact",
    "direction": "inbound",
}

# 発信 / Outgoing call
OUTGOING_EXTERNAL_CRITERIA = {
    "purpose": "external",
    "segmentType": "interact",
    "direction": "outbound",
}

# 留守電 / Voicemail
INCOMING_VOICEMAIL_CRITERIA = {
    "purpose": "voicemail",
    "segmentType": "interact",
    "direction": "inbound",
}