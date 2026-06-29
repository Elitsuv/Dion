# Dion 🦦 v2.2.0

Dion is a lightweight, high-performance Discord companion bot built with `discord.py` and `app_commands`. It features interactive UI elements, persistent voice structures, automated event RSVP management, and opt-in server alert topics.

## ✨ Features

- **🎤 Temporary Voice Channels:** Automatically spawns a private, customizable voice channel when users join a setup channel. Channels delete themselves when empty.
- **📅 Event RSVP Management:** Schedule server events with interactive buttons (✅ ❔ ❌) and automated start alerts that persist and recover across bot reboots.
- **🔔 Opt-in Server Alerts:** A clean subscription-based role announcement system so users only get pinged for topics they opt into.
- **🛡️ Server Moderation:** Straightforward mod commands (`/warn`, `/warnings`, `/timeout`, `/kick`, `/ban`, `/purge`) logged directly to the local database.

---

## 🛠️ Slash Commands Reference

### 🎤 Voice Channels
* `/vc_setup` (Admin) - Initializes the creation category and channel.
* `/vc_lock` | `/vc_unlock` - Locks/unlocks access to your current voice channel.
* `/vc_rename <name>` - Renames your temporary voice channel.
* `/vc_limit <limit>` - Restricts maximum user count.
* `/vc_delete` - Instantly deletes your temporary voice channel.

### 📅 Events
* `/event_create <title> <description> <duration>` - Starts a scheduled event with RSVP buttons (e.g., `2h`, `30m`).
* `/event_list` - Lists upcoming guild events.
* `/event_cancel <id>` (Admin) - Cancels a scheduled event and removes its timer.

### 🔔 Opt-in Alerts
* `/alert_create <name>` (Admin) - Creates a new subscription topic and guild role.
* `/alert_delete <name>` (Admin) - Deletes an alert topic and its guild role.
* `/alert_list` - Shows all available alert topics in the server.
* `/alert_join <name>` - Subscribes/adds the alert role to the user.
* `/alert_leave <name>` - Unsubscribes/removes the alert role from the user.
* `/alert_send <name> <message>` (Admin) - Pings topic subscribers with a styled embed.

### 🛡️ Moderation & Utility
* `/warn <user> <reason>` - Issues a warning to a member.
* `/warnings <user>` (also `/modlogs`) - Lists active warnings for a member.
* `/timeout <user> <minutes> [reason]` - Times out a user.
* `/kick <user> [reason]` - Kicks a user.
* `/ban <user> [reason]` - Bans a user.
* `/purge [amount]` - Deletes up to `amount` messages.
* `/help` - Displays the bot command directory.

---

## 🏗️ Architecture

- **Cogs (`cogs/`):** Separated into modular, reloadable extensions (`utility`, `events`, `alerts`, `moderation`, `help`).
- **Database (`utils/db.py`):** Uses an asynchronous-safe local **SQLite** database (`data/dion.db`) to manage configs, warnings, RSVPs, and scheduled timers.

---

## 🚀 Setup & Local Running

1. **Install dependencies:**
   ```bash
   pip install discord.py python-dotenv
   ```
2. **Environment Variables (`.env`):**
   Create a `.env` file in the bot root:
   ```env
   DISCORD_TOKEN=your_discord_bot_token
   ```
3. **Run the bot:**
   ```bash
   python main.py
   ```
