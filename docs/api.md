# API Documentation

Complete API reference for the Autonomous AI Operator.

## Base URL

```
https://api.autonomous-ai-operator.com
```

## Authentication

Most endpoints require JWT authentication. Include the token in the Authorization header:

```
Authorization: Bearer <your-jwt-token>
```

## Common Response Formats

### Success Response

```json
{
  "success": true,
  "data": { ... },
  "message": "Operation successful"
}
```

### Error Response

```json
{
  "success": false,
  "error": {
    "code": "ERROR_CODE",
    "message": "Error description",
    "details": { ... }
  }
}
```

## Voice Endpoints

### Twilio Webhook

Handle incoming and outgoing Twilio calls.

**Endpoint:** `POST /api/voice/webhook/twilio`

**Headers:**
```
Content-Type: application/x-www-form-urlencoded
Twilio-Signature: <twilio-signature>
```

**Parameters:**
- `CallSid`: Twilio call SID
- `CallStatus`: Call status (ringing, in-progress, completed, etc.)
- `From`: Caller phone number
- `To`: Receiver phone number
- `Digits`: Digits pressed by caller (if any)
- `RecordingUrl`: URL of recorded audio (if call ended)

**Response:** TwiML or 200 OK

**Example Request:**
```
POST /api/voice/webhook/twilio
Content-Type: application/x-www-form-urlencoded

CallSid=CA1234567890&CallStatus=in-progress&From=+18005551234&To=+18005551235
```

### Vapi Real-Time Stream

Handle real-time voice conversations via Vapi.ai.

**Endpoint:** `POST /api/voice/vapi/stream`

**Headers:**
```
Content-Type: application/json
Authorization: Bearer <your-jwt-token>
```

**Request Body:**
```json
{
  "session_id": "vapi-session-123",
  "audio": "base64-encoded-audio-chunk",
  "conversation_state": {
    "current_step": "gathering_info",
    "previous_response": "I can help you cancel your Comcast account. What's your account number?"
  }
}
```

**Response:**
```json
{
  "session_id": "vapi-session-123",
  "audio": "base64-encoded-audio-chunk",
  "next_action": "place_call",
  "tool_invocation": {
    "tool": "place_call",
    "arguments": {
      "phone_number": "+18005551234"
    }
  }
}
```

### Get Call Status

Retrieve current call status and transcript.

**Endpoint:** `GET /api/voice/status/{task_id}`

**Headers:**
```
Authorization: Bearer <your-jwt-token>
```

**Response:**
```json
{
  "success": true,
  "data": {
    "task_id": "uuid",
    "state": "CALL_IN_PROGRESS",
    "current_step": "gathering_info",
    "transcript": [
      {
        "role": "user",
        "content": "Cancel my Comcast account",
        "timestamp": "2024-01-01T00:00:00Z"
      },
      {
        "role": "assistant",
        "content": "I can help you with that. What's your account number?",
        "timestamp": "2024-01-01T00:00:01Z"
      }
    ],
    "next_action": "place_call",
    "confidence": 0.94
  }
}
```

## Email Endpoints

### Email Webhook

Handle email events (sent, delivered, opened, etc.).

**Endpoint:** `POST /api/email/webhook`

**Headers:**
```
Content-Type: application/json
X-Webhook-Secret: <webhook-secret>
```

**Request Body:**
```json
{
  "event": "sent",
  "message_id": "msg-123",
  "to": "user@example.com",
  "from": "noreply@autonomous-ai-operator.com",
  "subject": "[AI Operator] Task Summary",
  "timestamp": "2024-01-01T00:00:00Z"
}
```

**Response:** 200 OK

### Poll Inbox

Poll IMAP inbox for unread messages.

**Endpoint:** `GET /api/email/inbox`

**Headers:**
```
Authorization: Bearer <your-jwt-token>
```

**Query Parameters:**
- `limit` (optional): Maximum number of messages (default: 10)
- `since` (optional): Only messages since this timestamp

**Response:**
```json
{
  "success": true,
  "data": {
    "total": 2,
    "messages": [
      {
        "id": "msg-123",
        "from": "user@example.com",
        "subject": "Cancel my Comcast account",
        "body": "Please cancel my Comcast account...",
        "timestamp": "2024-01-01T00:00:00Z",
        "attachments": []
      }
    ]
  }
}
```

## Task Endpoints

### Create Task

Create a new autonomous task.

**Endpoint:** `POST /api/tasks`

**Headers:**
```
Authorization: Bearer <your-jwt-token>
Content-Type: application/json
```

