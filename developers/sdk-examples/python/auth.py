"""Python SDK Example: Authentication

Shows how to initialize the Pixelated client with API key auth,
configure the base URL, and verify connectivity.

Install: pip install pixelated_sdk
"""

import os

from pixelated_sdk import ApiClient

# ---------------------------------------------------------------------------
# Basic client initialization
# ---------------------------------------------------------------------------

# The client sends the API key in the X-API-Key header on every request.
# Set the key via an environment variable. Never hardcode it in source.

client = ApiClient(
    api_key=os.environ["PIXELATED_API_KEY"],
    base_url="https://api.pixelated.com",
)

# ---------------------------------------------------------------------------
# Sandbox client
# ---------------------------------------------------------------------------

# Use the sandbox for development. The base URL is the same, but the
# API key routes requests to the sandbox tenant.

sandbox_client = ApiClient(
    api_key=os.environ["PIXELATED_SANDBOX_KEY"],
    base_url="https://api.pixelated.com",
)

# ---------------------------------------------------------------------------
# Verify connectivity
# ---------------------------------------------------------------------------

# If the key is invalid, the SDK raises an ApiException with status 401
# and code "unauthorized". If the key lacks scope, you get 403 "forbidden".


def verify_connection() -> None:
    """Call a lightweight endpoint to confirm the key works."""
    try:
        patients = client.patients.list(limit=1)
        total = patients.pagination.total
        print(f"Connection OK. Patient count: {total}")
    except Exception as err:
        print(f"Connection failed: {err}")
        raise


if __name__ == "__main__":
    verify_connection()
