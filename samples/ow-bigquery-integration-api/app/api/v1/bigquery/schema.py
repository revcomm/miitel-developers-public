import uuid
from datetime import datetime

from app.api.base_schema import BaseModel
from pydantic import BaseModel


class OutgoingWebhookAnalysisPayload(BaseModel, extra="allow"):
    score: float = None
    tlr: float = None
    rally_count: int = None
    overlap_count: int = None
    silence_count: int = None


class OutgoingWebhookCallDetailPayload(BaseModel, extra="allow"):
    id: uuid.UUID
    dial_starts_at: datetime = None
    dial_answered_at: datetime = None
    dial_ends_at: datetime = None
    queueing_starts_at: datetime = None
    queueing_answered_at: datetime = None
    queueing_ends_at: datetime = None
    call_type: str = None
    circuit_number: str = None
    circuit_name: str = None
    from_number: str = None
    to_number: str = None
    previous_id: uuid.UUID = None
    dtmf: int = None


class OutgoingWebhookCallPayload(BaseModel, extra="allow"):
    id: uuid.UUID
    tenant_code: str
    details: list[OutgoingWebhookCallDetailPayload] = None


class OutgoingWebhookPayload(BaseModel, extra="allow"):
    call: OutgoingWebhookCallPayload = None
    challenge: str = None
