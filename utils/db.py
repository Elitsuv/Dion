import sqlite3
import os

DB_PATH = "data/dion.db"

def get_connection():
    # Ensure data folder exists
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    return sqlite3.connect(DB_PATH, check_same_thread=False)

def setup_db():
    conn = get_connection()
    cursor = conn.cursor()
    
    # --- Analytics ---
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS command_usage (
        user_id INTEGER PRIMARY KEY,
        commands_used INTEGER DEFAULT 0
    )
    """)

    # --- Economy / Games ---
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS economy (
        user_id INTEGER PRIMARY KEY,
        coins INTEGER DEFAULT 0,
        xp INTEGER DEFAULT 0,
        level INTEGER DEFAULT 1
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS inventory (
        user_id INTEGER,
        item_id TEXT,
        quantity INTEGER DEFAULT 1,
        PRIMARY KEY (user_id, item_id)
    )
    """)

    # --- Moderation ---
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS warnings (
        warn_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        moderator_id INTEGER,
        reason TEXT,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # --- Events ---
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS events (
        event_id INTEGER PRIMARY KEY AUTOINCREMENT,
        guild_id INTEGER,
        creator_id INTEGER,
        title TEXT,
        description TEXT,
        event_time TEXT,
        message_id INTEGER
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS event_rsvps (
        event_id INTEGER,
        user_id INTEGER,
        status TEXT, -- 'attending', 'maybe', 'not_coming'
        PRIMARY KEY (event_id, user_id)
    )
    """)

    # --- Alerts ---
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS alert_subscriptions (
        user_id INTEGER,
        guild_id INTEGER,
        category TEXT,
        PRIMARY KEY (user_id, guild_id, category)
    )
    """)

    # --- Temp Voice Channels ---
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS temp_voice_config (
        guild_id INTEGER PRIMARY KEY,
        setup_channel_id INTEGER,
        category_id INTEGER
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS active_temp_channels (
        channel_id INTEGER PRIMARY KEY,
        owner_id INTEGER
    )
    """)

    # --- Reminders ---
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS reminders (
        reminder_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        reminder_text TEXT,
        trigger_time TEXT
    )
    """)

    conn.commit()
    conn.close()

# Initialize DB when the module is imported
setup_db()
