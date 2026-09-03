# Linear workspace audit pipeline — runs the ETL audit + executive dashboard.
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Install dependencies (the dev set includes the runtime deps)
COPY requirements-dev.txt ./
RUN pip install --no-cache-dir -r requirements-dev.txt

COPY pyproject.toml README.md ./
COPY linear-audit/ linear-audit/
COPY tests/ tests/

# Default: run the audit pipeline in offline (local issues.json) mode.
# For a live fetch, override CMD: --fetch --team <TEAM_ID>
CMD ["python", "linear-audit/pipeline.py"]