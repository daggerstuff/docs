# OVH AI Training: Troubleshooting & Best Practices

This document records the critical configuration fixes required for running
Pixelated Empathy AI jobs on OVHcloud AI Platform.

## 🛑 Common Failure Modes

### 1. Exit Code 2 (Immediate Crash)

**Symptom**: The job fails within seconds with no logs or a generic "Exit Code
2". **Root Cause**: Permission mismatch. OVH forces containers to run as **UID
42420** (`ovhcloud`), ignoring the `USER` instruction in the Dockerfile. If your
app tries to write to directories owned by another user (e.g., UID 1000
`ubuntu`), it will crash early. **Resolution**:

- Explicitly create and use UID 42420 in the Dockerfile.
- Ensure all app directories (`/app`, `/app/logs`, `/app/tmp`) are recursively
  owned by 42420.

### 2. ModuleNotFoundError / ImportError

**Symptom**: `No module named 'ai.core'` even though the directory exists.
**Root Cause**: PYTHONPATH Paradox. If the source code is copied into
`/app/ai/`, setting `PYTHONPATH=/app/ai` will cause Python to look _inside_ that
folder for an `ai` package, which it won't find. **Resolution**:

- Set `PYTHONPATH=/app`.
- This allows `from ai.core import ...` to correctly resolve because Python sees
  the `ai/` folder inside `/app`.

### 3. "Ghost" Code (Stale Image)

**Symptom**: You push a fix, but the logs show old code or an old file
structure. **Root Cause**: OVH nodes cache the `:latest` tag locally. If a node
already has a `:latest` image, it may not re-pull even if you pushed a new
revision to Docker Hub. **Resolution**:

- **Never use `:latest` for active development.**
- Use unique, timestamped tags (e.g., `v1772392159`).
- Update your deployment script to generate these tags dynamically.

---

## 🛠️ Dockerfile Best Practices (OVH-Ready)

Ensure your production stage looks like this:

```dockerfile
# OVH AI Training runs as UID 42420
RUN groupadd -g 42420 ovhcloud && \
    useradd -u 42420 -g 42420 -m -s /bin/bash ovhcloud

WORKDIR /app
COPY . ai/

# Set ownership to OVH user
RUN chown -R 42420:42420 /app
USER 42420

CMD ["python", "-m", "ai.api.main"]
```

## 🚀 Running the Job

Always specify `PYTHONPATH` in the environment variables:

```bash
ovhai job run \
  --env PYTHONPATH="/app" \
  docker.io/pixelatedempathy/training-node:v<TIMESTAMP> \
  -- python /app/ai/training/scripts/batch_regenerate.py ...
```
