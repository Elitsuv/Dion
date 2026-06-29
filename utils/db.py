import sqlite3
import os
import threading

DB_PATH = "data/dion.db"

class SQLiteDatabase:
    def __init__(self, path):
        self.path = path
        self.lock = threading.Lock()
        self._init_db()

    def _execute(self, query, params=(), fetchall=False, fetchone=False, commit=False):
        with self.lock:
            conn = sqlite3.connect(self.path)
            conn.row_factory = sqlite3.Row
            try:
                cursor = conn.cursor()
                cursor.execute(query, params)
                if commit:
                    conn.commit()
                if fetchall:
                    return [dict(row) for row in cursor.fetchall()]
                if fetchone:
                    row = cursor.fetchone()
                    return dict(row) if row else None
                return cursor.lastrowid
            finally:
                conn.close()

    def _init_db(self):
        os.makedirs(os.path.dirname(self.path), exist_ok=True)
        self._execute("""
            CREATE TABLE IF NOT EXISTS warnings (
                warn_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT,
                moderator_id TEXT,
                reason TEXT,
                timestamp TEXT
            )
        """, commit=True)
        self._execute("""
            CREATE TABLE IF NOT EXISTS temp_voice_config (
                guild_id TEXT PRIMARY KEY,
                setup_channel_id INTEGER,
                category_id INTEGER
            )
        """, commit=True)
        self._execute("""
            CREATE TABLE IF NOT EXISTS active_temp_channels (
                channel_id TEXT PRIMARY KEY,
                owner_id TEXT
            )
        """, commit=True)
        self._execute("""
            CREATE TABLE IF NOT EXISTS stats (
                user_id TEXT PRIMARY KEY,
                command_count INTEGER DEFAULT 0,
                last_active TEXT
            )
        """, commit=True)
        self._execute("""
            CREATE TABLE IF NOT EXISTS events (
                event_id INTEGER PRIMARY KEY,
                guild_id INTEGER,
                creator_id INTEGER,
                title TEXT,
                description TEXT,
                event_time TEXT,
                message_id INTEGER,
                channel_id INTEGER
            )
        """, commit=True)
        self._execute("""
            CREATE TABLE IF NOT EXISTS event_rsvps (
                event_id INTEGER,
                user_id INTEGER,
                status TEXT,
                PRIMARY KEY (event_id, user_id)
            )
        """, commit=True)
        self._execute("""
            CREATE TABLE IF NOT EXISTS alert_topics (
                topic_id INTEGER PRIMARY KEY AUTOINCREMENT,
                guild_id INTEGER,
                name TEXT,
                role_id INTEGER,
                UNIQUE(guild_id, name)
            )
        """, commit=True)
        self._execute("""
            CREATE TABLE IF NOT EXISTS reaction_roles (
                guild_id TEXT,
                message_id TEXT,
                emoji TEXT,
                role_id TEXT,
                PRIMARY KEY (guild_id, message_id, emoji)
            )
        """, commit=True)


    def add_warning(self, user_id, moderator_id, reason, timestamp):
        self._execute(
            "INSERT INTO warnings (user_id, moderator_id, reason, timestamp) VALUES (?, ?, ?, ?)",
            (str(user_id), str(moderator_id), reason, timestamp),
            commit=True
        )

    def get_warnings(self, user_id):
        return self._execute("SELECT * FROM warnings WHERE user_id = ?", (str(user_id),), fetchall=True)

    def get_temp_voice_config(self, guild_id):
        return self._execute("SELECT setup_channel_id, category_id FROM temp_voice_config WHERE guild_id = ?", (str(guild_id),), fetchone=True)

    def set_temp_voice_config(self, guild_id, setup_channel_id, category_id):
        self._execute(
            "INSERT OR REPLACE INTO temp_voice_config (guild_id, setup_channel_id, category_id) VALUES (?, ?, ?)",
            (str(guild_id), setup_channel_id, category_id),
            commit=True
        )

    def get_active_temp_channel(self, channel_id):
        return self._execute("SELECT owner_id FROM active_temp_channels WHERE channel_id = ?", (str(channel_id),), fetchone=True)

    def set_active_temp_channel(self, channel_id, owner_id):
        self._execute(
            "INSERT OR REPLACE INTO active_temp_channels (channel_id, owner_id) VALUES (?, ?)",
            (str(channel_id), str(owner_id)),
            commit=True
        )

    def remove_active_temp_channel(self, channel_id):
        self._execute("DELETE FROM active_temp_channels WHERE channel_id = ?", (str(channel_id),), commit=True)

    def record_command_usage(self, user_id, active_time):
        self._execute("""
            INSERT INTO stats (user_id, command_count, last_active)
            VALUES (?, 1, ?)
            ON CONFLICT(user_id) DO UPDATE SET
            command_count = command_count + 1,
            last_active = EXCLUDED.last_active
        """, (str(user_id), active_time), commit=True)

    def get_command_usage_stats(self):
        return self._execute("SELECT user_id, command_count, last_active FROM stats ORDER BY command_count DESC LIMIT 15", fetchall=True)

    def add_event(self, event_id, guild_id, creator_id, title, description, event_time, message_id, channel_id):
        self._execute(
            "INSERT INTO events (event_id, guild_id, creator_id, title, description, event_time, message_id, channel_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (event_id, guild_id, creator_id, title, description, str(event_time), message_id, channel_id),
            commit=True
        )

    def get_events(self):
        return self._execute("SELECT * FROM events", fetchall=True)

    def get_guild_events(self, guild_id):
        return self._execute("SELECT * FROM events WHERE guild_id = ?", (guild_id,), fetchall=True)

    def get_event_by_message(self, message_id):
        return self._execute("SELECT * FROM events WHERE message_id = ?", (message_id,), fetchone=True)

    def get_event(self, event_id):
        return self._execute("SELECT * FROM events WHERE event_id = ?", (event_id,), fetchone=True)

    def remove_event(self, event_id):
        with self.lock:
            conn = sqlite3.connect(self.path)
            try:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM events WHERE event_id = ?", (event_id,))
                cursor.execute("DELETE FROM event_rsvps WHERE event_id = ?", (event_id,))
                conn.commit()
            finally:
                conn.close()

    def set_rsvp(self, event_id, user_id, status):
        self._execute(
            "INSERT OR REPLACE INTO event_rsvps (event_id, user_id, status) VALUES (?, ?, ?)",
            (event_id, user_id, status),
            commit=True
        )

    def get_rsvps(self, event_id):
        return self._execute("SELECT user_id, status FROM event_rsvps WHERE event_id = ?", (event_id,), fetchall=True)

    def add_alert_topic(self, guild_id, name, role_id):
        try:
            self._execute(
                "INSERT INTO alert_topics (guild_id, name, role_id) VALUES (?, ?, ?)",
                (guild_id, name.lower(), role_id),
                commit=True
            )
            return True
        except sqlite3.IntegrityError:
            return False

    def remove_alert_topic(self, guild_id, name):
        with self.lock:
            conn = sqlite3.connect(self.path)
            conn.row_factory = sqlite3.Row
            try:
                cursor = conn.cursor()
                cursor.execute("SELECT role_id FROM alert_topics WHERE guild_id = ? AND name = ?", (guild_id, name.lower()))
                row = cursor.fetchone()
                if not row:
                    return None
                role_id = row['role_id']
                cursor.execute("DELETE FROM alert_topics WHERE guild_id = ? AND name = ?", (guild_id, name.lower()))
                conn.commit()
                return role_id
            finally:
                conn.close()

    def get_alert_topics(self, guild_id):
        return self._execute("SELECT name, role_id FROM alert_topics WHERE guild_id = ?", (guild_id,), fetchall=True)

    def get_alert_topic(self, guild_id, name):
        return self._execute("SELECT name, role_id FROM alert_topics WHERE guild_id = ? AND name = ?", (guild_id, name.lower()), fetchone=True)

    def add_reaction_role(self, guild_id, message_id, emoji, role_id):
        self._execute(
            "INSERT OR REPLACE INTO reaction_roles (guild_id, message_id, emoji, role_id) VALUES (?, ?, ?, ?)",
            (str(guild_id), str(message_id), str(emoji), str(role_id)),
            commit=True
        )

    def remove_reaction_role(self, guild_id, message_id, emoji):
        self._execute(
            "DELETE FROM reaction_roles WHERE guild_id = ? AND message_id = ? AND emoji = ?",
            (str(guild_id), str(message_id), str(emoji)),
            commit=True
        )

    def get_reaction_role(self, guild_id, message_id, emoji):
        return self._execute(
            "SELECT role_id FROM reaction_roles WHERE guild_id = ? AND message_id = ? AND emoji = ?",
            (str(guild_id), str(message_id), str(emoji)),
            fetchone=True
        )

    def get_all_reaction_roles(self, guild_id):
        return self._execute(
            "SELECT message_id, emoji, role_id FROM reaction_roles WHERE guild_id = ?",
            (str(guild_id),),
            fetchall=True
        )


db = SQLiteDatabase(DB_PATH)

def get_db():
    return db
