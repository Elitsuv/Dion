# Dion 🦦 v2.1.0

Dion is a lightweight, modern, and highly polished Discord companion bot built for private community servers. Built with `discord.py` and `app_commands`, Dion prioritizes clean architecture, native UI components (buttons, embeds), and a strict "quality over quantity" design philosophy.

## ✨ Features

- **🎤 Temporary Voice Channels:** Users can join a dedicated "Create Voice" channel, and Dion will instantly spawn a private, temporary voice lounge that deletes itself when empty.
- **📅 Event Management:** Schedule server events with interactive, real-time RSVP buttons (✅ ❔ ❌) and automated timer notifications.
- **🔔 Opt-in Alerts:** A category-based subscription system so users only get pinged for the topics they care about.
- **🛡️ Essential Moderation & Utility:** Clean, non-bloated moderation tools to keep your server safe.

## 🏗️ Architecture

To keep the codebase maintainable for solo development, Dion is consolidated into three core extensions:
1. `cogs/utility.py` - Temporary Voice logic.
2. `cogs/events.py` - Event scheduling and RSVP tracking.
3. `cogs/moderation.py` - Core server moderation tools.

Data is stored locally and synchronously using **SQLite** (`data/dion.db`), ensuring reliable data persistence without the overhead of heavy external databases.

## 🚀 Setup & Installation

1. **Clone the repository:**
   ```bash
   git clone <repo-url>
   cd Dion
   ```

2. **Install dependencies:**
   Make sure you have Python 3.11+ installed.
   ```bash
   pip install discord.py python-dotenv
   ```

3. **Configure Environment:**
   Create a `.env` file in the root directory and add your bot token:
   ```env
   DISCORD_TOKEN=your_bot_token_here
   ```

4. **Run the bot:**
   ```bash
   python main.py
   ```

## 🛠️ Post-Setup

- Run `/vc setup` in your server to initialize the Temporary Voice Channel category.
- Enjoy!
