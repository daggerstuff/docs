"""Python SDK Example: Patients

Read, search, create, and update patients through the EHR API.
"""

import os

from pixelated_sdk import ApiClient

client = ApiClient(
    api_key=os.environ["PIXELATED_API_KEY"],
    base_url="https://api.pixelated.com",
)


# ---------------------------------------------------------------------------
# Search patients by name
# ---------------------------------------------------------------------------

# The `q` parameter matches against patient family and given names.
# Results are paginated. Use `limit` and `offset` to page through.


def search_patients() -> None:
    result = client.patients.list(q="Smith", active="true", limit=20, offset=0)

    print(f"Found {result.pagination.total} patients")
    for patient in result.data:
        name = patient.name[0] if patient.name else None
        given = " ".join(name.given) if name and name.given else ""
        family = name.family if name else ""
        print(f"  {patient.id}: {given} {family}")


# ---------------------------------------------------------------------------
# Read a single patient by ID
# ---------------------------------------------------------------------------

# Returns the full FHIR Patient resource. Raises a not_found error
# if the patient does not exist.


def read_patient(patient_id: str) -> None:
    try:
        patient = client.patients.read(patient_id)
        print(f"Patient: {patient.data.id}, active={patient.data.active}")
    except Exception as err:
        if "not_found" in str(err):
            print(f"Patient {patient_id} not found")
            return
        raise


# ---------------------------------------------------------------------------
# Create a new patient
# ---------------------------------------------------------------------------

# Send a FHIR R4 Patient resource in the body. The response includes
# the created patient with a server-assigned ID.


def create_patient() -> None:
    new_patient = client.patients.create(
        name=[{"family": "Doe", "given": ["John"]}],
        birthDate="1990-06-15",
        gender="male",
        telecom=[
            {"system": "phone", "value": "555-0199"},
            {"system": "email", "value": "john.doe@example.com"},
        ],
        address=[
            {
                "line": ["456 Oak Ave"],
                "city": "Portland",
                "state": "OR",
                "postalCode": "97201",
            }
        ],
        active=True,
    )

    print(f"Created patient with ID: {new_patient.data.id}")


# ---------------------------------------------------------------------------
# Update an existing patient
# ---------------------------------------------------------------------------

# Send the full patient resource. Partial updates are not supported.
# The response returns the updated resource.


def update_patient(patient_id: str) -> None:
    updated = client.patients.update(
        patient_id,
        name=[{"family": "Doe", "given": ["John", "Michael"]}],
        birthDate="1990-06-15",
        gender="male",
        active=True,
    )

    print(f"Updated patient: {updated.data.id}")


# ---------------------------------------------------------------------------
# Paginate through all active patients
# ---------------------------------------------------------------------------

# Loop until the data array is empty. Stop if `total` is available
# and the offset exceeds it.


def list_all_active_patients() -> None:
    limit = 100
    offset = 0
    total = float("inf")
    all_ids: list[str] = []

    while offset < total:
        page = client.patients.list(active="true", limit=limit, offset=offset)

        for patient in page.data:
            all_ids.append(patient.id)

        if page.pagination.total is not None:
            total = page.pagination.total

        if len(page.data) < limit:
            break
        offset += limit

    print(f"Total active patients: {len(all_ids)}")


if __name__ == "__main__":
    search_patients()
    create_patient()
