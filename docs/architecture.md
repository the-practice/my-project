# Autonomous AI Operator - System Architecture

## Overview

A production-ready, multi-channel AI operator that autonomously executes real-world tasks through voice, email, and web research. Built with Python/FastAPI, Anthropic Claude, PostgreSQL, Redis, and AWS infrastructure.

## Technology Stack

### Core Framework
- **Backend**: FastAPI (async-first, type-safe)
- **LLM**: Anthropic Claude 3.5 Sonnet (reasoning, planning)
- **Database**: PostgreSQL 15+ with pgvector extension
- **Cache**: Redis 7+ (working memory)
- **Vector Store**: pgvector for semantic memory

### External Services
- **Voice**: Twilio Programmable Voice + Vapi.ai (real-time orchestration)
- **TTS**: ElevenLabs (realistic voice synthesis)
- **STT**: Deepgram (speech-to-text)
- **Email**: IMAP (inbox) + SMTP (outbox)
- **Web Search**: Serper API (primary) + Playwright (fallback)
- **Deployment**: AWS (ECS Fargate, RDS, ElastiCache, S3)

### Infrastructure
- **Containerization**: Docker + Docker Compose
- **Orchestration**: AWS ECS Fargate
- **CI/CD**: GitHub Actions
- **Monitoring**: AWS CloudWatch + Prometheus
- **Logging**: Structured JSON logs

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Interaction Layer                        │
├─────────────────────────────────────────────────────────────┤
│  Voice (Twilio/Vapi)    │    Email (IMAP/SMTP)              │
│  - Media streams        │    - Thread tracking              │
│  - Real-time orchest.   │    - Attachment parsing           │
│  - Barge-in support     │    - Intent classification        │
└────────────┬──────────────────────────────┬────────────────┘
             │                              │
             ▼                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    Cognitive Core                            │
├─────────────────────────────────────────────────────────────┤
│  Intent Interpreter  │  Task Planner  │  Tool Orchestrator  │
│  - Parse raw input   │  - Hierarchical│  - Validate tools   │
│  - Extract entities  │  - Generate    │  - Execute actions  │
│  - Confidence scores │  - Subtasks    │  - Return results   │
└────────────┬──────────────────────────────┬────────────────┘
             │                              │
             ▼                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    Memory Layer                              │
├─────────────────────────────────────────────────────────────┤
│  PostgreSQL (persistent) │  Redis (working) │  pgvector (semantic) │
│  - Users, vault, tasks   │  - Session data  │  - Vector embeddings │
│  - Task logs             │  - Tool results  │  - Semantic search  │
└────────────┬──────────────────────────────┬────────────────┘
             │                              │
             ▼                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    Execution Layer                           │
