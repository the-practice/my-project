# Autonomous AI Operator

A production-ready, multi-channel AI operator that autonomously executes real-world tasks through voice, email, and web research. Built with Python/FastAPI, Anthropic Claude, PostgreSQL, Redis, and AWS infrastructure.

## Features

- **Multi-Channel Input**: Voice (Twilio/Vapi) and Email (IMAP/SMTP)
- **Autonomous Execution**: Plans and executes multi-step tasks
- **Real-Time Voice**: Natural conversation with realistic TTS
- **Persistent Memory**: Long-term storage with semantic search
- **Self-Monitoring**: Automatic replanning and failure recovery
- **Safety First**: Risk assessment and confirmation requirements
- **Production-Ready**: Comprehensive logging, monitoring, and error handling

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Interaction Layer                        │
├─────────────────────────────────────────────────────────────┤
│  Voice (Twilio/Vapi)    │    Email (IMAP/SMTP)              │
└────────────┬──────────────────────────────┬────────────────┘
             │                              │
             ▼                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    Cognitive Core                            │
├─────────────────────────────────────────────────────────────┤
│  Intent Interpreter  │  Task Planner  │  Tool Orchestrator  │
└────────────┬──────────────────────────────┬────────────────┘
             │                              │
             ▼                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    Memory Layer                              │
├─────────────────────────────────────────────────────────────┤
│  PostgreSQL (persistent) │  Redis (working) │  pgvector (semantic) │
└─────────────────────────────────────────────────────────────┘
```

## Quick Start

### Prerequisites

- Python 3.11+
- Docker & Docker Compose
- PostgreSQL 15+
- Redis 7+
- Anthropic API key
- Twilio account
- Vapi.ai account
- ElevenLabs API key

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/autonomous-ai-operator.git
   cd autonomous-ai-operator
   ```

2. **Copy environment variables**
   ```bash
   cp .env.example .env
   ```

3. **Configure your environment variables** in `.env`
   - Set your API keys (Anthropic, Twilio, Vapi, ElevenLabs, etc.)
   - Configure database connections
   - Set up security keys

4. **Start services with Docker Compose**
   ```bash
   docker-compose up -d
   ```

5. **Initialize the database**
   ```bash
   docker-compose exec postgres psql -U postgres -d autonomous_ai_operator -f /docker-entrypoint-initdb.d/schema.sql
   ```

6. **Run the application**
   ```bash
   docker-compose up app
   ```

## API Endpoints

### Voice
- `POST /api/voice/webhook/twilio` - Twilio webhook
- `POST /api/voice/vapi/stream` - Vapi real-time stream

### Email
- `POST /api/email/webhook` - Email event webhook
- `GET /api/email/inbox` - Poll IMAP inbox

### Tasks
- `POST /api/tasks` - Create new task
- `GET /api/tasks/{task_id}` - Get task details
- `GET /api/tasks/{task_id}/logs` - Get task logs
- `POST /api/tasks/{task_id}/execute` - Execute task
- `POST /api/tasks/{task_id}/replan` - Force replanning

### Memory
- `GET /api/memory/{user_id}/semantic?query=string` - Semantic search
- `POST /api/memory/{user_id}` - Store memory
- `GET /api/memory/{user_id}/vault` - Get secure vault

### Health
- `GET /health` - Health check
- `GET /metrics` - Prometheus metrics

## Usage Examples

### Create a Task via Email

Send an email to `your-email@gmail.com` with the subject:
```
Cancel my Comcast account
```

The system will:
1. Parse the email and extract intent
2. Check memory for existing credentials
3. Research official contact information
4. Place outbound call
5. Speak to representative
6. Confirm cancellation
7. Send summary email

### Create a Task via Voice

Call your Twilio number and say:
```
Cancel my AT&T account
```

The system will:
1. Convert speech to text
2. Parse intent and create task
3. Execute the cancellation process
4. Provide confirmation

## Project Structure

```
autonomous-ai-operator/
├── app/
│   ├── main.py                      # FastAPI application
│   ├── config.py                    # Configuration
│   ├── core/                        # Core business logic
│   ├── memory/                      # Memory architecture
│   ├── cognitive/                   # Cognitive core
│   ├── tools/                       # Tool implementations
│   ├── interactions/                # Voice & Email layers
│   ├── safety/                      # Safety & policy
│   └── research/                    # Web research
├── tests/                           # Test suite
├── database/
│   └── schema.sql                   # Database schema
├── docker/
│   ├── Dockerfile
│   ├── docker-compose.yml
│   └── nginx.conf
├── docs/
│   └── architecture.md              # Architecture documentation
└── .github/workflows/               # CI/CD pipelines
```

## Development

### Running Tests

```bash
pytest tests/ --cov=autonomous_ai_operator --cov-report=html
```

### Code Quality

```bash
# Lint
ruff check .

# Format
black .
isort .

# Type checking
mypy autonomous_ai_operator
```

### Local Development

```bash
# Start all services
docker-compose up -d

# Run app with hot reload
docker-compose up app

# Run email worker
docker-compose up email-worker

# Run Vapi worker
docker-compose up vapi-worker
```

## Configuration

### Environment Variables

See [`.env.example`](.env.example) for all available configuration options.

Key variables:
- `ANTHROPIC_API_KEY` - Anthropic Claude API key
- `DATABASE_URL` - PostgreSQL connection string
- `REDIS_URL` - Redis connection string
- `TWILIO_ACCOUNT_SID` - Twilio account SID
- `VAPI_API_KEY` - Vapi.ai API key
- `ELEVENLABS_API_KEY` - ElevenLabs API key

## Deployment

### AWS ECS

1. Build and push Docker image to ECR
2. Configure ECS task definition
3. Deploy with blue-green strategy

See [`.github/workflows/deploy.yml`](.github/workflows/deploy.yml) for CI/CD pipeline.

### Railway

1. Push to GitHub
2. Connect Railway repository
3. Configure environment variables
4. Deploy

### Render

1. Push to GitHub
2. Connect Render repository
3. Configure environment variables
4. Deploy

## Monitoring

### Metrics

- Task success rate
- Average execution time
- Tool success rate
- LLM token usage
- Call duration
- Error rate

### Logging

Structured JSON logs with correlation IDs:
```json
{
  "timestamp": "2024-01-01T00:00:00Z",
  "level": "INFO",
  "service": "autonomous-ai-operator",
  "task_id": "uuid",
  "event": "task_completed",
  "data": {}
}
```

## Security

- AES-256 encryption for sensitive data
- JWT-based authentication
- Rate limiting
- Input validation
- SQL injection prevention
- XSS protection

## Cost Estimation

Monthly costs (estimated):
- **AWS ECS**: $50-200
- **RDS PostgreSQL**: $50-150
- **ElastiCache Redis**: $30-100
- **Anthropic Claude**: $50-200
- **Twilio**: $20-100
- **ElevenLabs**: $10-50
- **Serper API**: $5-20

**Total**: $200-800/month depending on usage

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests and linting
5. Submit a pull request

## License

MIT License - see LICENSE file for details

## Support

- Documentation: [docs.autonomous-ai-operator.com](https://docs.autonomous-ai-operator.com)
- Issues: [GitHub Issues](https://github.com/yourusername/autonomous-ai-operator/issues)
- Email: support@autonomous-ai-operator.com

## Roadmap

- [ ] Multi-language support
- [ ] Advanced voice customization
- [ ] Custom tool development framework
- [ ] Analytics dashboard
- [ ] Mobile app
- [ ] Integration with more services
