# Dion Discord Bot

A powerful Discord bot with automated systems, engaging features, and built-in predictive modules.

## Features
- 🛡️ **Admin Commands**: Secure moderation commands (`/clear`, `/lock`, `/unlock`, `/alert`) powered by Discord slash commands.
- 🧠 **Engine System**: Predictive modeling (`/predict`) and linear algebra calculations (`/matrix`).
- 🎮 **Emoji Game**: A 3x3 interactive emoji guessing game to engage users (`/guess`).
- 🌐 **NLP World Cup Predictions**: Natural Language Processing driven world cup prediction module (`/nlp_predict`). Ask the bot who will win a match between two teams!

## Setup Instructions

### Prerequisites
- Python 3.8+
- `discord.py` library
- `numpy` library
- `python-dotenv` library

### Installation
1. Clone the repository and navigate to the project directory.
2. Install the required dependencies:
   ```bash
   pip install discord.py numpy python-dotenv
   ```
3. Set up the `.env` file for your security token (see below).

## Security and The `.env` File

**⚠️ IMPORTANT: Never share your Discord bot token or commit it to a public repository!**

To keep your bot's token secure, we use a `.env` file. The `.gitignore` file included in this repository ensures that this file will never be committed to Git.

**How to set up the `.env` file:**
1. In the root directory of the project (where `main.py` is located), create a new file and name it exactly `.env`.
2. Open `.env` in your text editor and add the following line, replacing `YOUR_ACTUAL_TOKEN_HERE` with your real bot token:
   ```env
   DISCORD_TOKEN=YOUR_ACTUAL_TOKEN_HERE
   ```
3. Save the file. The code in `main.py` will automatically read this token without exposing it in the codebase.

## Running the Bot
Once your `.env` file is set up and dependencies are installed, you can start the bot by running:
```bash
python main.py
```
The bot will initialize its extensions and sync its slash commands globally.
