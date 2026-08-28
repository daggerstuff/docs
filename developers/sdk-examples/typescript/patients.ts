/**
 * TypeScript SDK Example: Patients
 *
 * Read, search, create, and update patients through the EHR API.
 */

import { createPixelatedClient } from '@pixelated/sdk-typescript';

const client = createPixelatedClient({
  apiKey: process.env.PIXELATED_API_KEY!,
  baseUrl: 'https://api.pixelated.com',
});

/**
 * Search patients by name.
 *
 * The `q` parameter matches against patient family and given names.
 * Results are paginated. Use `limit` and `offset` to page through.
 */
async function searchPatients(): Promise<void> {
  const result = await client.patients.list({
    q: 'Smith',
    active: 'true',
    limit: 20,
    offset: 0,
  });

  console.log(`Found ${result.pagination.total} patients`);
  for (const patient of result.data) {
    const name = patient.name?.[0];
    console.log(`  ${patient.id}: ${name?.given?.join(' ')} ${name?.family}`);
  }
}

/**
 * Read a single patient by ID.
 *
 * Returns the full FHIR Patient resource. Throws a not_found error
 * if the patient does not exist.
 */
async function readPatient(patientId: string): Promise<void> {
  try {
    const patient = await client.patients.read(patientId);
    console.log('Patient:', patient.data.id, patient.data.active);
  } catch (err) {
    if (err instanceof Error && err.message.includes('not_found')) {
      console.log(`Patient ${patientId} not found`);
      return;
    }
    throw err;
  }
}

/**
 * Create a new patient.
 *
 * Send a FHIR R4 Patient resource in the body. The response includes
 * the created patient with a server-assigned ID.
 */
async function createPatient(): Promise<void> {
  const newPatient = await client.patients.create({
    name: [
      {
        family: 'Doe',
        given: ['John'],
      },
    ],
    birthDate: '1990-06-15',
    gender: 'male',
    telecom: [
      { system: 'phone', value: '555-0199' },
      { system: 'email', value: 'john.doe@example.com' },
    ],
    address: [
      {
        line: ['456 Oak Ave'],
        city: 'Portland',
        state: 'OR',
        postalCode: '97201',
      },
    ],
    active: true,
  });

  console.log('Created patient with ID:', newPatient.data.id);
}

/**
 * Update an existing patient.
 *
 * Send the full patient resource. Partial updates are not supported.
 * The response returns the updated resource.
 */
async function updatePatient(patientId: string): Promise<void> {
  const updated = await client.patients.update(patientId, {
    name: [
      {
        family: 'Doe',
        given: ['John', 'Michael'],
      },
    ],
    birthDate: '1990-06-15',
    gender: 'male',
    active: true,
  });

  console.log('Updated patient:', updated.data.id);
}

/**
 * Paginate through all active patients.
 *
 * Loop until the data array is empty. Stop if `total` is available
 * and the offset exceeds it.
 */
async function listAllActivePatients(): Promise<void> {
  const limit = 100;
  let offset = 0;
  let total = Infinity;
  const allIds: string[] = [];

  while (offset < total) {
    const page = await client.patients.list({
      active: 'true',
      limit,
      offset,
    });

    for (const patient of page.data) {
      allIds.push(patient.id);
    }

    if (page.pagination.total !== undefined) {
      total = page.pagination.total;
    }

    if (page.data.length < limit) break;
    offset += limit;
  }

  console.log(`Total active patients: ${allIds.length}`);
}

searchPatients().then(() => createPatient());
