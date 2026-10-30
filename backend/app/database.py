import sqlite3
import os
from contextlib import contextmanager

DATABASE_PATH = os.getenv("DATABASE_URL", "sqlite:///./evoxim.db").replace("sqlite:///", "")


def get_db_path() -> str:
    """Resolve the database file path."""
    if DATABASE_PATH.startswith("./"):
        base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        return os.path.join(base, DATABASE_PATH[2:])
    return DATABASE_PATH


def get_connection() -> sqlite3.Connection:
    """Create a new database connection with row factory."""
    conn = sqlite3.connect(get_db_path())
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    return conn


@contextmanager
def get_db():
    """Context manager for database connections."""
    conn = get_connection()
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


LEAD_STATUSES = [
    "NEW",
    "QUALIFIED",
    "PROPOSAL_DRAFT",
    "PROPOSAL_SENT",
    "MEETING_REQUESTED",
    "WON",
    "LOST",
]

SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS leads (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    company TEXT NOT NULL,
    email TEXT NOT NULL,
    phone TEXT,
    team_size INTEGER,
    language TEXT DEFAULT 'en',
    status TEXT DEFAULT 'NEW',
    recommended_service TEXT,
    objectives TEXT,
    context TEXT,
    discovery_answers TEXT,
    ai_summary TEXT,
    ai_brief TEXT,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS proposals (
    id TEXT PRIMARY KEY,
    lead_id TEXT NOT NULL,
    version INTEGER DEFAULT 1,
    content TEXT,
    status TEXT DEFAULT 'DRAFT',
    language TEXT DEFAULT 'en',
    created_at TEXT NOT NULL,
    approved_at TEXT,
    sent_at TEXT,
    FOREIGN KEY (lead_id) REFERENCES leads(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS feedback (
    id TEXT PRIMARY KEY,
    lead_id TEXT NOT NULL,
    original_recommendation TEXT,
    override_recommendation TEXT,
    reason TEXT,
    created_at TEXT NOT NULL,
    FOREIGN KEY (lead_id) REFERENCES leads(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS analytics_events (
    id TEXT PRIMARY KEY,
    event_type TEXT NOT NULL,
    metadata TEXT,
    created_at TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_leads_status ON leads(status);
CREATE INDEX IF NOT EXISTS idx_leads_email ON leads(email);
CREATE INDEX IF NOT EXISTS idx_proposals_lead_id ON proposals(lead_id);
CREATE INDEX IF NOT EXISTS idx_feedback_lead_id ON feedback(lead_id);
CREATE INDEX IF NOT EXISTS idx_analytics_event_type ON analytics_events(event_type);
CREATE INDEX IF NOT EXISTS idx_analytics_created_at ON analytics_events(created_at);
"""


def init_db():
    """Initialize the database schema."""
    with get_db() as conn:
        conn.executescript(SCHEMA_SQL)
