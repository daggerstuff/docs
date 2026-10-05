# Pixelated EHR API Developer Guide

The Pixelated EHR API provides programmatic access to electronic health
records, clinical encounters, observations, notes, analytics, and outcome
measures. The API follows FHIR R4 resource conventions and uses a consistent
JSON response envelope across all endpoints.

## Base URL

```
https://api.pixelated.com/api/ehr/v1
```

All paths in this guide are relative to this base URL unless noted otherwise.

## Authentication

Every request requires an API key sent in the `X-API-Key` header.

```
X-API-Key: pk_live_abc123...
```

API keys are SHA-256 hashed at rest. The plaintext key is shown only once when
created. Store it securely. If a key is compromised, revoke it immediately
through the key management endpoint.

### Scopes

| Scope | Description |
|-------|-------------|
| `read` | Read access to EHR resources (patients, encounters, observations, notes, analytics, outcomes) |
| `write` | Create and update EHR resources |
| `admin` | Full access including key management, configuration, and administrative endpoints |

A key's scope determines which endpoints it can call. A `read`-scoped key
cannot create or modify resources. Endpoints that require `write` or `admin`
scope return `403 forbidden` when called with a `read`-only key.

### Key Management

Manage API keys at:

```
https://api.pixelated.com/api/developer/api-keys/
```

Supported operations:

- `GET /api/developer/api-keys/` - List your API keys
- `POST /api/developer/api-keys/` - Create a new API key
- `DELETE /api/developer/api-keys/{id}` - Revoke a key

When you create a key, the response includes the plaintext key value. This is
the only time the full key is visible. Subsequent list responses show only the
key prefix and metadata.

## Response Envelope

### Success

Single-resource responses return a `data` field:

```json
{
  "data": {
    "id": "patient-001",
    "resourceType": "Patient",
    "name": [{ "family": "Smith", "given": ["Jane"] }],
    "active": true
  }
}
```

List responses include a `pagination` object:

```json
{
  "data": [
    { "id": "patient-001", "resourceType": "Patient" },
    { "id": "patient-002", "resourceType": "Patient" }
  ],
  "pagination": {
    "limit": 20,
    "offset": 0,
    "total": 142
  }
}
```

### Error

All errors use a consistent envelope with an `error` object containing a
machine-readable `code` and a human-readable `message`:

```json
{
  "error": {
    "code": "validation_failed",
    "message": "patientId is required."
  }
}
```

### HTTP Status Codes

| Status | Meaning |
|--------|---------|
| 200 | Success (GET, PUT) |
| 201 | Created (POST) |
| 400 | Validation failed or malformed request |
| 401 | Missing or invalid API key |
| 403 | API key lacks required scope or permission |
| 404 | Resource not found |
| 429 | Rate limit exceeded |
| 500 | Internal server error |

## Error Codes

| Code | HTTP Status | Description |
|------|-------------|-------------|
| `validation_failed` | 400 | Request body or query parameters failed validation |
| `unauthorized` | 401 | API key missing, expired, or invalid |
| `forbidden` | 403 | API key scope or clinical role lacks permission for this operation |
| `not_found` | 404 | The requested resource does not exist |
| `rate_limited` | 429 | Too many requests in the current window |
| `internal_error` | 500 | Unexpected server error |

Handle errors by checking the `code` field, not by parsing the `message`. The
message text may change between API versions, but the code is stable.

## Pagination

List endpoints accept `limit` and `offset` query parameters.

| Parameter | Default | Maximum |
|-----------|---------|---------|
| `limit` | 20 | 100 |
| `offset` | 0 | None |

Example request:

```
GET /patients?limit=50&offset=100
```

Example response:

```json
{
  "data": [/* up to 50 patient objects */],
  "pagination": {
    "limit": 50,
    "offset": 100,
    "total": 142
  }
}
```

The `pagination.total` field is included when the server can compute the total
count. Some endpoints may omit `total` for performance reasons. When `total`
is absent, continue paginating until `data` is empty.

## Rate Limits

API keys have configurable rate limits measured in requests per minute. The
default limit varies by scope: `read` keys get a higher default, `write` keys
a moderate default, and `admin` keys a lower default (since they access
sensitive endpoints).

Rate limit information is returned in response headers:

| Header | Description |
|--------|-------------|
| `X-RateLimit-Limit` | Maximum requests per minute for this key |
| `X-RateLimit-Remaining` | Requests remaining in the current window |
| `X-RateLimit-Reset` | Unix timestamp when the window resets |

When you exceed the rate limit, the API returns `429` with an error code of
`rate_limited`. The response also includes a `Retry-After` header (seconds)
indicating when to retry.

```
HTTP/1.1 429 Too Many Requests
X-RateLimit-Limit: 60
X-RateLimit-Remaining: 0
X-RateLimit-Reset: 1696234680
Retry-After: 30
Content-Type: application/json

{
  "error": {
    "code": "rate_limited",
    "message": "Rate limit exceeded. Retry after 30 seconds."
  }
}
```

Implement exponential backoff with jitter when retrying rate-limited requests.

## Webhooks

