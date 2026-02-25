-- Autonomous AI Operator - Database Schema
-- PostgreSQL 15+ with pgvector extension

-- Enable required extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgvector";

-- Users table
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(255) NOT NULL,
    phone VARCHAR(20) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Secure vault for sensitive data (AES-256 encrypted)
CREATE TABLE vault (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    company VARCHAR(255) NOT NULL,
    account_number VARCHAR(100) NOT NULL,
    pin VARCHAR(50) NOT NULL,  -- AES-256 encrypted
    metadata_json JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(user_id, company)
);

-- Tasks table
CREATE TABLE tasks (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    goal TEXT NOT NULL,
    state VARCHAR(50) NOT NULL DEFAULT 'INIT',
    metadata_json JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Task logs table
CREATE TABLE task_logs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    task_id UUID NOT NULL REFERENCES tasks(id) ON DELETE CASCADE,
    event_type VARCHAR(100) NOT NULL,
    payload_json JSONB NOT NULL,
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Vector embeddings table for semantic memory
CREATE TABLE semantic_memory (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    content TEXT NOT NULL,
    embedding vector(1536),  -- OpenAI embedding dimension
    metadata_json JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create indexes for performance
CREATE INDEX idx_tasks_user_id ON tasks(user_id);
CREATE INDEX idx_tasks_state ON tasks(state);
CREATE INDEX idx_tasks_created_at ON tasks(created_at DESC);
CREATE INDEX idx_task_logs_task_id ON task_logs(task_id);
CREATE INDEX idx_task_logs_timestamp ON task_logs(timestamp DESC);
CREATE INDEX idx_task_logs_event_type ON task_logs(event_type);
CREATE INDEX idx_semantic_memory_user_id ON semantic_memory(user_id);
CREATE INDEX idx_semantic_memory_embedding ON semantic_memory USING ivfflat (embedding vector_cosine_ops) WITH (lists = 100);
CREATE INDEX idx_semantic_memory_created_at ON semantic_memory(created_at DESC);

-- Create triggers for updated_at timestamps
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_vault_updated_at BEFORE UPDATE ON vault
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_tasks_updated_at BEFORE UPDATE ON tasks
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Create views for common queries
CREATE VIEW v_active_tasks AS
SELECT 
    t.id,
    t.user_id,
    t.goal,
    t.state,
    t.metadata_json,
    t.created_at,
    t.updated_at,
    u.name AS user_name,
    u.email AS user_email,
    u.phone AS user_phone
FROM tasks t
JOIN users u ON t.user_id = u.id
WHERE t.state IN ('INIT', 'GATHER_INFO', 'RESEARCH', 'READY_TO_EXECUTE', 'CALL_IN_PROGRESS', 'AWAITING_USER_INPUT');

CREATE VIEW v_task_history AS
SELECT 
    tl.id,
    tl.task_id,
    tl.event_type,
    tl.payload_json,
    tl.timestamp,
    t.goal,
    u.name AS user_name
FROM task_logs tl
JOIN tasks t ON tl.task_id = t.id
JOIN users u ON t.user_id = u.id
ORDER BY tl.timestamp DESC;

-- Create materialized view for semantic search optimization
CREATE MATERIALIZED VIEW semantic_search_index AS
SELECT 
    sm.id,
    sm.user_id,
    sm.content,
    sm.embedding,
    sm.metadata_json,
    sm.created_at
FROM semantic_memory sm;

CREATE UNIQUE INDEX idx_semantic_search_index_id ON semantic_search_index(id);
CREATE INDEX idx_semantic_search_index_user_id ON semantic_search_index(user_id);

-- Function to refresh materialized view
CREATE OR REPLACE FUNCTION refresh_semantic_search_index()
RETURNS void AS $$
BEGIN
    REFRESH MATERIALIZED VIEW CONCURRENTLY semantic_search_index;
END;
$$ language 'plpgsql';

-- Function to calculate similarity score
CREATE OR REPLACE FUNCTION calculate_similarity(a vector, b vector)
RETURNS float AS $$
BEGIN
    RETURN 1 - (a <=> b);  -- Cosine distance
END;
$$ language 'plpgsql';

-- Function to search semantic memory
CREATE OR REPLACE FUNCTION search_semantic_memory(
    p_user_id UUID,
    p_query TEXT,
    p_limit INTEGER DEFAULT 5
)
RETURNS TABLE (
    id UUID,
    content TEXT,
    similarity FLOAT,
    metadata JSONB,
    created_at TIMESTAMP WITH TIME ZONE
) AS $$
DECLARE
    v_embedding vector(1536);
BEGIN
    -- Generate embedding for query (would be done by application layer)
    -- For now, return empty result
    RETURN QUERY
    SELECT 
        sm.id,
        sm.content,
        calculate_similarity(sm.embedding, v_embedding) as similarity,
        sm.metadata_json as metadata,
        sm.created_at
    FROM semantic_memory sm
    WHERE sm.user_id = p_user_id
    ORDER BY sm.embedding <=> v_embedding
    LIMIT p_limit;
END;
$$ language 'plpgsql';

-- Grant permissions (adjust based on your security requirements)
-- GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO your_app_user;
-- GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO your_app_user;
-- GRANT EXECUTE ON ALL FUNCTIONS IN SCHEMA public TO your_app_user;

-- Insert sample data for testing (optional)
-- INSERT INTO users (name, phone, email) VALUES
--     ('John Doe', '+18005551234', 'john@example.com'),
--     ('Jane Smith', '+18005551235', 'jane@example.com');

-- INSERT INTO vault (user_id, company, account_number, pin, metadata_json) VALUES
--     (uuid_generate_v4(), 'Comcast', '1234567890', 'encrypted_pin', '{"type": "cable"}'),
--     (uuid_generate_v4(), 'AT&T', '9876543210', 'encrypted_pin', '{"type": "phone"}');

-- INSERT INTO tasks (user_id, goal, state, metadata_json) VALUES
--     (uuid_generate_v4(), 'Cancel my Comcast account', 'INIT', '{"company": "Comcast"}'),
--     (uuid_generate_v4(), 'Contact AT&T support', 'INIT', '{"company": "AT&T"}');
