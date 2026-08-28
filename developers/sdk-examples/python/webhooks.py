"""Python SDK Example: Webhook Handling

Verify webhook signatures and process EHR events in a Flask, FastAPI,
or similar HTTP server.

Webhooks are delivered as POST requests with a JSON body. Every
delivery includes an HMAC-SHA256 signature in the X-Webhook-Signature
header. Verify the signature before processing the payload.
"""

import hashlib
import hmac
import json
import os
from typing import Any

# ---------------------------------------------------------------------------
# Signature verification
# ---------------------------------------------------------------------------


def verify_webhook_signature(raw_body: bytes, signature: str, secret: str) -> bool:
    """Verify the HMAC-SHA256 signature of a webhook delivery.

    Args:
        raw_body: The raw request body bytes (before JSON parsing).
        signature: The value of the X-Webhook-Signature header.
        secret: Your webhook signing secret.

    Returns:
        True if the signature matches, False otherwise.
    """
    expected = hmac.new(
        secret.encode("utf-8"), raw_body, hashlib.sha256
    ).hexdigest()

    # Use hmac.compare_digest to prevent timing attacks
    return hmac.compare_digest(expected, signature)


# ---------------------------------------------------------------------------
# Event types
# ---------------------------------------------------------------------------

WEBHOOK_EVENTS = {
    "patient.created",
    "patient.updated",
    "encounter.created",
    "encounter.updated",
    "observation.created",
    "observation.updated",
    "note.created",
    "note.signed",
}


# ---------------------------------------------------------------------------
# Webhook handler
# ---------------------------------------------------------------------------


def handle_webhook(
    raw_body: bytes,
    headers: dict[str, str],
    secret: str,
) -> tuple[int, dict[str, Any]]:
    """Process an incoming webhook delivery.

    Args:
        raw_body: The raw request body bytes.
        headers: Request headers (lowercase keys).
        secret: Your webhook signing secret.

    Returns:
        A tuple of (status_code, response_body).
    """
    # 1. Extract the signature header
    signature = headers.get("x-webhook-signature")
    if not signature:
        return 401, {"error": "Missing X-Webhook-Signature header"}

    # 2. Verify the signature
    if not verify_webhook_signature(raw_body, signature, secret):
        return 401, {"error": "Invalid webhook signature"}

    # 3. Parse the payload
    try:
        payload = json.loads(raw_body.decode("utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError):
        return 400, {"error": "Invalid JSON payload"}

    event_type = payload.get("eventType", "")
    resource_id = payload.get("resourceId", "")
    tenant_id = payload.get("tenantId", "")

    # 4. Dispatch to the appropriate handler
    try:
        if event_type == "patient.created":
            on_patient_created(payload)
        elif event_type == "patient.updated":
            on_patient_updated(payload)
        elif event_type == "encounter.created":
            on_encounter_created(payload)
        elif event_type == "observation.created":
            on_observation_created(payload)
        elif event_type == "note.signed":
            on_note_signed(payload)
        else:
            print(f"Unhandled event type: {event_type}")
    except Exception as err:
        # Log the error but still return 500 to trigger a retry.
        # The API retries on non-2xx responses with exponential backoff.
        print(f"Webhook handler error: {err}")
        return 500, {"error": "Handler failed"}

    return 200, {"received": True}


# ---------------------------------------------------------------------------
# Event handlers
# ---------------------------------------------------------------------------


def on_patient_created(payload: dict[str, Any]) -> None:
    resource_id = payload.get("resourceId", "")
    tenant_id = payload.get("tenantId", "")
    print(f"Patient created: {resource_id} in tenant {tenant_id}")
    # Sync the patient to your system, trigger onboarding, etc.


def on_patient_updated(payload: dict[str, Any]) -> None:
    resource_id = payload.get("resourceId", "")
    print(f"Patient updated: {resource_id}")
    # Update your local cache of the patient record.


def on_encounter_created(payload: dict[str, Any]) -> None:
    resource_id = payload.get("resourceId", "")
    print(f"Encounter created: {resource_id}")
    # Notify the care team, update scheduling, etc.


def on_observation_created(payload: dict[str, Any]) -> None:
    resource_id = payload.get("resourceId", "")
    print(f"Observation created: {resource_id}")
    # Check for alert thresholds, update dashboards, etc.


def on_note_signed(payload: dict[str, Any]) -> None:
    resource_id = payload.get("resourceId", "")
    print(f"Note signed: {resource_id}")
    # Archive the signed note, update compliance records, etc.


# ---------------------------------------------------------------------------
# Flask integration example (commented out, requires flask)
# ---------------------------------------------------------------------------

# from flask import Flask, request, Response
#
# app = Flask(__name__)
# WEBHOOK_SECRET = os.environ["PIXELATED_WEBHOOK_SECRET"]
#
#
# @app.route("/webhooks/pixelated", methods=["POST"])
# def webhook() -> Response:
#     raw_body = request.get_data()
#     headers = {k.lower(): v for k, v in request.headers.items()}
#     status, body = handle_webhook(raw_body, headers, WEBHOOK_SECRET)
#     return Response(
#         json.dumps(body),
#         status=status,
#         content_type="application/json",
#     )
#
#
# if __name__ == "__main__":
#     app.run(port=3000)


# ---------------------------------------------------------------------------
# FastAPI integration example (commented out, requires fastapi)
# ---------------------------------------------------------------------------

# from fastapi import FastAPI, Request, Response
#
# app = FastAPI()
# WEBHOOK_SECRET = os.environ["PIXELATED_WEBHOOK_SECRET"]
#
#
# @app.post("/webhooks/pixelated")
# async def webhook(request: Request) -> Response:
#     raw_body = await request.body()
#     headers = {k.lower(): v for k, v in request.headers.items()}
#     status, body = handle_webhook(raw_body, headers, WEBHOOK_SECRET)
#     return Response(
#         content=json.dumps(body),
#         status_code=status,
#         media_type="application/json",
#     )
