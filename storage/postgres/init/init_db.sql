-- 启用 UUID 扩展（必须放在最前面）
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- 用户表
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    nickname VARCHAR(50),
    role VARCHAR(20) DEFAULT 'user',
    avatar_url VARCHAR(500),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_username ON users(username);

-- 检测记录表
CREATE TABLE IF NOT EXISTS detection_records (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    type VARCHAR(20) NOT NULL,
    status VARCHAR(20) DEFAULT 'pending',
    model_name VARCHAR(50) NOT NULL,
    model_version VARCHAR(20) DEFAULT '1.0.0',
    total_objects INTEGER DEFAULT 0,
    detection_time FLOAT,
    original_image_key VARCHAR(500),
    result_image_key VARCHAR(500),
    error_message TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_detection_records_user_id ON detection_records(user_id);
CREATE INDEX idx_detection_records_status ON detection_records(status);
CREATE INDEX idx_detection_records_created_at ON detection_records(created_at DESC);

-- 检测结果表
CREATE TABLE IF NOT EXISTS detection_results (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    record_id UUID NOT NULL REFERENCES detection_records(id) ON DELETE CASCADE,
    x1 FLOAT NOT NULL,
    y1 FLOAT NOT NULL,
    x2 FLOAT NOT NULL,
    y2 FLOAT NOT NULL,
    confidence FLOAT NOT NULL,
    class_id INTEGER NOT NULL,
    class_name VARCHAR(50) NOT NULL,
    chinese_name VARCHAR(50)
);

CREATE INDEX idx_detection_results_record_id ON detection_results(record_id);
CREATE INDEX idx_detection_results_class_id ON detection_results(class_id);

-- 目标类别表
CREATE TABLE IF NOT EXISTS target_categories (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE,
    chinese_name VARCHAR(50) NOT NULL UNIQUE,
    description TEXT,
    icon_url VARCHAR(500),
    color VARCHAR(20) DEFAULT '#10b981',
    enabled BOOLEAN DEFAULT TRUE,
    sort_order INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_target_categories_enabled ON target_categories(enabled);
CREATE INDEX idx_target_categories_sort_order ON target_categories(sort_order);

-- AI问答记录表
CREATE TABLE IF NOT EXISTS ai_qa_records (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    question TEXT NOT NULL,
    answer TEXT,
    model_name VARCHAR(50),
    status VARCHAR(20) DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_ai_qa_records_user_id ON ai_qa_records(user_id);
CREATE INDEX idx_ai_qa_records_created_at ON ai_qa_records(created_at DESC);

-- 模型版本表
CREATE TABLE IF NOT EXISTS model_versions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(50) NOT NULL,
    version VARCHAR(20) NOT NULL,
    description TEXT,
    model_key VARCHAR(500),
    status VARCHAR(20) DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(name, version)
);

CREATE INDEX idx_model_versions_status ON model_versions(status);

-- AI问答对话表 (用于多轮对话)
CREATE TABLE IF NOT EXISTS conversations (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(255) NOT NULL,
    title VARCHAR(255) DEFAULT '新对话',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_conversations_user_id ON conversations(user_id);

-- AI问答消息表
CREATE TABLE IF NOT EXISTS messages (
    id SERIAL PRIMARY KEY,
    conversation_id INTEGER REFERENCES conversations(id) ON DELETE CASCADE,
    role VARCHAR(50) NOT NULL,
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_messages_conversation_id ON messages(conversation_id);

-- 插入目标类别数据
INSERT INTO target_categories (name, chinese_name, description, color, sort_order) VALUES
('crazing', '裂纹', '表面裂纹缺陷', '#ef4444', 1),
('inclusion', '夹杂物', '材料内部夹杂物', '#f59e0b', 2),
('patches', '斑块', '表面斑块缺陷', '#10b981', 3),
('pitted_surface', '点蚀表面', '表面点蚀缺陷', '#3b82f6', 4),
('rolled-in_scale', '轧制氧化皮', '轧制氧化皮缺陷', '#8b5cf6', 5),
('scratches', '划痕', '表面划痕缺陷', '#06b6d4', 6);
