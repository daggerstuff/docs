/**
 * TypeScript SDK Example: Authentication
 *
 * Shows how to initialize the Pixelated client with API key auth,
 * configure the base URL, and verify connectivity.
 *
 * Install: pnpm add @pixelated/sdk-typescript
 */

import { createPixelatedClient } from '@pixelated/sdk-typescript';

/**
 * Basic client initialization.
 *
 * The client sends the API key in the X-API-Key header on every request.
 * Set the key via an environment variable. Never hardcode it in source.
 */
const client = createPixelatedClient({
  apiKey: process.env.PIXELATED_API_KEY!,
  baseUrl: 'https://api.pixelated.com',
});

/**
 * Client with custom timeout and retry configuration.
 *
 * The SDK retries on 429 responses and network errors by default.
 * Override the defaults when you need tighter or looser bounds.
 */
const clientWithRetry = createPixelatedClient({
  apiKey: process.env.PIXELATED_API_KEY!,
  baseUrl: 'https://api.pixelated.com',
  timeout: 10_000,
  maxRetries: 5,
  retryDelay: 500,
});

/**
 * Client targeting the sandbox environment.
 *
 * Use the sandbox for development. The base URL is the same, but the
 * API key routes requests to the sandbox tenant.
 */
const sandboxClient = createPixelatedClient({
  apiKey: process.env.PIXELATED_SANDBOX_KEY!,
  baseUrl: 'https://api.pixelated.com',
});

/**
 * Verify connectivity by calling a lightweight endpoint.
 *
 * If the key is invalid, the SDK throws an error with status 401 and
 * code "unauthorized". If the key lacks scope, you get 403 "forbidden".
 */
async function verifyConnection(): Promise<void> {
  try {
    const patients = await client.patients.list({ limit: 1 });
    console.log('Connection OK. Patient count:', patients.pagination.total);
  } catch (err) {
    if (err instanceof Error) {
      console.error('Connection failed:', err.message);
    }
    throw err;
  }
}

verifyConnection();
