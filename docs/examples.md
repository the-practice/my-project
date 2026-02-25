# End-to-End Flow Examples

Complete examples of how the Autonomous AI Operator handles different scenarios.

## Example 1: Cancel Comcast Account via Email

### Scenario
User sends an email requesting to cancel their Comcast account.

### Flow

```
1. Email Received
   └─> IMAP Listener polls inbox
       └─> Finds unread email: "Cancel my Comcast account"
           └─> Parser extracts intent
               └─> Intent Interpreter: "cancel_service", company="Comcast", confidence=0.94

2. Task Creation
   └─> Create task in PostgreSQL
       └─> State: INIT
           └─> Log: task_created

3. Memory Check
   └─> Check Redis for existing credentials
       └─> Not found
           └─> State: GATHER_INFO

4. Data Gathering
   └─> Ask user for missing data
       └─> Send email: "Please provide your Comcast account number"
           └─> User replies with account number
               └─> Store in vault (AES-256 encrypted)
                   └─> State: RESEARCH

5. Web Research
   └─> Tool: web_search("Comcast customer service cancellation")
       └─> Serper API returns official number: +18005551234
           └─> Validate against trusted domain
               └─> State: READY_TO_EXECUTE

6. Task Planning
   └─> Task Planner generates plan:
       1. Retrieve credentials
       2. Research official number
       3. Place outbound call
       4. Authenticate user
       5. Request cancellation
       6. Confirm reference number
       7. Send summary email
       8. Store transcript

7. Tool Execution
   └─> Tool: place_call(phone_number="+18005551234")
       └─> Twilio initiates call
           └─> State: CALL_IN_PROGRESS

8. Voice Conversation
   └─> Vapi streams audio to Claude
       └─> Claude generates response
           └─> ElevenLabs synthesizes voice
               └─> User responds: "Yes, cancel my account"
                   └─> Claude processes response
                       └─> Tool: retrieve_credentials
                           └─> User provides account number
                               └─> Tool: authenticate_user
                                   └─> User provides PIN
                                       └─> Tool: request_cancellation
                                           └─> Representative confirms
                                               └─> Tool: get_reference_number
                                                   └─> Representative provides reference: REF-123456
                                                       └─> State: SUMMARIZE

9. Summary Generation
   └─> Generate summary email
       └─> Subject: "[AI Operator] Task Summary - Comcast Cancellation"
           └─> Body: "Your Comcast account has been successfully cancelled. Reference number: REF-123456"
               └─> Tool: send_email(to=user@example.com, subject=..., body=...)
                   └─> State: COMPLETED

10. Memory Storage
    └─> Store summary in semantic memory
        └─> Store reference number in vault
            └─> Log: task_completed
```

### API Calls

```bash
# 1. Create task
POST /api/tasks
{
  "goal": "Cancel my Comcast account",
  "user_id": "uuid",
  "metadata": {"company": "Comcast"}
}

# 2. Execute task
POST /api/tasks/{task_id}/execute

# 3. Get task status
GET /api/tasks/{task_id}

# 4. Get logs
GET /api/tasks/{task_id}/logs

# 5. Store memory
POST /api/memory/{user_id}
{
  "content": "Comcast account cancelled. Reference: REF-123456",
  "metadata": {"type": "task_summary", "company": "Comcast"}
}
```

## Example 2: Contact AT&T Support via Voice

### Scenario
User calls the system and requests to contact AT&T support.

### Flow

