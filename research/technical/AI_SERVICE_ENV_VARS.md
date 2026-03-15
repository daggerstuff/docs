# AI Service Environment Variables

This document defines the environment variables used by the AI Service (`src/lib/ai/services/server.ts`) and the AI Provider Registry (`src/lib/ai/providers.ts`).

## Provider Keys

The following keys are required to enable respective AI providers:

| Variable | Provider | Description |
| :--- | :--- | :--- |
| `TOGETHER_API_KEY` | Together AI | API key for legacy and high-throughput completions. |
| `OPENAI_API_KEY` | OpenAI | API key for GPT-4 and other models. |
| `ANTHROPIC_API_KEY` | Anthropic | API key for Claude models. |
| `AZURE_OPENAI_API_KEY` | Azure OpenAI | API key for Azure-hosted OpenAI models. |
| `AZURE_OPENAI_ENDPOINT` | Azure OpenAI | The endpoint URL for your Azure OpenAI resource. |
| `HUGGINGFACE_API_KEY` | Hugging Face | API key for Hugging Face Inference API. |

## Service Configuration

| Variable | Default | Description |
| :--- | :--- | :--- |
| `PORT` | `8002` | The port the internal AI server listens on. |
| `LOCAL_AI_BASE_URL` | `http://localhost:8000/v1` | Base URL for the local GGUF/Wayfarer inference service. |
| `AI_PROVIDER_PREFERENCE` | `local,together,openai,anthropic,huggingface` | A comma-separated list of provider names in order of preference. |

## Provider Preference Logic

The AI Service uses the `AI_PROVIDER_PREFERENCE` variable to determine which provider to use when no specific provider is requested by the client.

1.  The comma-separated string is split and trimmed.
2.  The service iterates through the list.
3.  The first provider that is **initialized** (i.e., has an API key or is `local`) is selected.
4.  If none of the preferred providers are available, it falls back to a hardcoded default list in the same order.

## Sentry Instrumentation

The AI server is instrumented with Sentry. To ensure correct tracing and error reporting:

-   `src/lib/ai/services/server.ts` imports `config/instrument.mjs` at the very top.
-   `SENTRY_DSN` must be set for reports to be sent.
-   Metrics for API response time and emotion analysis latency are automatically recorded.

## Usage Example

```bash
# Set preference to use Together AI first, then local, then OpenAI
export AI_PROVIDER_PREFERENCE="together,local,openai"
export TOGETHER_API_KEY="your-key-here"

# Start the services
pnpm dev:all-services
```