The EHR API sends webhook events when clinical resources change. Configure a
webhook endpoint through the developer dashboard to receive these events.

### Event Types

| Event | Description |
|-------|-------------|
| `patient.created` | A new patient was created |
| `patient.updated` | A patient record was updated |
| `encounter.created` | A new encounter was created |
| `encounter.updated` | An encounter was updated |
| `observation.created` | A new observation was recorded |
| `observation.updated` | An observation was updated |
| `note.created` | A clinical note was created |
| `note.signed` | A clinical note was signed by a clinician |

### Webhook Payload

```json
{
  "eventType": "patient.created",
  "timestamp": "2024-01-15T10:30:00Z",
  "resourceType": "Patient",
  "resourceId": "patient-001",
  "tenantId": "tenant-abc",
  "data": {
    "id": "patient-001",
    "resourceType": "Patient",
    "name": [{ "family": "Smith", "given": ["Jane"] }],
    "active": true
  }
}
```

| Field | Type | Description |
|-------|------|-------------|
| `eventType` | string | The event type (see table above) |
| `timestamp` | string | ISO 8601 timestamp of the event |
| `resourceType` | string | FHIR resource type (Patient, Encounter, Observation, etc.) |
| `resourceId` | string | ID of the affected resource |
| `tenantId` | string | Tenant ID for multi-tenant isolation |
| `data` | object | The full resource payload at the time of the event |

### Signature Verification

Every webhook delivery includes an HMAC-SHA256 signature in the
`X-Webhook-Signature` header. The signature is computed over the raw request
body using your webhook signing secret.

To verify:

1. Read the raw request body (before any JSON parsing).
2. Compute `HMAC-SHA256(raw_body, webhook_secret)` and encode as hex.
3. Compare the result to the `X-Webhook-Signature` header value using a
   constant-time comparison.

If the signature does not match, reject the delivery. Do not process
unsigned or mismatched webhooks.

### Delivery and Retries

The API expects your endpoint to respond with `200` within 10 seconds. If your
endpoint returns a non-2xx status or times out, the API retries delivery with
exponential backoff: 1 minute, 5 minutes, 15 minutes, 1 hour, 6 hours. After
the final retry, the delivery is marked as failed and logged.

## FHIR Compatibility

EHR API endpoints mirror FHIR R4 resource structures. Patient, Encounter, and
Observation resources follow FHIR R4 conventions for field names, data types,
and search parameters.

A FHIR R4 CapabilityStatement is available at:

```
GET /api/fhir/r4/metadata
```

This endpoint returns the full FHIR CapabilityStatement describing supported
resources, interactions, search parameters, and operations. Use it to
validate FHIR compatibility before integrating.

Not all FHIR search parameters are supported on every endpoint. The query
parameters documented in the Endpoints section below are the authoritative
list for each route.

## Endpoints

### Patients

#### GET /patients

Search patients by name query or active status.

**Query Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `q` | string | Search query (matches patient name) |
| `active` | string | Filter by active status. Pass `false` to include inactive patients. Defaults to active-only. |
| `limit` | integer | Page size (default 20, max 100) |
| `offset` | integer | Page offset (default 0) |

**Response:** `200` with paginated patient list.

```
GET /patients?q=Smith&limit=20&offset=0
```

#### POST /patients

Create a new patient.

**Request Body:**

```json
{
  "name": [
    {
      "family": "Smith",
      "given": ["Jane", "Marie"]
    }
  ],
  "birthDate": "1985-03-15",
  "gender": "female",
  "telecom": [
    { "system": "phone", "value": "555-0100" }
  ],
  "address": [
    { "line": ["123 Main St"], "city": "Springfield", "state": "IL", "postalCode": "62701" }
  ],
  "active": true
}
```

**Response:** `201` with created patient resource.

#### GET /patients/{id}

Read a single patient by ID.

**Response:** `200` with patient resource, or `404` if not found.

#### PATCH /patients/{id}

Partially update an existing patient. Send only the fields to update.

**Response:** `200` with updated patient resource, or `404` if not found.

#### DELETE /patients/{id}

Delete a patient. This is a soft delete. The patient record is marked inactive
and excluded from default search results.

**Response:** `200` with confirmation, or `404` if not found.

### Encounters

#### GET /encounters

Search encounters. At least one filter is required.

**Query Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `patient` | string | Patient ID |
| `status` | string | Encounter status (e.g., `planned`, `arrived`, `in-progress`, `finished`) |
| `practitioner` | string | Practitioner ID |
| `start` | string | ISO timestamp for date range start |
| `end` | string | ISO timestamp for date range end |
| `limit` | integer | Page size (default 20, max 100) |
| `offset` | integer | Page offset (default 0) |

**Response:** `200` with paginated encounter list.

```
GET /encounters?patient=patient-001&status=finished&limit=20
```

#### POST /encounters

Create a new encounter from a FHIR Encounter resource.

**Request Body:** FHIR Encounter resource.

**Response:** `201` with created encounter.

#### GET /encounters/{id}

Read a single encounter by ID.

**Response:** `200` with encounter resource, or `404`.

#### PATCH /encounters/{id}

