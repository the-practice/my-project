"""
Email API routes for webhook and IMAP inbox polling.
"""

import asyncio
import imaplib
import email as email_lib
import logging
from typing import Dict, Any, List
from fastapi import APIRouter, HTTPException, status

from app.core.config import settings
from app.api.schemas import EmailWebhookRequest, EmailWebhookResponse, InboxResponse

logger = logging.getLogger(__name__)
router = APIRouter()


def _poll_imap_inbox() -> List[Dict[str, Any]]:
    """
    Poll IMAP inbox for unread emails (runs in executor).

    Returns a list of unread email metadata.
    """
    try:
        with imaplib.IMAP4_SSL(settings.IMAP_HOST, settings.IMAP_PORT) as imap:
            imap.login(settings.IMAP_USERNAME, settings.IMAP_PASSWORD)
            imap.select("INBOX")

            # Search for unread emails
            _, msg_ids = imap.search(None, "UNSEEN")
            results = []

            # Process up to 20 most recent unread emails
            msg_id_list = msg_ids[0].split()[-20:] if msg_ids[0] else []

            for msg_id in msg_id_list:
                try:
                    _, msg_data = imap.fetch(msg_id, "(RFC822)")
                    msg = email_lib.message_from_bytes(msg_data[0][1])

                    results.append({
                        "id": msg_id.decode(),
                        "from": msg.get("From", "unknown"),
                        "subject": msg.get("Subject", "(no subject)"),
                        "date": msg.get("Date", "unknown"),
                    })
                except Exception as e:
                    logger.warning(f"Error processing email {msg_id}: {e}")
                    continue

            return results

    except imaplib.IMAP4.error as e:
        logger.error(f"IMAP error: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error polling IMAP: {e}")
        raise


@router.post("/webhook", response_model=EmailWebhookResponse)
async def email_webhook(request: EmailWebhookRequest) -> EmailWebhookResponse:
    """
    Email event webhook endpoint.

    This endpoint receives email events from email service providers
    (e.g., SendGrid, Mailgun, etc.) and processes them.

    Supports flexible JSON payload formats.
    """
    # Extract email data from various possible formats using model fields
    from_addr = (
        request.from_ or
        request.sender or
        request.From or
        "unknown"
    )
    subject = (
        request.subject or
        request.Subject or
        "(no subject)"
    )
    text_body = (
        request.text or
        request.plain or
        request.body or
        request.body_plain or
        ""
    )

    # Log the incoming email
    logger.info(
        f"Email webhook: from={from_addr}, subject={subject}, "
        f"body_length={len(text_body)}"
    )

    # Compose a summary of the email for potential task creation
    goal = f"Email from {from_addr}: {subject}\n\n{text_body[:500]}"
    logger.debug(f"Email content: {goal}")

    # TODO: Create a Task record from the email
    # This would require linking the email to a user_id, which needs to be resolved
    # For now, we acknowledge receipt and log the data

    return EmailWebhookResponse(
        status="received",
        from_addr=from_addr,
        subject=subject,
        message="Email received and logged for processing"
    )


@router.get("/inbox", response_model=InboxResponse)
async def get_inbox() -> InboxResponse:
    """
    Poll IMAP inbox endpoint.

    This endpoint polls the user's IMAP inbox for unread emails
    and returns a list of recent unread messages.
    """
    # Check if IMAP credentials are configured
    if not settings.IMAP_USERNAME or not settings.IMAP_PASSWORD:
        logger.warning("IMAP not configured - credentials missing")
        return InboxResponse(
            status="not_configured",
            count=0,
            emails=[],
            message="IMAP credentials not configured"
        )

    try:
        # Run IMAP polling in thread executor (IMAP is synchronous I/O)
        loop = asyncio.get_event_loop()
        emails = await loop.run_in_executor(None, _poll_imap_inbox)

        logger.info(f"IMAP poll successful: found {len(emails)} unread emails")

        return InboxResponse(
            status="ok",
            count=len(emails),
            emails=emails
        )

    except imaplib.IMAP4.error as e:
        logger.error(f"IMAP connection error: {e}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"IMAP error: {str(e)}"
        )

    except Exception as e:
        logger.error(f"Unexpected error in IMAP poll: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error polling inbox: {str(e)}"
        )