├─────────────────────────────────────────────────────────────┤
│  State Machine  │  Self-Monitoring Loop  │  Safety Governor  │
│  - Task states  │  - Replanning logic   │  - Risk checks    │
│  - Transitions  │  - Failure recovery   │  - Confirmation   │
└─────────────────────────────────────────────────────────────┘
```

## Project Structure

```
autonomous-ai-operator/
├── .github/
│   └── workflows/
│       ├── ci.yml
│       └── deploy.yml
├── app/
│   ├── __init__.py
│   ├── main.py                          # FastAPI application entry
│   ├── config.py                        # Configuration management
│   ├── dependencies.py                  # FastAPI dependencies
│   │
│   ├── core/                            # Core business logic
│   │   ├── __init__.py
│   │   ├── security.py                  # Encryption, auth
│   │   ├── state_machine.py             # Task state definitions
│   │   ├── logger.py                    # Structured logging
│   │   └── metrics.py                   # Cost tracking
│   │
│   ├── memory/                          # Memory architecture
│   │   ├── __init__.py
│   │   ├── base.py                      # Memory interface
│   │   ├── postgres.py                  # PostgreSQL storage
│   │   ├── redis.py                     # Redis working memory
│   │   └── vector.py                    # pgvector semantic memory
│   │
│   ├── cognitive/                       # Cognitive core
│   │   ├── __init__.py
│   │   ├── intent_interpreter.py        # Intent parsing
│   │   ├── task_planner.py              # Hierarchical planning
│   │   ├── tool_orchestrator.py         # Tool execution
│   │   └── self_monitor.py              # Monitoring & replanning
│   │
│   ├── tools/                           # Tool implementations
│   │   ├── __init__.py
│   │   ├── base.py                      # Tool interface
│   │   ├── web_search.py                # Serper API
│   │   ├── phone_call.py                # Twilio outbound
│   │   ├── email_send.py                # SMTP sender
│   │   ├── email_receive.py             # IMAP listener
│   │   ├── memory_ops.py                # Memory CRUD
│   │   └── tts.py                       # ElevenLabs TTS
│   │
│   ├── interactions/                    # Interaction layers
│   │   ├── __init__.py
│   │   ├── voice/                       # Voice handling
│   │   │   ├── __init__.py
│   │   │   ├── twilio_handler.py        # Twilio webhooks
│   │   │   ├── vapi_orchestrator.py     # Vapi integration
│   │   │   └── tts_service.py           # ElevenLabs TTS
│   │   └── email/                       # Email handling
│   │       ├── __init__.py
│   │       ├── imap_listener.py         # Background worker
│   │       ├── smtp_sender.py           # Email sender
│   │       └── parser.py                # Message parsing
│   │
│   ├── safety/                          # Safety & policy
│   │   ├── __init__.py
│   │   ├── governor.py                  # Policy enforcement
│   │   ├── risk_assessor.py             # Risk evaluation
│   │   └── confirmation.py              # User confirmation
│   │
│   ├── research/                        # Web research
│   │   ├── __init__.py
│   │   ├── serper_client.py             # Serper API client
│   │   ├── playwright_fallback.py       # Fallback scraper
│   │   └── validator.py                 # Result validation
│   │
│   └── models/                          # Pydantic models
│       ├── __init__.py
│       ├── user.py
│       ├── task.py
│       ├── intent.py
│       ├── plan.py
│       ├── tool.py
│       └── memory.py
│
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_cognitive/
│   ├── test_memory/
│   ├── test_tools/
│   ├── test_interactions/
│   └── test_safety/
│
├── scripts/
│   ├── init_db.py                       # Database initialization
│   ├── seed_data.py                     # Sample data
│   └── migrate.py                       # Alembic migrations
│
├── alembic/
│   ├── versions/
│   └── env.py
│
├── docker/
│   ├── Dockerfile
│   ├── docker-compose.yml
│   └── nginx.conf
│
├── docs/
│   ├── architecture.md                  # This file
│   ├── api.md                           # API documentation
│   ├── deployment.md                    # Deployment guide
│   └── examples.md                      # Usage examples
│
├── .env.example                         # Environment variables template
├── .gitignore
├── requirements.txt                     # Python dependencies
├── pyproject.toml                       # Project configuration
└── README.md
```

## Database Schema

### PostgreSQL Tables

```sql
-- Users table
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    phone VARCHAR(20) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Secure vault for sensitive data
CREATE TABLE vault (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    company VARCHAR(255) NOT NULL,
    account_number VARCHAR(100) NOT NULL,
    pin VARCHAR(50) NOT NULL,  -- AES-256 encrypted
    metadata_json JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Tasks table
CREATE TABLE tasks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    goal TEXT NOT NULL,
    state VARCHAR(50) NOT NULL DEFAULT 'INIT',
    metadata_json JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Task logs table
CREATE TABLE task_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    task_id UUID REFERENCES tasks(id) ON DELETE CASCADE,
    event_type VARCHAR(100) NOT NULL,
    payload_json JSONB NOT NULL,
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Vector embeddings table
CREATE TABLE semantic_memory (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    content TEXT NOT NULL,
    embedding vector(1536),  -- OpenAI embedding dimension
    metadata_json JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create indexes
CREATE INDEX idx_tasks_user_id ON tasks(user_id);
CREATE INDEX idx_tasks_state ON tasks(state);
CREATE INDEX idx_task_logs_task_id ON task_logs(task_id);
CREATE INDEX idx_task_logs_timestamp ON task_logs(timestamp);
CREATE INDEX idx_semantic_memory_user_id ON semantic_memory(user_id);
CREATE INDEX idx_semantic_memory_embedding ON semantic_memory USING ivfflat (embedding vector_cosine_ops) WITH (lists = 100);
```

### Redis Data Structures

```
# Working memory keys
task:{task_id}:state          -> String (current state)
task:{task_id}:plan           -> JSON (current plan)
task:{task_id}:context        -> JSON (execution context)
task:{task_id}:transcript     -> JSON (call/email transcript)
user:{user_id}:session        -> JSON (user session data)
user:{user_id}:preferences    -> JSON (user preferences)

# Tool results cache
tool:{tool_name}:result:{id}  -> JSON (cached results)
tool:{tool_name}:last_used    -> Timestamp

# Rate limiting
rate_limit:{user_id}:{tool}   -> Counter
rate_limit:{user_id}:global   -> Counter
```

## Environment Variables

```bash
# Application
APP_NAME=autonomous-ai-operator
APP_ENV=production
DEBUG=false
LOG_LEVEL=INFO

# Database
DATABASE_URL=postgresql+asyncpg://user:password@host:5432/dbname
REDIS_URL=redis://host:6379/0
VECTOR_DIMENSION=1536

# Anthropic Claude
ANTHROPIC_API_KEY=sk-ant-xxx
CLAUDE_MODEL=claude-3-5-sonnet-20241022
CLAUDE_MAX_TOKENS=4096
CLAUDE_TEMPERATURE=0.3

# Twilio
TWILIO_ACCOUNT_SID=ACxxx
TWILIO_AUTH_TOKEN=xxx
TWILIO_PHONE_NUMBER=+1xxx
TWILIO_WEBHOOK_URL=https://api.example.com/voice/webhook

# Vapi.ai
VAPI_API_KEY=xxx
VAPI_PROJECT_ID=xxx
VAPI_BASE_URL=https://api.vapi.ai

# ElevenLabs
ELEVENLABS_API_KEY=xxx
ELEVENLABS_VOICE_ID=xxx
ELEVENLABS_VOICE_SETTINGS={"stability":0.5,"similarity_boost":0.75}

# Deepgram (STT)
DEEPGRAM_API_KEY=xxx
DEEPGRAM_MODEL=nova-2

# Serper (Web Search)
SERPER_API_KEY=xxx
SERPER_SEARCH_URL=https://google.serper.dev/search

# Email
IMAP_HOST=imap.gmail.com
IMAP_PORT=993
IMAP_USERNAME=user@gmail.com
IMAP_PASSWORD=xxx
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=user@gmail.com
SMTP_PASSWORD=xxx

# Security
ENCRYPTION_KEY=your-32-byte-encryption-key-here
JWT_SECRET=your-jwt-secret-here
JWT_ALGORITHM=HS256
JWT_EXPIRATION_HOURS=24

# AWS (Deployment)
AWS_REGION=us-east-1
AWS_ECS_CLUSTER=autonomous-ai-operator
AWS_ECS_SERVICE=autonomous-ai-operator-service
AWS_ECR_REPOSITORY=autonomous-ai-operator

# Monitoring
SENTRY_DSN=https://xxx@sentry.io/xxx
PROMETHEUS_PORT=9090

# Cost Tracking
COST_TRACKING_ENABLED=true
COST_ALERT_THRESHOLD=10.00
```

## API Endpoints

### Voice Endpoints

```
POST /api/voice/webhook/twilio
  - Twilio webhook for incoming/outgoing calls
  - Accepts: Call status, media stream events
  - Returns: TwiML or 200 OK

POST /api/voice/vapi/stream
  - Vapi.ai real-time stream endpoint
  - Accepts: Audio chunks, conversation state
  - Returns: Audio chunks, tool invocation signals

GET /api/voice/status/{task_id}
  - Get current call status
  - Returns: State, transcript, next action
```

### Email Endpoints

```
POST /api/email/webhook
  - Webhook for email events (sent, delivered, opened)
  - Accepts: Email event data
  - Returns: 200 OK

GET /api/email/inbox
  - Poll IMAP inbox (background worker)
  - Returns: Unread messages
```

### Task Endpoints

```
POST /api/tasks
  - Create new task
  - Body: { goal: string, user_id: string }
  - Returns: Task object

GET /api/tasks/{task_id}
  - Get task details
  - Returns: Task object with state, logs, plan

GET /api/tasks/{task_id}/logs
  - Get task execution logs
  - Returns: Array of log entries

POST /api/tasks/{task_id}/execute
  - Trigger task execution
  - Returns: Execution status

POST /api/tasks/{task_id}/replan
  - Force replanning
  - Returns: New plan
```

### Memory Endpoints

```
GET /api/memory/{user_id}/semantic?query=string
  - Semantic search
  - Returns: Relevant memories

POST /api/memory/{user_id}
  - Store new memory
  - Body: { content: string, metadata: object }

GET /api/memory/{user_id}/vault
  - Get user's secure vault
  - Returns: Encrypted vault data
```

### Health & Monitoring

```
GET /health
  - Health check endpoint
  - Returns: Service status

GET /metrics
  - Prometheus metrics
  - Returns: Metrics in Prometheus format
```

## Task State Machine

```mermaid
stateDiagram-v2
    [*] --> INIT: New task created
    INIT --> GATHER_INFO: Intent confirmed
    GATHER_INFO --> RESEARCH: Data retrieved
    RESEARCH --> READY_TO_EXECUTE: Research complete
    READY_TO_EXECUTE --> CALL_IN_PROGRESS: Call placed
    CALL_IN_PROGRESS --> AWAITING_USER_INPUT: User responds
    CALL_IN_PROGRESS --> SUMMARIZE: Call completed
    AWAITING_USER_INPUT --> CALL_IN_PROGRESS: Continue conversation
    AWAITING_USER_INPUT --> SUMMARIZE: User confirms
    SUMMARIZE --> COMPLETED: Summary generated
    SUMMARIZE --> FAILED: Critical failure
    CALL_IN_PROGRESS --> RESEARCH: Need more info
    CALL_IN_PROGRESS --> GATHER_INFO: Missing credentials
    RESEARCH --> FAILED: Research failed
    READY_TO_EXECUTE --> FAILED: Tool validation failed
    [*] --> FAILED: Critical error
```

### State Definitions

**INIT**
- Entry: Task created, goal parsed
- Exit: Intent confirmed, gather required data
- Transitions: GATHER_INFO, FAILED

**GATHER_INFO**
- Entry: Check memory for existing data
- Exit: All required data collected
- Transitions: RESEARCH, FAILED
- Recovery: Ask user for missing data

**RESEARCH**
- Entry: Search for official contact info
- Exit: Found valid contact method
- Transitions: READY_TO_EXECUTE, FAILED
- Recovery: Try alternative search, escalate

**READY_TO_EXECUTE**
- Entry: Plan generated, tools validated
- Exit: First tool executed
- Transitions: CALL_IN_PROGRESS, FAILED
- Recovery: Re-validate tools, replan

**CALL_IN_PROGRESS**
- Entry: Call connected, conversation started
- Exit: Call ended, transcript saved
- Transitions: AWAITING_USER_INPUT, SUMMARIZE, RESEARCH, GATHER_INFO
- Recovery: Handle interruptions, drop recovery

**AWAITING_USER_INPUT**
- Entry: Waiting for user response
- Exit: User provided input
- Transitions: CALL_IN_PROGRESS, SUMMARIZE
- Recovery: Timeout handling, re-prompt

**SUMMARIZE**
- Entry: Task completed, generate summary
- Exit: Summary saved, email sent
- Transitions: COMPLETED, FAILED
- Recovery: Partial summary, log error

**COMPLETED**
- Entry: Task successfully finished
- Exit: Mark as complete, notify user
- Transitions: [*]

**FAILED**
- Entry: Critical error or unrecoverable failure
- Exit: Log error, notify user
- Transitions: [*]

**ESCALATED**
- Entry: Task requires human intervention
- Exit: Escalated to human operator
- Transitions: [*]
```

## Component Interactions

### Voice Flow

```
1. Twilio initiates call
   ↓
2. Media stream → Vapi.ai
   ↓
3. Vapi streams audio to Claude
   ↓
4. Claude generates response
   ↓
5. ElevenLabs synthesizes voice
   ↓
6. Audio stream back to Vapi
   ↓
7. Vapi → Twilio → User
   ↓
8. If tool needed:
   - Claude signals tool call
   - Backend executes tool
   - Claude incorporates result
   - Continue conversation
```

### Email Flow

```
1. IMAP listener polls inbox
   ↓
2. Parse unread messages
   ↓
3. Intent Interpreter classifies
   ↓
4. Create/update task
   ↓
5. Task Planner generates plan
   ↓
6. Execute planning loop
   ↓
7. Send response email
   ↓
8. Store thread in memory
```

### Task Execution Loop

```
while task.state not in [COMPLETED, FAILED]:
    1. Load task from PostgreSQL
    2. Load working memory from Redis
    3. Call Task Planner for next action
    4. Validate action with Safety Governor
    5. Execute tool via Tool Orchestrator
    6. Store result in Redis
    7. Log event to PostgreSQL
    8. Update task state
    9. Check for failures
    10. If failed, trigger replanning
```

## Security Considerations

### Data Protection
- **Vault**: AES-256 encryption for sensitive data
- **API Keys**: Environment variables, never hardcoded
- **HTTPS**: All endpoints require TLS
- **JWT**: Token-based authentication for API access

### Access Control
- User isolation: Tasks scoped to user_id
- Role-based access: Admin vs. user permissions
- Rate limiting: Prevent abuse
- Audit logging: All actions logged

### Safety Measures
- **Confirmation Required**: High-risk actions need explicit user confirmation
- **Risk Assessment**: Evaluate action risk before execution
- **Tool Validation**: All tool calls validated before execution
- **Fallback Logic**: Graceful degradation on failures

## Deployment Architecture

### AWS Infrastructure

```
┌─────────────────────────────────────────────────────────┐
│                    AWS Cloud                            │
├─────────────────────────────────────────────────────────┤
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │   API Gateway│  │   ALB        │  │   CloudFront │  │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘  │
│         │                 │                 │          │
│  ┌──────▼─────────────────▼─────────────────▼──────┐   │
│  │              ECS Fargate Cluster                 │   │
│  │  ┌──────────────────────────────────────────┐   │   │
│  │  │  Task Definition (FastAPI + Workers)     │   │   │
│  │  │  - API Server (port 8000)                │   │   │
│  │  │  - IMAP Worker (port 8001)               │   │   │
│  │  │  - Vapi Stream Handler (port 8002)       │   │   │
│  │  └──────────────────────────────────────────┘   │   │
│  └──────┬──────────────────────────────────────────┘   │
│         │                                              │
│  ┌──────▼──────────────────────────────────────────┐   │
│  │              RDS PostgreSQL                      │   │
│  │  - Multi-AZ deployment                          │   │
│  │  - Read replicas for scaling                    │   │
│  └──────┬──────────────────────────────────────────┘   │
│         │                                              │
│  ┌──────▼──────────────────────────────────────────┐   │
│  │              ElastiCache Redis                   │   │
│  │  - Cluster mode for high availability           │   │
│  └──────┬──────────────────────────────────────────┘   │
│         │                                              │
│  ┌──────▼──────────────────────────────────────────┐   │
│  │              S3 (Static assets, logs)            │   │
│  └──────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘
```

### Containerization

**Dockerfile**:
- Multi-stage build
- Python 3.11 base image
- Production-ready optimizations
- Health check endpoint

**docker-compose.yml**:
- Local development environment
- PostgreSQL, Redis, and app services
- Volume mounts for development
- Network isolation

### CI/CD Pipeline

1. **Code Push** → GitHub Actions
2. **Lint & Test** → Run pytest, mypy, ruff
3. **Build Image** → Docker build
4. **Push to ECR** → AWS ECR
5. **Deploy to ECS** → Blue-green deployment
6. **Health Check** → Verify service health
7. **Notify** → Slack/Email on success/failure

## Cost Estimation (Monthly)

### AWS Services
- **ECS Fargate**: $50-200 (depending on usage)
- **RDS PostgreSQL**: $50-150 (t3.medium)
- **ElastiCache Redis**: $30-100 (cache.t3.medium)
- **S3**: $5-20 (storage + requests)
- **API Gateway**: $10-50 (requests)
- **CloudWatch**: $10-30 (logs + metrics)

### External Services
- **Anthropic Claude**: $0.003/1K tokens (estimated $50-200)
- **Twilio**: $0.005/min (estimated $20-100)
- **ElevenLabs**: $0.005/1K characters (estimated $10-50)
- **Serper API**: $0.50/100 searches (estimated $5-20)
- **Deepgram**: $0.004/minute (estimated $5-20)

**Total Estimated**: $200-800/month depending on usage

## Monitoring & Observability

### Metrics to Track
- **Task Success Rate**: Percentage of completed tasks
- **Average Execution Time**: Time from task creation to completion
- **Tool Success Rate**: Percentage of successful tool calls
- **LLM Token Usage**: Cost and efficiency
- **Call Duration**: Average call length
- **Error Rate**: Percentage of failed tasks
- **Memory Usage**: Redis and PostgreSQL memory

### Logging Strategy
- **Structured JSON logs** with correlation IDs
- **Log levels**: DEBUG, INFO, WARNING, ERROR, CRITICAL
- **Log retention**: 30 days for production
- **Centralized logging**: AWS CloudWatch Logs

### Alerts
- **High error rate**: >5% error rate
- **High cost**: >$50/day
- **Service downtime**: >1 minute
- **Database connection issues**
- **Memory pressure**: >80% usage

## Performance Considerations

### Scalability
- **Horizontal scaling**: Add more ECS tasks
- **Database sharding**: For large user bases
- **Redis clustering**: For high throughput
- **CDN**: For static assets

### Optimization
- **Connection pooling**: PostgreSQL and Redis
- **Async I/O**: All I/O operations
- **Caching**: Tool results, user preferences
- **Batch operations**: Database queries

### Reliability
- **Health checks**: All services
- **Graceful degradation**: Fallback mechanisms
- **Retry logic**: Exponential backoff
- **Circuit breakers**: For external services

## Development Workflow

1. **Feature Branch**: Create branch from main
2. **Local Development**: Use docker-compose
3. **Testing**: Run pytest with coverage
4. **Code Review**: Pull request with review
5. **CI/CD**: Automated testing and deployment
6. **Monitoring**: Check CloudWatch after deployment

## Next Steps

1. Create project structure
2. Set up FastAPI application
3. Implement database schema
4. Build core components
5. Integrate external services
6. Write tests
7. Deploy to AWS
8. Monitor and iterate
