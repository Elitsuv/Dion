# Contributing to Dion 🦦

Thank you for your interest in contributing to Dion! Please follow these guidelines to keep the codebase clean and reliable.

## 🛠️ Local Development

1. **Prerequisites:** Python 3.10+ and a discord bot token from the Discord Developer Portal.
2. **Setup:**
   ```bash
   pip install discord.py python-dotenv
   ```
3. **Database:** On startup, Dion initializes an SQLite database file at `data/dion.db`. You can use any SQLite browser to inspect schemas or logs.

## 📝 Code Guidelines

- **Slash Commands Only:** All user interactions must use modern `app_commands` (slash commands). Traditional text-prefix commands should be avoided.
- **Keep Cogs Modular:** New features should go into distinct files under the `cogs/` directory and loaded explicitly in `main.py`.
- **Database Safety:** Do not write inline SQL queries directly in cogs. Add new CRUD methods to the `SQLiteDatabase` manager in `utils/db.py` to maintain a separation of concerns and database thread safety.
- **Clean Styling:** Always return status messages, logs, or command responses using the standardized `DionEmbed` found in `utils/embeds.py`.

## 🚀 Submitting Changes

1. Create a descriptive branch (e.g. `feature/ticket-system` or `bugfix/voice-leak`).
2. Test your changes locally in a private Discord testing server.
3. Open a Pull Request detailing the changes made and steps to verify them.
