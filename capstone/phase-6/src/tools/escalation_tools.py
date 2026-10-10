import json
import uuid
from typing import Dict, Any, Optional
from pydantic import BaseModel, Field, ValidationError

class EscalationTicketSchema(BaseModel):
    ticket_id: str = Field(..., description="Unique generated support ticket ID")
    user_id: str = Field(..., description="ID of the user requesting escalation")
    reason: str = Field(..., description="Core reason for human handover")
    summary: str = Field(..., description="Context summary for the support agent")
    status: str = Field(default="OPEN")
    priority: str = Field(default="HIGH")

def escalate_to_human(reason: str, user_id: str, summary: str) -> str:
    """
    Creates a support ticket with defensive schema validation.
    Ensures downstream CRM systems never ingest malformed ticket payloads.
    """
    try:
        # Construct raw payload
        raw_ticket = {
            "ticket_id": f"TICK-{uuid.uuid4().hex[:8].upper()}",
            "user_id": user_id,
            "reason": reason,
            "summary": summary,
            "status": "OPEN",
            "priority": "HIGH"
        }

        # Defensive Parsing: Validate through Pydantic schema before returning
        validated_ticket = EscalationTicketSchema(**raw_ticket)

        return json.dumps({
            "status": "SUCCESS",
            "message": f"Support ticket successfully validated and dispatched. ID: {validated_ticket.ticket_id}",
            "ticket": validated_ticket.model_dump()
        })

    except ValidationError as e:
        # Defensive fallback: Catch schema mismatch and return structured error to model
        return json.dumps({
            "status": "ERROR",
            "message": "Failed to generate valid escalation ticket due to schema validation error.",
            "details": str(e)
        })