Partially update an existing encounter.

**Response:** `200` with updated encounter, or `404`.

### Observations

#### GET /observations

Search observations. At least one filter is required.

**Query Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `patient` | string | Patient ID |
| `encounter` | string | Encounter ID |
| `code` | string | LOINC code (e.g., `44261-6` for PHQ-9) |
| `status` | string | Observation status (e.g., `final`, `preliminary`) |
| `start` | string | ISO timestamp for date range start (requires `patient`) |
| `end` | string | ISO timestamp for date range end (requires `patient`) |
| `limit` | integer | Page size (default 20, max 100) |
| `offset` | integer | Page offset (default 0) |

**Response:** `200` with paginated observation list.

```
GET /observations?patient=patient-001&code=44261-6&limit=50
```

#### POST /observations

Create a new observation (e.g., PHQ-9 or GAD-7 scores).

**Request Body:** FHIR Observation resource.

**Response:** `201` with created observation.

#### GET /observations/{id}

Read a single observation by ID.

**Response:** `200` with observation resource, or `404`.

#### PATCH /observations/{id}

Partially update an existing observation.

**Response:** `200` with updated observation, or `404`.

### Clinical Notes

#### GET /notes

List clinical note templates, optionally filtered by modality.

**Query Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `modality` | string | Filter templates by modality (e.g., `individual`, `group`, `family`) |

**Response:** `200` with note template list.

#### POST /notes

Create a clinical note (DocumentReference) from a template.

**Request Body:**

```json
{
  "templateId": "initial-intake",
  "patientId": "patient-001",
  "encounterId": "encounter-001",
  "values": {
    "chief_complaint": "Patient reports persistent anxiety",
    "mental_status": "Alert and oriented"
  }
}
```

**Response:** `201` with created DocumentReference.

#### POST /notes/{id}/sign

Sign a clinical note. This is the compliance gate for AI-drafted notes. Only
manual, individual sign-off is accepted. Batch or automated signing is
rejected.

**Request Body:**

```json
{
  "note": { "id": "note-001", "resourceType": "DocumentReference" },
  "patient_id": "patient-001",
  "encounter_id": "encounter-001",
  "signer_ref": "Practitioner/practitioner-001"
}
```

**Response:** `200` with signed note, or `400` if the note is not a registered
AI draft or the sign request is automated.

### Analytics

#### GET /analytics

Retrieve dashboard metrics for a specified dashboard type.

**Query Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `type` | string | Required. One of: `practice`, `outcomes`, `utilization`, `billing`, `compliance` |
| `startDate` | string | ISO date string for time range start |
| `endDate` | string | ISO date string for time range end |
| `provider` | string | Filter by provider ID |
| `location` | string | Filter by location ID |
| `payer` | string | Filter by payer ID |

**Response:** `200` with dashboard metrics.

```
GET /analytics?type=outcomes&startDate=2024-01-01&endDate=2024-03-31
```

#### GET /analytics/saved-views

List saved analytics views for the current user.

**Response:** `200` with saved view list.

#### POST /analytics/saved-views

Create a saved analytics view.

**Request Body:**

```json
{
  "name": "Q1 Outcomes Dashboard",
  "type": "outcomes",
  "filters": {
    "timeRange": { "start": "2024-01-01", "end": "2024-03-31" }
  }
}
```

**Response:** `201` with created saved view.

#### POST /analytics/export/pdf

Export analytics data as a PDF document.

**Request Body:**

```json
{
  "type": "outcomes",
  "startDate": "2024-01-01",
  "endDate": "2024-03-31",
  "format": "pdf"
}
```

**Response:** `200` with PDF binary content (`Content-Type: application/pdf`).

### Outcomes

#### GET /outcomes

List available outcome measures (PHQ-9, GAD-7, OQ-45) with metadata.

**Response:** `200` with measure list.

#### GET /outcomes/alerts

List outcome alerts. Alerts are triggered when significant change is detected
in outcome measure scores.

**Response:** `200` with alert list.

#### GET /outcomes/config

Get the outcome configuration for the current tenant. Includes threshold
settings, alert rules, and measure enablement.

**Response:** `200` with outcome configuration.

#### POST /outcomes/config

Update the outcome configuration.

**Request Body:** Updated configuration object.

**Response:** `200` with updated configuration.

#### GET /outcomes/trending

Get trending outcome data. Returns time-series data for outcome measures
across the tenant.

**Query Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `measure` | string | Filter by measure type (e.g., `phq-9`, `gad-7`, `oq-45`) |
| `startDate` | string | ISO date string for range start |
| `endDate` | string | ISO date string for range end |

**Response:** `200` with trending data.

## Sandbox

A sandbox tenant with pre-seeded test data is available for development and
testing. The sandbox includes sample patients, encounters, observations, and
outcome measures.

Contact support at `support@pixelated.com` to request sandbox access. Once
provisioned, you receive a sandbox API key and can make requests against the
same base URL. Sandbox data is reset periodically.

Sandbox API keys have `read` and `write` scopes but cannot access `admin`
endpoints. Rate limits in the sandbox are lower than production.
