"""Python SDK Example: Observations

Read, search, and create clinical observations through the EHR API.
Observations include outcome measure scores like PHQ-9 and GAD-7.
"""

import os
from datetime import datetime, timezone

from pixelated_sdk import ApiClient

client = ApiClient(
    api_key=os.environ["PIXELATED_API_KEY"],
    base_url="https://api.pixelated.com",
)


# ---------------------------------------------------------------------------
# Search observations by patient
# ---------------------------------------------------------------------------

# At least one filter is required: patient, encounter, code, or status.
# Combine patient with start/end to filter by date range.


def search_by_patient(patient_id: str) -> None:
    result = client.observations.list(patient=patient_id, limit=50, offset=0)

    print(f"Found {result.pagination.total} observations")
    for obs in result.data:
        display = "Unknown"
        if obs.code and obs.code.coding:
            display = obs.code.coding[0].display or "Unknown"
        value = obs.valueQuantity.value if obs.valueQuantity else "N/A"
        print(f"  {obs.id}: {display} = {value}")


# ---------------------------------------------------------------------------
# Search observations by LOINC code
# ---------------------------------------------------------------------------

# Use the `code` parameter to filter by LOINC code. For example,
# `44261-6` is the PHQ-9 total score.


def search_by_code(patient_id: str, loinc_code: str) -> None:
    result = client.observations.list(
        patient=patient_id, code=loinc_code, limit=20
    )

    print(f"Found {len(result.data)} observations for code {loinc_code}")
    for obs in result.data:
        value = obs.valueQuantity.value if obs.valueQuantity else "N/A"
        unit = obs.valueQuantity.unit if obs.valueQuantity else ""
        print(f"  {obs.id}: value={value} {unit}")


# ---------------------------------------------------------------------------
# Search observations by date range
# ---------------------------------------------------------------------------

# Pass `patient` along with `start` and `end` (ISO timestamps) to
# filter observations within a specific time window.


def search_by_date_range(
    patient_id: str, start_date: str, end_date: str
) -> None:
    result = client.observations.list(
        patient=patient_id, start=start_date, end=end_date, limit=100
    )

    print(
        f"Found {len(result.data)} observations "
        f"between {start_date} and {end_date}"
    )


# ---------------------------------------------------------------------------
# Read a single observation by ID
# ---------------------------------------------------------------------------


def read_observation(observation_id: str) -> None:
    try:
        obs = client.observations.read(observation_id)
        print(f"Observation: {obs.data.id}, status={obs.data.status}")
    except Exception as err:
        if "not_found" in str(err):
            print(f"Observation {observation_id} not found")
            return
        raise


# ---------------------------------------------------------------------------
# Create a PHQ-9 observation
# ---------------------------------------------------------------------------

# Send a FHIR R4 Observation resource. The example below records a
# PHQ-9 total score of 12 (moderate depression).


def create_phq9_observation(patient_id: str) -> None:
    created = client.observations.create(
        resourceType="Observation",
        status="final",
        subject={"reference": f"Patient/{patient_id}"},
        code={
            "coding": [
                {
                    "system": "http://loinc.org",
                    "code": "44261-6",
                    "display": "PHQ-9 total score",
                }
            ]
        },
        valueQuantity={
            "value": 12,
            "unit": "score",
            "system": "http://unitsofmeasure.org",
            "code": "{score}",
        },
        effectiveDateTime=datetime.now(timezone.utc).isoformat(),
    )

    print(f"Created observation with ID: {created.data.id}")


# ---------------------------------------------------------------------------
# Create a GAD-7 observation
# ---------------------------------------------------------------------------

# LOINC code 70274-6 is the GAD-7 total score.


def create_gad7_observation(patient_id: str) -> None:
    created = client.observations.create(
        resourceType="Observation",
        status="final",
        subject={"reference": f"Patient/{patient_id}"},
        code={
            "coding": [
                {
                    "system": "http://loinc.org",
                    "code": "70274-6",
                    "display": "GAD-7 total score",
                }
            ]
        },
        valueQuantity={
            "value": 8,
            "unit": "score",
            "system": "http://unitsofmeasure.org",
            "code": "{score}",
        },
        effectiveDateTime=datetime.now(timezone.utc).isoformat(),
    )

    print(f"Created GAD-7 observation: {created.data.id}")


if __name__ == "__main__":
    patient_id = "patient-001"
    search_by_patient(patient_id)
    create_phq9_observation(patient_id)