**Request Body:**
```json
{
  "goal": "Cancel my Comcast account",
  "user_id": "uuid",
  "metadata": {
    "company": "Comcast",
    "priority": "high"
  }
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "task_id": "uuid",
    "goal": "Cancel my Comcast account",
    "state": "INIT",
    "created_at": "2024-01-01T00:00:00Z",
    "metadata": {
      "company": "Comcast",
      "priority": "high"
    }
  }
}
```

### Get Task Details

Retrieve task details and execution status.

**Endpoint:** `GET /api/tasks/{task_id}`

**Headers:**
```
Authorization: Bearer <your-jwt-token>
```

**Response:**
```json
{
  "success": true,
  "data": {
    "task_id": "uuid",
    "user_id": "uuid",
    "goal": "Cancel my Comcast account",
    "state": "CALL_IN_PROGRESS",
    "current_step": "gathering_info",
    "plan": [
      {
        "step": 1,
        "action": "retrieve_credentials",
        "status": "completed",
        "result": "Account number: 1234567890"
      },
      {
        "step": 2,
        "action": "research_contact",
        "status": "completed",
        "result": "Found official number: +18005551234"
      },
      {
        "step": 3,
        "action": "place_call",
        "status": "in_progress",
        "result": null
      }
    ],
    "metadata": {
      "company": "Comcast",
      "priority": "high"
    },
    "created_at": "2024-01-01T00:00:00Z",
    "updated_at": "2024-01-01T00:01:00Z"
  }
}
```

### Get Task Logs

Retrieve task execution logs.

**Endpoint:** `GET /api/tasks/{task_id}/logs`

**Headers:**
```
Authorization: Bearer <your-jwt-token>
```

**Query Parameters:**
- `limit` (optional): Maximum number of logs (default: 100)
- `offset` (optional): Offset for pagination (default: 0)

**Response:**
```json
{
  "success": true,
  "data": {
    "total": 50,
    "logs": [
      {
        "log_id": "uuid",
        "task_id": "uuid",
        "event_type": "task_created",
        "payload": {
          "goal": "Cancel my Comcast account",
          "user_id": "uuid"
        },
        "timestamp": "2024-01-01T00:00:00Z"
      },
      {
        "log_id": "uuid",
        "task_id": "uuid",
        "event_type": "intent_confirmed",
        "payload": {
          "intent": "cancel_service",
          "company": "Comcast",
          "confidence": 0.94
        },
        "timestamp": "2024-01-01T00:00:01Z"
      }
    ]
  }
}
```

### Execute Task

Trigger task execution.

**Endpoint:** `POST /api/tasks/{task_id}/execute`

**Headers:**
```
Authorization: Bearer <your-jwt-token>
```

**Response:**
```json
{
  "success": true,
  "data": {
    "task_id": "uuid",
    "state": "GATHER_INFO",
    "message": "Task execution started"
  }
}
```

### Replan Task

Force task replanning.

**Endpoint:** `POST /api/tasks/{task_id}/replan`

**Headers:**
```
Authorization: Bearer <your-jwt-token>
```

**Request Body:**
```json
{
  "reason": "tool_failed",
  "new_plan": [
    {
      "action": "research_alternative",
      "parameters": { ... }
    }
  ]
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "task_id": "uuid",
    "new_plan": [
      {
        "step": 1,
        "action": "research_alternative",
        "parameters": { ... }
      }
    ],
    "message": "Task replanned successfully"
  }
}
```

## Memory Endpoints

### Semantic Search

Search semantic memory using vector embeddings.

**Endpoint:** `GET /api/memory/{user_id}/semantic`

**Headers:**
```
Authorization: Bearer <your-jwt-token>
```

**Query Parameters:**
- `query` (required): Search query
- `limit` (optional): Maximum results (default: 5)
- `min_similarity` (optional): Minimum similarity score (default: 0.7)

**Response:**
```json
{
  "success": true,
  "data": {
    "user_id": "uuid",
    "query": "Comcast account",
    "results": [
      {
        "id": "uuid",
        "content": "Comcast account number: 1234567890",
        "similarity": 0.92,
        "metadata": {
          "type": "account_info",
          "company": "Comcast"
        },
        "created_at": "2024-01-01T00:00:00Z"
      }
    ]
  }
}
```

### Store Memory

Store new memory in semantic memory.

**Endpoint:** `POST /api/memory/{user_id}`

**Headers:**
```
Authorization: Bearer <your-jwt-token>
Content-Type: application/json
```

