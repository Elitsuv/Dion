# 🏢 Dion Discord Bot
<p align="left">
  <img src="assets/dion.png" alt="Dion" width="10%">
</p>

Dion is a feature-rich Discord bot designed to elevate server administration, facilitate active community engagement, manage support tickets, and provide interactive progression and game systems.

---

## 🛠️ Key Features

### 🛡️ Administration & Moderation
Dion provides a secure and comprehensive suite of moderation utilities powered by Discord slash commands:
*   **Security Controls**: Quickly manage server behavior with `/timeout`, `/kick`, and `/ban` commands.
*   **Sector Operations**: Lock down or restore text channels dynamically using `/lock` and `/unlock`.
*   **Clean Sector**: Prune chat clutter easily with the `/clear` command.
*   **Broadcasting**: Authorized personnel can dispatch global `/alert` messages.

### 🎮 Entertainment & Games
Engage your community with built-in interactive game modules and leveling systems:
*   **Tic-Tac-Toe (`/tictactoe`)**: Match up against an opponent or play against Dion's predictive AI engine. Win coins to add to your user profile!
*   **Country Word Chain (`/set_country_chain`)**:
    *   **Co-op Mode**: Play against Dion to keep the country list chain alive.
    *   **Multiplayer Mode**: Challenge other members of the server.
    *   **Anti-Cheat Speed Check**: Players must respond within 15 seconds.
    *   **Streak Protection**: Spend **50 Coins** to save a broken streak!
*   **Employee Profile (`/profile`)**: Track your server leveling progression, accumulated coins, and total XP with a visual progress bar.

### 🎫 Support Ticketing & Engagement
*   **Support Ticket Portal (`/setup_tickets`)**: Initialize a button-driven helpdesk. Users can click to spawn a private, secure channel with server support staff.
*   **Dynamic Voice Hubs (`/setup_voice`)**: Set up a "Join to Create" channel. Dion automatically creates temporary voice lounges for members and cleans them up when empty.
*   **Squad Finder (`/lfg`)**: Let users ping roles and organize multiplayer groups with ease.
*   **Giveaway System (`/giveaway`)**: Host custom reaction-based giveaways with configurable winners and duration.

---

## 📂 Command Directory

| Command | Category | Description | Permissions Required |
| :--- | :--- | :--- | :--- |
| `/help` | General | Opens the Dion Corp command directory | Everyone |
| `/profile [user]` | Progression | View level, coin balance, and XP progress | Everyone |
| `/tictactoe <opponent>` | Games | Challenge a friend or the bot to Tic-Tac-Toe | Everyone |
| `/lfg <game> [role] [details]`| Engagement | Post a looking-for-group lobby announcement | Everyone |
| `/setup_voice` | Voice | Setup the dynamic "Join to Create" voice system | Administrator |
| `/setup_tickets` | Support | Set up the interactive button-based support panel | Administrator |
| `/close_ticket` | Support | Instantly close and archive a support channel | Manage Channels |
| `/giveaway <prize> <duration> [winners]` | Engagement | Initiate an automated reaction giveaway | Manage Events |
| `/clear [amount]` | Moderation | Deletes a specified amount of text messages | Manage Messages |
| `/lock` / `/unlock` | Moderation | Suspend or restore channel typing access | Manage Channels |
| `/timeout <user> <minutes> [reason]` | Moderation | Issue a timeout to a server member | Moderate Members |
| `/kick <user> [reason]` | Moderation | Kick a member from the server | Kick Members |
| `/ban <user> [reason]` | Moderation | Ban a member from the server | Ban Members |
| `/add_role` / `/remove_role` | Moderation | Assign or remove server roles | Manage Roles |
| `/add_level` / `/remove_level` | Admin | Override and set member level | Administrator |
| `/add_xp` / `/remove_xp` | Admin | Manually reward or deduct member XP points | Administrator |
| `/alert <message>` | Utility | Broadcast a system-wide announcement | Administrator |
| `/changelog <version> <changes>` | Utility | Post formatted bot version logs | Administrator |

---

## 🔧 Installation & Setup

### Prerequisites
*   Python 3.8+
*   `discord.py` library
*   `python-dotenv` library

### Installation Steps
1.  **Clone the repository** and navigate to the project directory.
2.  **Install dependencies**:
    ```bash
    pip install discord.py python-dotenv
    ```
3.  **Configure environment variables**:
    Create a `.env` file in the root directory and add your bot token:
    ```env
    DISCORD_TOKEN=YOUR_ACTUAL_TOKEN_HERE
    ```
4.  **Run the bot**:
    ```bash
    python main.py
    ```