```
1. Call Initiated
   └─> Twilio receives call
       └─> Media stream connects to Vapi
           └─> Vapi streams audio to Claude
               └─> Claude transcribes: "I need to contact AT&T support"

2. Intent Recognition
   └─> Intent Interpreter: "contact_support", company="AT&T", confidence=0.91
       └─> State: INIT

3. Memory Check
   └─> Check Redis for AT&T credentials
       └─> Found: account_number="9876543210", pin="encrypted"
           └─> State: READY_TO_EXECUTE

4. Task Planning
   └─> Task Planner generates plan:
       1. Retrieve AT&T credentials
       2. Research official support number
       3. Place outbound call
       4. Authenticate user
       5. Describe issue
       6. Get support ticket number
       7. Send summary email

5. Tool Execution
   └─> Tool: web_search("AT&T customer support phone number")
       └─> Serper API returns: +18005551234
           └─> State: READY_TO_EXECUTE

6. Outbound Call
   └─> Tool: place_call(phone_number="+18005551234")
       └─> Twilio calls AT&T support
           └─> State: CALL_IN_PROGRESS

7. Conversation
   └─> Claude speaks: "Hello, I'd like to speak with AT&T support regarding my account."
       └─> Vapi streams audio to Twilio
           └─> AT&T representative answers
               └─> Claude: "My account number is 9876543210. I'm having billing issues."
                   └─> Representative: "Let me pull up your account..."
                       └─> Claude: "Thank you. What's your support ticket number?"
                           └─> Representative: "Your ticket is #AT-789456"
                               └─> State: SUMMARIZE

8. Summary & Email
   └─> Generate summary
       └─> Send email to user
           └─> State: COMPLETED

9. Memory Storage
   └─> Store ticket number in semantic memory
       └─> Log: task_completed
```

### Voice Flow

```
User: "I need to contact AT&T support"
  ↓
Claude: "I can help you contact AT&T support. What's your account number?"
  ↓
User: "9876543210"
  ↓
Claude: "Thank you. I'm placing a call to AT&T support now."
  ↓
[Call connected to AT&T]
  ↓
Claude: "Hello, I'd like to speak with AT&T support regarding my account."
  ↓
[AT&T representative answers]
  ↓
Claude: "My account number is 9876543210. I'm having billing issues."
  ↓
[Representative processes account]
  ↓
Claude: "Thank you. What's your support ticket number?"
  ↓
Representative: "Your ticket is #AT-789456"
  ↓
Claude: "Thank you. I'll send you a summary email with this information."
  ↓
[Call ends]
  ↓
Claude: "I've contacted AT&T support and received ticket #AT-789456. A summary email has been sent to you."
```

## Example 3: Research and Book Appointment

### Scenario
User wants to book a dentist appointment.

### Flow

```
1. Email Received
   └─> Email: "I need to book a dentist appointment"
       └─> Intent: "book_appointment", confidence=0.88

2. Task Creation
   └─> State: INIT

3. Memory Check
   └─> Check for dentist information
       └─> Not found
           └─> State: GATHER_INFO

4. Data Gathering
   └─> Ask user for dentist name
       └─> User: "Dr. Smith Dental"
           └─> Ask for preferred date
               └─> User: "Next Tuesday"
                   └─> Ask for time
                       └─> User: "10 AM"
                           └─> State: RESEARCH

5. Web Research
   └─> Tool: web_search("Dr. Smith Dental appointment booking")
       └─> Serper API returns booking URL: https://drsmithdental.com/book
           └─> Validate domain
               └─> State: READY_TO_EXECUTE

6. Task Planning
   └─> Plan:
       1. Research dentist booking system
       2. Navigate to booking page
       3. Select date and time
       4. Enter patient information
       5. Confirm appointment
       6. Send confirmation email

7. Tool Execution
   └─> Tool: web_search("Dr. Smith Dental appointment booking")
       └─> State: READY_TO_EXECUTE

8. Browser Automation
   └─> Tool: navigate_to(url="https://drsmithdental.com/book")
       └─> Select date: "2024-01-16"
           └─> Select time: "10:00"
               └─> Enter patient info
                   └─> Confirm appointment
                       └─> State: SUMMARIZE

9. Summary
   └─> Generate confirmation email
       └─> Send to user
           └─> State: COMPLETED

10. Memory Storage
    └─> Store appointment details
        └─> Log: task_completed
```

## Example 4: Handle Failed Task

### Scenario
Task fails due to representative not understanding.

### Flow

