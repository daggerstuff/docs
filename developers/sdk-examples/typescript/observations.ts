/**
 * TypeScript SDK Example: Observations
 *
 * Read, search, and create clinical observations through the EHR API.
 * Observations include outcome measure scores like PHQ-9 and GAD-7.
 */

import { createPixelatedClient } from '@pixelated/sdk-typescript';

const client = createPixelatedClient({
  apiKey: process.env.PIXELATED_API_KEY!,
  baseUrl: 'https://api.pixelated.com',
});

/**
 * Search observations by patient.
 *
 * At least one filter is required: patient, encounter, code, or status.
 * Combine patient with start/end to filter by date range.
 */
async function searchByPatient(patientId: string): Promise<void> {
  const result = await client.observations.list({
    patient: patientId,
    limit: 50,
    offset: 0,
  });

  console.log(`Found ${result.pagination.total} observations`);
  for (const obs of result.data) {
    console.log(
      `  ${obs.id}: ${obs.code?.coding?.[0]?.display ?? 'Unknown'} = ${obs.valueQuantity?.value ?? 'N/A'}`,
    );
  }
}

/**
 * Search observations by LOINC code.
 *
 * Use the `code` parameter to filter by LOINC code. For example,
 * `44261-6` is the PHQ-9 total score.
 */
async function searchByCode(patientId: string, loincCode: string): Promise<void> {
  const result = await client.observations.list({
    patient: patientId,
    code: loincCode,
    limit: 20,
  });

  console.log(`Found ${result.data.length} observations for code ${loincCode}`);
  for (const obs of result.data) {
    console.log(
      `  ${obs.id}: value=${obs.valueQuantity?.value} ${obs.valueQuantity?.unit ?? ''}`,
    );
  }
}

/**
 * Search observations by date range.
 *
 * Pass `patient` along with `start` and `end` (ISO timestamps) to
 * filter observations within a specific time window.
 */
async function searchByDateRange(
  patientId: string,
  startDate: string,
  endDate: string,
): Promise<void> {
  const result = await client.observations.list({
    patient: patientId,
    start: startDate,
    end: endDate,
    limit: 100,
  });

  console.log(
    `Found ${result.data.length} observations between ${startDate} and ${endDate}`,
  );
}

/**
 * Read a single observation by ID.
 */
async function readObservation(observationId: string): Promise<void> {
  try {
    const obs = await client.observations.read(observationId);
    console.log('Observation:', obs.data.id, obs.data.status);
  } catch (err) {
    if (err instanceof Error && err.message.includes('not_found')) {
      console.log(`Observation ${observationId} not found`);
      return;
    }
    throw err;
  }
}

/**
 * Create a new observation.
 *
 * Send a FHIR R4 Observation resource. The example below records a
 * PHQ-9 total score of 12 (moderate depression).
 */
async function createPhq9Observation(patientId: string): Promise<void> {
  const created = await client.observations.create({
    resourceType: 'Observation',
    status: 'final',
    subject: { reference: `Patient/${patientId}` },
    code: {
      coding: [
        {
          system: 'http://loinc.org',
          code: '44261-6',
          display: 'PHQ-9 total score',
        },
      ],
    },
    valueQuantity: {
      value: 12,
      unit: 'score',
      system: 'http://unitsofmeasure.org',
      code: '{score}',
    },
    effectiveDateTime: new Date().toISOString(),
  });

  console.log('Created observation with ID:', created.data.id);
}

/**
 * Create a GAD-7 observation.
 *
 * LOINC code 70274-6 is the GAD-7 total score.
 */
async function createGad7Observation(patientId: string): Promise<void> {
  const created = await client.observations.create({
    resourceType: 'Observation',
    status: 'final',
    subject: { reference: `Patient/${patientId}` },
    code: {
      coding: [
        {
          system: 'http://loinc.org',
          code: '70274-6',
          display: 'GAD-7 total score',
        },
      ],
    },
    valueQuantity: {
      value: 8,
      unit: 'score',
      system: 'http://unitsofmeasure.org',
      code: '{score}',
    },
    effectiveDateTime: new Date().toISOString(),
  });

  console.log('Created GAD-7 observation:', created.data.id);
}

// Run examples
const patientId = 'patient-001';
searchByPatient(patientId);
createPhq9Observation(patientId);