**Request Body:**
```json
{
  "content": "Comcast account number: 1234567890",
  "metadata": {
    "type": "account_info",
    "company": "Comcast",
    "category": "credentials"
  }
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "memory_id": "uuid",
    "user_id": "uuid",
    "content": "Comcast account number: 1234567890",
    "metadata": {
      "type": "account_info",
      "company": "Comcast",
      "category": "credentials"
    },
    "created_at": "2024-01-01T00:00:00Z"
  }
}
```

### Get Vault

Retrieve user's secure vault.

**Endpoint:** `GET /api/memory/{user_id}/vault`

**Headers:**
```
Authorization: Bearer <your-jwt-token>
```

**Response:**
```json
{
  "success": true,
  "data": {
    "user_id": "uuid",
    "vault": [
      {
        "company": "Comcast",
        "account_number": "1234567890",
        "metadata": {
          "type": "cable",
          "created_at": "2024-01-01T00:00:00Z"
        }
      }
    ]
  }
}
```

## Health & Monitoring

### Health Check

Check service health.

**Endpoint:** `GET /health`

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2024-01-01T00:00:00Z",
  "services": {
    "database": "healthy",
    "redis": "healthy",
    "llm": "healthy"
  }
}
```

### Metrics

Get Prometheus metrics.

**Endpoint:** `GET /metrics`

**Response:**
```
# HELP task_success_rate Task success rate
# TYPE task_success_rate gauge
task_success_rate{task_id="uuid"} 0.95

# HELP average_execution_time Average task execution time in seconds
# TYPE average_execution_time gauge
average_execution_time 120.5

# HELP llm_token_usage LLM token usage
# TYPE llm_token_usage counter
llm_token_usage{model="claude-3-5-sonnet",direction="input"} 1000
llm_token_usage{model="claude-3-5-sonnet",direction="output"} 500

# HELP call_duration_seconds Call duration in seconds
# TYPE call_duration_seconds gauge
call_duration_seconds{task_id="uuid"} 300.5
```

## Error Codes

| Code | Description |
|------|-------------|
| `INVALID_TOKEN` | Invalid or expired JWT token |
| `TASK_NOT_FOUND` | Task not found |
| `INSUFFICIENT_PERMISSIONS` | User lacks required permissions |
| `TOOL_VALIDATION_FAILED` | Tool validation failed |
| `RISK_HIGH` | Action exceeds risk threshold |
| `CONFIRMATION_REQUIRED` | Action requires user confirmation |
| `DATABASE_ERROR` | Database operation failed |
| `REDIS_ERROR` | Redis operation failed |
| `LLM_ERROR` | LLM API call failed |
| `EXTERNAL_SERVICE_ERROR` | External service call failed |

## Rate Limiting

- **API endpoints**: 10 requests per second per IP
- **Voice endpoints**: 5 calls per minute per user
- **Email endpoints**: 30 emails per minute per user

Rate limit headers:
```
X-RateLimit-Limit: 10
X-RateLimit-Remaining: 9
X-RateLimit-Reset: 1704067200
```

## Webhooks

### Webhook Configuration

Configure webhook endpoints for events.

**Endpoint:** `POST /api/webhooks`

**Request Body:**
```json
{
  "event_type": "task_completed",
  "url": "https://your-webhook-endpoint.com",
  "secret": "webhook-secret"
}
```

### Webhook Events

| Event | Description |
|-------|-------------|
| `task_created` | Task created |
| `task_started` | Task execution started |
| `task_completed` | Task completed successfully |
| `task_failed` | Task failed |
| `task_replanned` | Task replanned |
| `call_started` | Call started |
| `call_completed` | Call completed |
| `email_sent` | Email sent |
| `email_delivered` | Email delivered |

## Testing

### Test API

Use the interactive API documentation:

```bash
# Start development server
docker-compose up app

# Open browser
open http://localhost:8000/docs
```

### Test with cURL

```bash
# Create task
curl -X POST http://localhost:8000/api/tasks \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "goal": "Cancel my Comcast account",
    "user_id": "uuid"
  }'

# Get task status
curl http://localhost:8000/api/tasks/{task_id} \
  -H "Authorization: Bearer <token>"
```

### Test with Python

```python
import httpx

async def test_api():
    async with httpx.AsyncClient() as client:
        # Create task
        response = await client.post(
            "http://localhost:8000/api/tasks",
            headers={"Authorization": "Bearer <token>"},
            json={"goal": "Cancel my Comcast account", "user_id": "uuid"}
        )
        print(response.json())

        # Get task status
        task_id = response.json()["data"]["task_id"]
        response = await client.get(
            f"http://localhost:8000/api/tasks/{task_id}",
            headers={"Authorization": "Bearer <token>"}
        )
        print(response.json())

import asyncio
asyncio.run(test_api())
```
