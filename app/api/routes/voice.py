"""
Voice API routes for Twilio and Vapi.ai integration.
"""

import logging
from fastapi import APIRouter, Request, HTTPException, status
from typing import Dict, Any
from twilio.request_validator import RequestValidator
from twilio.twiml.voice_response import VoiceResponse, Gather, Say

from app.core.config import settings
from app.api.schemas import VapiWebhookRequest

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/webhook/twilio")
async def twilio_webhook(request: Request) -> Dict[str, str]:
    """
    Twilio voice webhook endpoint.

    This endpoint receives voice calls from Twilio and responds with TwiML.
    It validates the webhook signature for security.
    """
    # Get request body for signature validation
    body = await request.body()

    # Validate Twilio request signature (skip if AUTH_TOKEN not configured)
    if settings.TWILIO_AUTH_TOKEN:
        validator = RequestValidator(settings.TWILIO_AUTH_TOKEN)
        twilio_signature = request.headers.get("X-Twilio-Signature", "")
        request_url = str(request.url)

        # Parse form data for validation
        form_data = await request.form()

        if not validator.validate(request_url, form_data, twilio_signature):
            logger.warning(f"Invalid Twilio signature from {request.client}")
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Invalid Twilio signature"
            )

    # Parse form data
    form_data = await request.form()
    call_sid = form_data.get("CallSid", "unknown")
    from_number = form_data.get("From", "unknown")
    to_number = form_data.get("To", "unknown")
    call_status = form_data.get("CallStatus", "unknown")
    speech_result = form_data.get("SpeechResult", None)

    # Log the incoming call
    logger.info(
        f"Twilio webhook: CallSid={call_sid}, From={from_number}, To={to_number}, "
        f"CallStatus={call_status}, SpeechResult={speech_result}"
    )

    # Create TwiML response
    response = VoiceResponse()

    if speech_result:
        # User has provided speech input
        logger.info(f"Processing speech: {speech_result}")
        response.say("I received your request and will process it shortly.")
        response.hangup()
    else:
        # Initial call - gather speech input
        gather = Gather(
            input="speech",
            action="/api/voice/webhook/twilio",
            timeout=5,
            method="POST"
        )
        gather.say("How can I help you today?")
        response.append(gather)
        response.say("I did not hear any input. Please try again.")

    # Return TwiML response
    return {"message": str(response)}


@router.post("/vapi/stream")
async def vapi_stream(request: VapiWebhookRequest) -> Dict[str, Any]:
    """
    Vapi.ai real-time stream endpoint.

    This endpoint handles webhook events from Vapi.ai, including:
    - Assistant request initialization
    - Function calls from the AI
    - End of call reports
    - Status updates
    """
    message_type = request.type

    logger.info(f"Vapi webhook: type={message_type}")

    # Route based on message type
    if message_type == "assistant-request":
        # Initialize assistant for the call
        logger.info("Vapi: Assistant request - initializing")
        return {
            "assistant": {
                "firstMessage": "Hello, how can I help you today?",
                "model": {
                    "provider": "anthropic",
                    "model": "claude-haiku-4-5-20251001"
                }
            }
        }

    elif message_type == "function-call":
        # Handle function calls from Vapi
        function_name = request.function.get("name", "unknown") if request.function else "unknown"
        function_args = request.function.get("arguments", {}) if request.function else {}
        logger.info(f"Vapi: Function call - {function_name} with args: {function_args}")
        return {
            "result": f"Function {function_name} has been noted and is being processed."
        }

    elif message_type == "end-of-call-report":
        # Process end of call summary
        ended_reason = request.endedReason or "unknown"
        transcript = request.transcript or ""
        duration = request.duration or 0
        logger.info(
            f"Vapi: Call ended - reason={ended_reason}, duration={duration}s, "
            f"transcript_length={len(transcript)}"
        )
        return {"status": "received", "call_processed": True}

    elif message_type == "status-update":
        # Handle status updates
        status_msg = request.status or "unknown"
        logger.info(f"Vapi: Status update - {status_msg}")
        return {"status": "ok"}

    else:
        # Unhandled message type
        logger.warning(f"Vapi: Unhandled message type - {message_type}")
        return {
            "status": "unhandled",
            "type": message_type,
            "message": f"Message type {message_type} is not yet handled"
        }