```
1. Task Execution
   └─> State: CALL_IN_PROGRESS
       └─> Attempting to cancel Comcast account
           └─> Representative: "I don't see that account in our system"
               └─> Claude: "Let me check the account number again. Is it 1234567890?"
                   └─> Representative: "No, that's not our account"
                       └─> State: RESEARCH

2. Failure Detection
   └─> Self-Monitoring Loop detects:
       └─> Tool: place_call failed
           └─> Error: "Account not found"
               └─> State: RESEARCH

3. Replanning
   └─> Task Planner generates new plan:
       1. Research alternative contact methods
       2. Try online cancellation portal
       3. Send email request
       4. Escalate to human if needed

4. Alternative Research
   └─> Tool: web_search("Comcast online account cancellation")
       └─> Serper API returns: https://www.comcast.com/support/cancel
           └─> Validate domain
               └─> State: READY_TO_EXECUTE

5. Tool Execution
   └─> Tool: navigate_to(url="https://www.comcast.com/support/cancel")
       └─> Fill cancellation form
           └─> Submit
               └─> State: SUMMARIZE

6. Summary
   └─> Generate summary
       └─> Send email to user
           └─> State: COMPLETED

7. Memory Storage
    └─> Store alternative method
        └─> Log: task_completed
```

## Example 5: Escalation to Human

### Scenario
Task requires human intervention (e.g., complex IVR system).

### Flow

```
1. Task Execution
   └─> State: CALL_IN_PROGRESS
       └─> Attempting to cancel account
           └─> IVR system: "Press 1 for billing, 2 for support..."
               └─> Claude: "I'm pressing 1 for billing"
                   └─> IVR: "Please enter your account number"
                       └─> Claude: "1234567890"
                           └─> IVR: "Account not found. Please try again."
                               └─> Claude: "Let me try again. 1234567890"
                                   └─> IVR: "Account not found."
                                       └─> State: RESEARCH

2. Failure Detection
   └─> Self-Monitoring Loop detects:
       └─> Tool: place_call failed
           └─> Error: "IVR system not responding"
               └─> State: RESEARCH

3. Replanning
   └─> Task Planner generates new plan:
       1. Research alternative contact methods
       2. Try online cancellation portal
       3. Send email request
       4. Escalate to human

4. Human Escalation
   └─> State: ESCALATED
       └─> Log: task_escalated
           └─> Send notification to human operator
               └─> Include task details
                   └─> Include transcript
                       └─> Include attempted solutions
```

## State Transitions

### Normal Flow
```
INIT → GATHER_INFO → RESEARCH → READY_TO_EXECUTE → CALL_IN_PROGRESS → SUMMARIZE → COMPLETED
```

### Failure Recovery
```
CALL_IN_PROGRESS → RESEARCH → GATHER_INFO → READY_TO_EXECUTE → CALL_IN_PROGRESS
```

### Escalation
```
READY_TO_EXECUTE → ESCALATED
```

### Critical Failure
```
ANY STATE → FAILED
```

## Cost Tracking

Each task tracks costs:

```json
{
  "task_id": "uuid",
  "costs": {
    "llm_input_tokens": 1000,
    "llm_output_tokens": 500,
    "llm_cost": "$0.015,
    "twilio_call_duration": 300,
    "twilio_cost": "$1.50,
    "serper_searches": 2,
    "serper_cost": "$0.01,
    "elevenlabs_chars": 500,
    "elevenlabs_cost": "$0.0025,
    "total_cost": "$1.5175
  }
}
```

## Monitoring

### Metrics Tracked

- **Task Success Rate**: 95% (19/20 tasks completed)
- **Average Execution Time**: 5 minutes
- **Tool Success Rate**: 92%
- **LLM Token Usage**: 1500 tokens per task
- **Call Duration**: 3-5 minutes
- **Error Rate**: 5%

### Alerts

- **High Error Rate**: >5% error rate triggers alert
- **High Cost**: >$10/day triggers alert
- **Service Downtime**: >1 minute triggers alert
- **Memory Pressure**: >80% usage triggers alert

## Best Practices

1. **Always store credentials securely** in the vault
2. **Validate all external data** before using it
3. **Log all actions** for audit trail
4. **Implement retry logic** for transient failures
5. **Always provide user confirmation** for high-risk actions
6. **Generate summaries** for all completed tasks
7. **Store results in memory** for future reference
8. **Monitor costs** and optimize regularly
