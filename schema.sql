-- =============================================================
--  TASK MANAGEMENT SYSTEM — DATABASE SCHEMA
--  Database: PostgreSQL
--  Run this file in pgAdmin Query Tool or psql
-- =============================================================


-- -------------------------------------------------------------
--  1. CREATE DATABASE (run this separately if not yet created)
-- -------------------------------------------------------------
-- CREATE DATABASE task_manager;


-- -------------------------------------------------------------
--  2. USERS TABLE
-- -------------------------------------------------------------
CREATE TABLE IF NOT EXISTS users (
    id          SERIAL PRIMARY KEY,
    username    VARCHAR(80)  UNIQUE NOT NULL,
    email       VARCHAR(120) UNIQUE NOT NULL,
    password    VARCHAR(200) NOT NULL,           -- bcrypt hash
    created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


-- -------------------------------------------------------------
--  3. TASKS TABLE
-- -------------------------------------------------------------
CREATE TABLE IF NOT EXISTS tasks (
    id          SERIAL PRIMARY KEY,
    user_id     INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title       VARCHAR(120) NOT NULL,
    description TEXT,
    priority    VARCHAR(10)  DEFAULT 'medium'    CHECK (priority IN ('low', 'medium', 'high')),
    status      VARCHAR(20)  DEFAULT 'pending'   CHECK (status   IN ('pending', 'in_progress', 'completed')),
    created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


-- -------------------------------------------------------------
--  4. AUTO-UPDATE updated_at ON PATCH
-- -------------------------------------------------------------
CREATE OR REPLACE FUNCTION update_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE TRIGGER tasks_updated_at
BEFORE UPDATE ON tasks
FOR EACH ROW
EXECUTE FUNCTION update_updated_at();


-- -------------------------------------------------------------
--  5. INDEXES FOR PERFORMANCE
-- -------------------------------------------------------------
CREATE INDEX IF NOT EXISTS idx_tasks_user_id ON tasks(user_id);
CREATE INDEX IF NOT EXISTS idx_tasks_status   ON tasks(status);
CREATE INDEX IF NOT EXISTS idx_tasks_priority ON tasks(priority);


-- -------------------------------------------------------------
--  6. SAMPLE DATA (optional — for testing)
-- -------------------------------------------------------------
-- INSERT INTO users (username, email, password) VALUES
--     ('avadhi', 'a@a.com', '<bcrypt_hash_here>');

-- INSERT INTO tasks (user_id, title, description, priority, status) VALUES
--     (1, 'Setup Flask API',    'Initialize project structure', 'high',   'completed'),
--     (1, 'Build Auth Routes',  'Register and login endpoints', 'high',   'completed'),
--     (1, 'Add Task CRUD',      'POST PATCH DELETE GET',        'medium', 'in_progress'),
--     (1, 'Analytics Module',   'Pandas and NumPy summary',     'medium', 'pending'),
--     (1, 'Frontend UI',        'HTML CSS JS dashboard',        'low',    'pending');


-- -------------------------------------------------------------
--  SCHEMA SUMMARY
-- -------------------------------------------------------------
--
--  users
--  ├── id          (PK, auto-increment)
--  ├── username    (unique)
--  ├── email       (unique)
--  ├── password    (bcrypt hash)
--  └── created_at
--
--  tasks
--  ├── id          (PK, auto-increment)
--  ├── user_id     (FK → users.id, CASCADE DELETE)
--  ├── title
--  ├── description
--  ├── priority    (low / medium / high)
--  ├── status      (pending / in_progress / completed)
--  ├── created_at
--  └── updated_at  (auto-updated via trigger)
--
-- =============================================================
