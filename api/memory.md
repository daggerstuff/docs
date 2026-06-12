# Memory API Documentation

**Version:** 1.0.0 **Base URL:** `/api/memory` **Authentication:** Bearer Token
(JWT)

The Memory API provides a unified interface for storing, retrieving, and
managing therapeutic conversation memories with rich metadata and emotional
context.

## Table of Contents

1. [Authentication](#authentication)
2. [Error Handling](#error-handling)
3. [Common Response Format](#common-response-format)
4. [Endpoints](#endpoints)
   - [Create Memory](#create-memory)
   - [Get Memory](#get-memory)
   - [Update Memory](#update-memory)
   - [Delete Memory](#delete-memory)
   - [List Memories](#list-memories)
   - [Search Memories](#search-memories)
   - [Memory Statistics](#memory-statistics)
5. [Data Models](#data-models)
   - [UnifiedMemory](#unifiedmemory)
   - [EmotionalContext](#emotionalcontext)
   - [EmpathyMetrics](#empathymetrics)

## Authentication

All API requests require authentication using a Bearer Token in the
Authorization header:

```http
Authorization: Bearer YOUR_JWT_TOKEN
```

## Error Handling

All API responses follow a standardized format:

### Success Response

```json
{
  "success": true,
  "data": {...},
  "message": "Success message"
}
```

### Error Response

```json
{
  "success": false,
  "error": "ERROR_CODE",
  "message": "Human-readable error message",
  "details": "Additional error details (optional)"
}
```

### HTTP Status Codes

- `200` - Success
- `201` - Created
- `400` - Bad Request
- `401` - Unauthorized
- `403` - Forbidden
- `404` - Not Found
- `429` - Too Many Requests
- `500` - Internal Server Error

## Common Response Format

All API responses follow the same structure:

```json
{
  "success": boolean,
  "data": object|array|null,
  "message": string
}
```

## Endpoints

### Create Memory

Creates a new memory record in the unified memory system.

**Endpoint:** `POST /api/memory`

**Request Body:**

```json
{
  "content": "string (required)",
  "scope": "session|arc|trait|fact (optional)",
  "retention": "ephemeral|short_term|long_term|permanent (optional)",
  "category": "string (optional)",
  "tags": ["string"] (optional),
  "importance": "number (0-1, optional)",
  "emotionalContext": {
    "valence": "number (-1 to 1)",
    "arousal": "number (0 to 1)",
    "dominance": "number (0 to 1)",
    "primaryEmotion": "string",
    "intensity": "number (0 to 1)"
  } (optional),
  "empathyMetrics": {
    "reciprocity": "number (0 to 1)",
    "validationAccuracy": "number (0 to 1)",
    "resistanceLevel": "number (0 to 1)"
  } (optional)
}
```

**Response:**

```json
{
  "success": true,
  "data": {
    "id": "string",
    "content": "string",
    "metadata": "object"
  },
  "message": "Memory created successfully"
}
```

**Example Request:**

```bash
curl -X POST "https://api.pixelatedempathy.com/api/memory" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "Patient expressed concerns about work-life balance and mentioned feeling overwhelmed with upcoming deadlines.",
    "scope": "session",
    "category": "conversation",
    "tags": ["work_stress", "overwhelm"],
    "importance": 0.8,
    "emotionalContext": {
      "valence": -0.6,
      "arousal": 0.7,
      "dominance": 0.3,
      "primaryEmotion": "anxiety",
      "intensity": 0.65
    }
  }'
```

**Example Response:**

```json
{
  "success": true,
  "data": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "content": "Patient expressed concerns about work-life balance and mentioned feeling overwhelmed with upcoming deadlines.",
    "metadata": {
      "scope": "session",
      "category": "conversation",
      "tags": ["work_stress", "overwhelm"],
      "importance": 0.8
    }
  },
  "message": "Memory created successfully"
}
```

### Get Memory

Retrieves a specific memory record by its ID.

**Endpoint:** `GET /api/memory/{memoryId}`

**Response:**

```json
{
  "success": true,
  "data": {
    "id": "string",
    "content": "string",
    "metadata": "object",
    "createdAt": "string (ISO 8601)",
    "updatedAt": "string (ISO 8601)"
  },
  "message": "Memory retrieved successfully"
}
```

**Example Request:**

```bash
curl -X GET "https://api.pixelatedempathy.com/api/memory/550e8400-e29b-41d4-a716-446655440000" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

**Example Response:**

```json
{
  "success": true,
  "data": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "content": "Patient expressed concerns about work-life balance and mentioned feeling overwhelmed with upcoming deadlines.",
    "metadata": {
      "scope": "session",
      "category": "conversation",
      "tags": ["work_stress", "overwhelm"],
      "importance": 0.8,
      "emotionalContext": {
        "valence": -0.6,
        "arousal": 0.7,
        "dominance": 0.3,
        "primaryEmotion": "anxiety",
        "intensity": 0.65
      }
    },
    "createdAt": "2026-06-11T10:30:00Z",
    "updatedAt": "2026-06-11T10:30:00Z"
  },
  "message": "Memory retrieved successfully"
}
```

### Update Memory

Updates an existing memory record.

**Endpoint:** `PATCH /api/memory/{memoryId}`

**Request Body:**

```json
{
  "content": "string (optional)",
  "scope": "session|arc|trait|fact (optional)",
  "retention": "ephemeral|short_term|long_term|permanent (optional)",
  "category": "string (optional)",
  "tags": ["string"] (optional),
  "importance": "number (0-1, optional)",
  "emotionalContext": {
    "valence": "number (-1 to 1)",
    "arousal": "number (0 to 1)",
    "dominance": "number (0 to 1)",
    "primaryEmotion": "string",
    "intensity": "number (0 to 1)"
  } (optional),
  "empathyMetrics": {
    "reciprocity": "number (0 to 1)",
    "validationAccuracy": "number (0 to 1)",
    "resistanceLevel": "number (0 to 1)"
  } (optional)
}
```

**Response:**

```json
{
  "success": true,
  "data": {
    "id": "string",
    "content": "string",
    "metadata": "object"
  },
  "message": "Memory updated successfully"
}
```

**Example Request:**

```bash
curl -X PATCH "https://api.pixelatedempathy.com/api/memory/550e8400-e29b-41d4-a716-446655440000" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "Patient expressed concerns about work-life balance and mentioned feeling overwhelmed with upcoming deadlines. Discussed time management strategies.",
    "tags": ["work_stress", "overwhelm", "time_management"]
  }'
```

**Example Response:**

```json
{
  "success": true,
  "data": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "content": "Patient expressed concerns about work-life balance and mentioned feeling overwhelmed with upcoming deadlines. Discussed time management strategies.",
    "metadata": {
      "scope": "session",
      "category": "conversation",
      "tags": ["work_stress", "overwhelm", "time_management"],
      "importance": 0.8,
      "emotionalContext": {
        "valence": -0.6,
        "arousal": 0.7,
        "dominance": 0.3,
        "primaryEmotion": "anxiety",
        "intensity": 0.65
      }
    }
  },
  "message": "Memory updated successfully"
}
```

### Delete Memory

Deletes a memory record by its ID.

**Endpoint:** `DELETE /api/memory/{memoryId}`

**Response:**

```json
{
  "success": true,
  "message": "Memory deleted successfully"
}
```

**Example Request:**

```bash
curl -X DELETE "https://api.pixelatedempathy.com/api/memory/550e8400-e29b-41d4-a716-446655440000" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

**Example Response:**

```json
{
  "success": true,
  "message": "Memory deleted successfully"
}
```

### List Memories

Lists memories with optional filtering and pagination.

**Endpoint:** `GET /api/memory`

**Query Parameters:**

| Parameter       | Type    | Description                                                  |
| --------------- | ------- | ------------------------------------------------------------ |
| `category`      | string  | Filter by category                                           |
| `scope`         | string  | Filter by scope (session, arc, trait, fact)                  |
| `retention`     | string  | Filter by retention policy                                   |
| `tag`           | string  | Filter by tag (can be used multiple times)                   |
| `minImportance` | number  | Minimum importance score (0-1)                               |
| `sortBy`        | string  | Sort by field (createdAt, updatedAt, importance, accessedAt) |
| `sortOrder`     | string  | Sort order (asc, desc)                                       |
| `limit`         | integer | Number of results (default: 10, max: 100)                    |
| `offset`        | integer | Offset for pagination (default: 0)                           |

**Response:**

```json
{
  "success": true,
  "data": {
    "memories": [
      {
        "id": "string",
        "content": "string",
        "metadata": "object",
        "createdAt": "string (ISO 8601)",
        "updatedAt": "string (ISO 8601)"
      }
    ],
    "pagination": {
      "limit": "integer",
      "offset": "integer",
      "total": "integer"
    }
  },
  "message": "Memories retrieved successfully"
}
```

**Example Request:**

```bash
curl -X GET "https://api.pixelatedempathy.com/api/memory?category=conversation&tag=work_stress&limit=5" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

**Example Response:**

```json
{
  "success": true,
  "data": {
    "memories": [
      {
        "id": "550e8400-e29b-41d4-a716-446655440000",
        "content": "Patient expressed concerns about work-life balance and mentioned feeling overwhelmed with upcoming deadlines.",
        "metadata": {
          "scope": "session",
          "category": "conversation",
          "tags": ["work_stress", "overwhelm"],
          "importance": 0.8
        },
        "createdAt": "2026-06-11T10:30:00Z",
        "updatedAt": "2026-06-11T10:30:00Z"
      }
    ],
    "pagination": {
      "limit": 5,
      "offset": 0,
      "total": 1
    }
  },
  "message": "Memories retrieved successfully"
}
```

### Search Memories

Searches memories using text-based queries with optional filtering.

**Endpoint:** `GET /api/memory/search?q={query}`

**Query Parameters:**

| Parameter       | Type    | Description                                 |
| --------------- | ------- | ------------------------------------------- |
| `q`             | string  | Search query (required)                     |
| `category`      | string  | Filter by category                          |
| `scope`         | string  | Filter by scope (session, arc, trait, fact) |
| `retention`     | string  | Filter by retention policy                  |
| `tag`           | string  | Filter by tag (can be used multiple times)  |
| `minImportance` | number  | Minimum importance score (0-1)              |
| `limit`         | integer | Number of results (default: 10, max: 100)   |
| `offset`        | integer | Offset for pagination (default: 0)          |

**Response:**

```json
{
  "success": true,
  "data": {
    "memories": [
      {
        "id": "string",
        "content": "string",
        "metadata": "object",
        "createdAt": "string (ISO 8601)",
        "updatedAt": "string (ISO 8601)"
      }
    ],
    "query": "string",
    "pagination": {
      "limit": "integer",
      "offset": "integer",
      "total": "integer"
    }
  },
  "message": "Memories searched successfully"
}
```

**Example Request:**

```bash
curl -X GET "https://api.pixelatedempathy.com/api/memory/search?q=work-life%20balance&category=conversation" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

**Example Response:**

```json
{
  "success": true,
  "data": {
    "memories": [
      {
        "id": "550e8400-e29b-41d4-a716-446655440000",
        "content": "Patient expressed concerns about work-life balance and mentioned feeling overwhelmed with upcoming deadlines.",
        "metadata": {
          "scope": "session",
          "category": "conversation",
          "tags": ["work_stress", "overwhelm"],
          "importance": 0.8
        },
        "createdAt": "2026-06-11T10:30:00Z",
        "updatedAt": "2026-06-11T10:30:00Z"
      }
    ],
    "query": "work-life balance",
    "pagination": {
      "limit": 10,
      "offset": 0,
      "total": 1
    }
  },
  "message": "Memories searched successfully"
}
```

### Memory Statistics

Retrieves statistics about memory usage and distribution.

**Endpoint:** `GET /api/memory/stats`

**Query Parameters:**

| Parameter   | Type   | Description                                 |
| ----------- | ------ | ------------------------------------------- |
| `category`  | string | Filter by category                          |
| `scope`     | string | Filter by scope (session, arc, trait, fact) |
| `retention` | string | Filter by retention policy                  |

**Response:**

```json
{
  "success": true,
  "data": {
    "totalMemories": "integer",
    "categoryCounts": {
      "categoryName": "integer"
    }
  },
  "message": "Memory statistics retrieved successfully"
}
```

**Example Request:**

```bash
curl -X GET "https://api.pixelatedempathy.com/api/memory/stats" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

**Example Response:**

```json
{
  "success": true,
  "data": {
    "totalMemories": 1247,
    "categoryCounts": {
      "conversation": 842,
      "fact": 205,
      "preference": 120,
      "crisis": 80
    }
  },
  "message": "Memory statistics retrieved successfully"
}
```

## Data Models

### UnifiedMemory

The canonical memory object shared by all Pixelated services.

| Field              | Type                   | Description                                                    |
| ------------------ | ---------------------- | -------------------------------------------------------------- |
| `id`               | string (UUID)          | Globally unique identifier                                     |
| `tenantId`         | string                 | Tenant identifier for multi-tenant isolation                   |
| `userId`           | string                 | User identifier                                                |
| `bankId`           | string                 | Memory bank identifier                                         |
| `content`          | string                 | Primary memory content                                         |
| `scope`            | string                 | Semantic scope (session, arc, trait, fact)                     |
| `retention`        | string                 | Retention policy (ephemeral, short_term, long_term, permanent) |
| `category`         | string                 | Category label for filtering                                   |
| `tags`             | array[string]          | Free-form tags for filtering                                   |
| `version`          | integer                | Version counter                                                |
| `schemaVersion`    | string                 | Schema version identifier                                      |
| `sourceService`    | string                 | Service that created this memory                               |
| `importance`       | number (0-1)           | Current importance score                                       |
| `decayRate`        | number                 | Per-memory decay rate                                          |
| `strengthTrend`    | string                 | Current strength trend                                         |
| `activationCount`  | integer                | Number of times activated                                      |
| `retrievalCount`   | integer                | Number of times retrieved                                      |
| `isGhost`          | boolean                | Whether this is a Ghost Node                                   |
| `gist`             | string/null            | 10-word summary                                                |
| `synthesizedFrom`  | array[string]          | Source memory IDs                                              |
| `vectorId`         | string/null            | Vector store reference                                         |
| `emotionalContext` | EmotionalContext/null  | Emotional metadata                                             |
| `empathyMetrics`   | EmpathyMetrics/null    | Empathy quality metrics                                        |
| `createdAt`        | string (ISO 8601)      | Creation timestamp                                             |
| `updatedAt`        | string/null (ISO 8601) | Last update timestamp                                          |
| `accessedAt`       | string/null (ISO 8601) | Last access timestamp                                          |
| `lastRetrievedAt`  | string/null (ISO 8601) | Last retrieval timestamp                                       |

### EmotionalContext

Emotional metadata anchored to Plutchik's Wheel of Emotions.

| Field            | Type             | Description                     |
| ---------------- | ---------------- | ------------------------------- |
| `valence`        | number (-1 to 1) | Emotional positivity/negativity |
| `arousal`        | number (0 to 1)  | Emotional activation level      |
| `dominance`      | number (0 to 1)  | Sense of control/power          |
| `primaryEmotion` | string           | Primary detected emotion        |
| `intensity`      | number (0 to 1)  | Emotional intensity             |

### EmpathyMetrics

Empathy quality metrics derived from therapeutic interactions.

| Field                | Type            | Description                      |
| -------------------- | --------------- | -------------------------------- |
| `reciprocity`        | number (0 to 1) | Participant's empathy matching   |
| `validationAccuracy` | number (0 to 1) | Accuracy of emotional validation |
| `resistanceLevel`    | number (0 to 1) | Resistance to perspective shift  |
