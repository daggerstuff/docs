/**
 * TypeScript SDK Example: Webhook Handling
 *
 * Verify webhook signatures and process EHR events in an Express
 * or similar HTTP server.
 *
 * Webhooks are delivered as POST requests with a JSON body. Every
 * delivery includes an HMAC-SHA256 signature in the X-Webhook-Signature
 * header. Verify the signature before processing the payload.
 */

import crypto from 'node:crypto';

/**
 * Verify the HMAC-SHA256 signature of a webhook delivery.
 *
 * @param rawBody - The raw request body as a Buffer (before JSON parsing)
 * @param signature - The value of the X-Webhook-Signature header
 * @param secret - Your webhook signing secret
 * @returns true if the signature matches, false otherwise
 */
function verifyWebhookSignature(
  rawBody: Buffer,
  signature: string,
  secret: string,
): boolean {
  const expected = crypto
    .createHmac('sha256', secret)
    .update(rawBody)
    .digest('hex');

  // Use timingSafeEqual to prevent timing attacks
  if (expected.length !== signature.length) {
    return false;
  }

  return crypto.timingSafeEqual(
    Buffer.from(expected),
    Buffer.from(signature),
  );
}

/**
 * Webhook event types and their descriptions.
 */
const WEBHOOK_EVENTS = {
  patient_created: 'patient.created',
  patient_updated: 'patient.updated',
  encounter_created: 'encounter.created',
  encounter_updated: 'encounter.updated',
  observation_created: 'observation.created',
  observation_updated: 'observation.updated',
  note_created: 'note.created',
  note_signed: 'note.signed',
} as const;

type WebhookEvent = (typeof WEBHOOK_EVENTS)[keyof typeof WEBHOOK_EVENTS];

/**
 * Parsed webhook payload.
 */
interface WebhookPayload {
  eventType: WebhookEvent;
  timestamp: string;
  resourceType: string;
  resourceId: string;
  tenantId: string;
  data: Record<string, unknown>;
}

/**
 * Express-style webhook handler.
 *
 * Mount this on your server at the URL configured in the developer
 * dashboard. The handler verifies the signature, parses the payload,
 * dispatches to the appropriate handler, and returns 200.
 *
 * Important: use `express.raw()` to capture the raw body before
 * JSON parsing. If you use `express.json()` first, the signature
 * verification will fail because the body has been re-serialized.
 *
 * @example
 *   import express from 'express';
 *   const app = express();
 *   app.post('/webhooks/pixelated', express.raw({ type: '*/*' }), handleWebhook);
 */
async function handleWebhook(
  rawBody: Buffer,
  headers: Record<string, string | string[] | undefined>,
  secret: string,
): Promise<{ status: number; body: Record<string, unknown> }> {
  // 1. Extract the signature header
  const signature = headers['x-webhook-signature'];
  if (typeof signature !== 'string') {
    return {
      status: 401,
      body: { error: 'Missing X-Webhook-Signature header' },
    };
  }

  // 2. Verify the signature
  if (!verifyWebhookSignature(rawBody, signature, secret)) {
    return {
      status: 401,
      body: { error: 'Invalid webhook signature' },
    };
  }

  // 3. Parse the payload
  let payload: WebhookPayload;
  try {
    payload = JSON.parse(rawBody.toString('utf-8')) as WebhookPayload;
  } catch {
    return {
      status: 400,
      body: { error: 'Invalid JSON payload' },
    };
  }

  // 4. Dispatch to the appropriate handler
  try {
    switch (payload.eventType) {
      case WEBHOOK_EVENTS.patient_created:
        await onPatientCreated(payload);
        break;
      case WEBHOOK_EVENTS.patient_updated:
        await onPatientUpdated(payload);
        break;
      case WEBHOOK_EVENTS.encounter_created:
        await onEncounterCreated(payload);
        break;
      case WEBHOOK_EVENTS.observation_created:
        await onObservationCreated(payload);
        break;
      case WEBHOOK_EVENTS.note_signed:
        await onNoteSigned(payload);
        break;
      default:
        console.log(`Unhandled event type: ${payload.eventType}`);
    }
  } catch (err) {
    // Log the error but still return 200 to prevent retries.
    // The API retries on non-2xx responses. If your handler fails
    // transiently, return 500 to trigger a retry.
    console.error('Webhook handler error:', err);
    return {
      status: 500,
      body: { error: 'Handler failed' },
    };
  }

  return { status: 200, body: { received: true } };
}

// ---------------------------------------------------------------------------
// Event handlers
// ---------------------------------------------------------------------------

async function onPatientCreated(payload: WebhookPayload): Promise<void> {
  console.log(`Patient created: ${payload.resourceId} in tenant ${payload.tenantId}`);
  // Sync the patient to your system, trigger onboarding, etc.
}

async function onPatientUpdated(payload: WebhookPayload): Promise<void> {
  console.log(`Patient updated: ${payload.resourceId}`);
  // Update your local cache of the patient record.
}

async function onEncounterCreated(payload: WebhookPayload): Promise<void> {
  console.log(`Encounter created: ${payload.resourceId}`);
  // Notify the care team, update scheduling, etc.
}

async function onObservationCreated(payload: WebhookPayload): Promise<void> {
  console.log(`Observation created: ${payload.resourceId}`);
  // Check for alert thresholds, update dashboards, etc.
}

async function onNoteSigned(payload: WebhookPayload): Promise<void> {
  console.log(`Note signed: ${payload.resourceId}`);
  // Archive the signed note, update compliance records, etc.
}

// ---------------------------------------------------------------------------
// Express integration example (commented out, requires express)
// ---------------------------------------------------------------------------

/*
import express from 'express';

const app = express();
const WEBHOOK_SECRET = process.env.PIXELATED_WEBHOOK_SECRET!;

app.post(
  '/webhooks/pixelated',
  express.raw({ type: '*/*' }),
  async (req, res) => {
    const result = await handleWebhook(
      req.body as Buffer,
      req.headers,
      WEBHOOK_SECRET,
    );
    res.status(result.status).json(result.body);
  },
);

app.listen(3000, () => {
  console.log('Webhook server listening on port 3000');
});
*/
