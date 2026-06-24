import discord
from discord.ext import commands
from discord import app_commands
from typing import List
import asyncio
import json
import os
import random
import time
import re

CONFIG_FILE = "chain_config.json"

def load_chain_config():
    if not os.path.exists(CONFIG_FILE):
        return {"channel_id": None, "mode": "bot"}
    with open(CONFIG_FILE, "r") as f:
        try:
            return json.load(f)
        except:
            return {"channel_id": None, "mode": "bot"}

def save_chain_config(channel_id, mode):
    with open(CONFIG_FILE, "w") as f:
        json.dump({"channel_id": channel_id, "mode": mode}, f)

COUNTRIES = {
    "afghanistan", "albania", "algeria", "andorra", "angola", "antigua and barbuda", "argentina", "armenia", "australia", 
    "austria", "azerbaijan", "bahamas", "bahrain", "bangladesh", "barbados", "belarus", "belgium", "belize", "benin", 
    "bhutan", "bolivia", "bosnia and herzegovina", "botswana", "brazil", "brunei", "bulgaria", "burkina faso", "burundi", 
    "cabo verde", "cambodia", "cameroon", "canada", "central african republic", "chad", "chile", "china", "colombia", 
    "comoros", "congo", "costa rica", "croatia", "cuba", "cyprus", "czechia", "czech republic", "denmark", "djibouti", 
    "dominica", "dominican republic", "east timor", "ecuador", "egypt", "el salvador", "equatorial guinea", "eritrea", 
    "estonia", "eswatini", "ethiopia", "fiji", "finland", "france", "gabon", "gambia", "georgia", "germany", "ghana", 
    "greece", "grenada", "guatemala", "guinea", "guinea-bissau", "guyana", "haiti", "honduras", "hungary", "iceland", 
    "india", "indonesia", "iran", "iraq", "ireland", "israel", "italy", "ivory coast", "jamaica", "japan", "jordan", 
    "kazakhstan", "kenya", "kiribati", "kuwait", "kyrgyzstan", "laos", "latvia", "lebanon", "lesotho", "liberia", 
    "libya", "liechtenstein", "lithuania", "luxembourg", "madagascar", "malawi", "malaysia", "maldives", "mali", 
    "malta", "marshall islands", "mauritania", "mauritius", "mexico", "micronesia", "moldova", "monaco", "mongolia", 
    "montenegro", "morocco", "mozambique", "myanmar", "namibia", "nauru", "nepal", "netherlands", "new zealand", 
    "nicaragua", "niger", "nigeria", "north korea", "north macedonia", "norway", "oman", "pakistan", "palau", 
    "palestine", "panama", "papua new guinea", "paraguay", "peru", "philippines", "poland", "portugal", "qatar", 
    "romania", "russia", "rwanda", "saint kitts and nevis", "saint lucia", "saint vincent and the grenadines", 
    "samoa", "san marino", "sao tome and principe", "saudi arabia", "senegal", "serbia", "seychelles", "sierra leone", 
    "singapore", "slovakia", "slovenia", "solomon islands", "somalia", "south africa", "south korea", "south sudan", 
    "spain", "sri lanka", "sudan", "suriname", "sweden", "switzerland", "syria", "tajikistan", "tanzania", "thailand", 
    "timor-leste", "togo", "tonga", "trinidad and tobago", "tunisia", "turkey", "turkmenistan", "tuvalu", "uganda", 
    "ukraine", "united arab emirates", "united kingdom", "united states", "united states of america", "uruguay", 
    "uzbekistan", "vanuatu", "venezuela", "vietnam", "yemen", "zambia", "zimbabwe", "us", "usa", "uk", "uae"
}

ISO_MAP = {
    "afghanistan": "af", "albania": "al", "algeria": "dz", "andorra": "ad", "angola": "ao", "antigua and barbuda": "ag",
    "argentina": "ar", "armenia": "am", "australia": "au", "austria": "at", "azerbaijan": "az", "bahamas": "bs",
    "bahrain": "bh", "bangladesh": "bd", "barbados": "bb", "belarus": "by", "belgium": "be", "belize": "bz",
    "benin": "bj", "bhutan": "bt", "bolivia": "bo", "bosnia and herzegovina": "ba", "botswana": "bw", "brazil": "br",
    "brunei": "bn", "bulgaria": "bg", "burkina faso": "bf", "burundi": "bi", "cabo verde": "cv", "cambodia": "kh",
    "cameroon": "cm", "canada": "ca", "central african republic": "cf", "chad": "td", "chile": "cl", "china": "cn",
    "colombia": "co", "comoros": "km", "congo": "cg", "costa rica": "cr", "croatia": "hr", "cuba": "cu", "cyprus": "cy",
    "czechia": "cz", "czech republic": "cz", "denmark": "dk", "djibouti": "dj", "dominica": "dm", "dominican republic": "do",
    "east timor": "tl", "ecuador": "ec", "egypt": "eg", "el salvador": "sv", "equatorial guinea": "gq", "eritrea": "er",
    "estonia": "ee", "eswatini": "sz", "ethiopia": "et", "fiji": "fj", "finland": "fi", "france": "fr", "gabon": "ga",
    "gambia": "gm", "georgia": "ge", "germany": "de", "ghana": "gh", "greece": "gr", "grenada": "gd", "guatemala": "gt",
    "guinea": "gn", "guinea-bissau": "gw", "guyana": "gy", "haiti": "ht", "honduras": "hn", "hungary": "hu", "iceland": "is",
    "india": "in", "indonesia": "id", "iran": "ir", "iraq": "iq", "ireland": "ie", "israel": "il", "italy": "it",
    "ivory coast": "ci", "jamaica": "jm", "japan": "jp", "jordan": "jo", "kazakhstan": "kz", "kenya": "ke", "kiribati": "ki",
    "kuwait": "kw", "kyrgyzstan": "kg", "laos": "la", "latvia": "lv", "lebanon": "lb", "lesotho": "ls", "liberia": "lr",
    "libya": "ly", "liechtenstein": "li", "lithuania": "lt", "luxembourg": "lu", "madagascar": "mg", "malawi": "mw",
    "malaysia": "my", "maldives": "mv", "mali": "ml", "malta": "mt", "marshall islands": "mh", "mauritania": "mr",
    "mauritius": "mu", "mexico": "mx", "micronesia": "fm", "moldova": "md", "monaco": "mc", "mongolia": "mn",
    "montenegro": "me", "morocco": "ma", "mozambique": "mz", "myanmar": "mm", "namibia": "na", "nauru": "nr",
    "nepal": "np", "netherlands": "nl", "new zealand": "nz", "nicaragua": "ni", "niger": "ne", "nigeria": "ng",
    "north korea": "kp", "north macedonia": "mk", "norway": "no", "oman": "om", "pakistan": "pk", "palau": "pw",
    "palestine": "ps", "panama": "pa", "papua new guinea": "pg", "paraguay": "py", "peru": "pe", "philippines": "ph",
    "poland": "pl", "portugal": "pt", "qatar": "qa", "romania": "ro", "russia": "ru", "rwanda": "rw",
    "saint kitts and nevis": "kn", "saint lucia": "lc", "saint vincent and the grenadines": "vc", "samoa": "ws",
    "san marino": "sm", "sao tome and principe": "st", "saudi arabia": "sa", "senegal": "sn", "serbia": "rs",
    "seychelles": "sc", "sierra leone": "sl", "singapore": "sg", "slovakia": "sk", "slovenia": "si", "solomon islands": "sb",
    "somalia": "so", "south africa": "za", "south korea": "kr", "south sudan": "ss", "spain": "es", "sri lanka": "lk",
    "sudan": "sd", "suriname": "sr", "sweden": "se", "switzerland": "ch", "syria": "sy", "tajikistan": "tj",
    "tanzania": "tz", "thailand": "th", "timor-leste": "tl", "togo": "tg", "tonga": "to", "trinidad and tobago": "tt",
    "tunisia": "tn", "turkey": "tr", "turkmenistan": "tm", "tuvalu": "tv", "uganda": "ug", "ukraine": "ua",
    "united arab emirates": "ae", "united kingdom": "gb", "united states": "us", "united states of america": "us",
    "uruguay": "uy", "uzbekistan": "uz", "vanuatu": "vu", "venezuela": "ve", "vietnam": "vn", "yemen": "ye",
    "zambia": "zm", "zimbabwe": "zw", "us": "us", "usa": "us", "uk": "gb", "uae": "ae"
}

def get_flag_emoji(country_name):
    code = ISO_MAP.get(country_name.lower())
    if not code:
        return "🏳️"
    return "".join(chr(127462 + ord(c) - 97) for c in code.lower())

class TicTacToeButton(discord.ui.Button['TicTacToeView']):
    def __init__(self, x: int, y: int):
        super().__init__(style=discord.ButtonStyle.secondary, label='\u200b', row=y)
        self.x = x
        self.y = y

    async def callback(self, interaction: discord.Interaction):
        assert self.view is not None
        view: TicTacToeView = self.view
        state = view.board[self.y][self.x]
        
        if state in (view.X, view.O):
            return

        if interaction.user not in (view.player1, view.player2):
            await interaction.response.send_message("You are not playing this game!", ephemeral=True)
            return

        if view.current_player == view.X and interaction.user != view.player1:
            await interaction.response.send_message("It's not your turn!", ephemeral=True)
            return
        elif view.current_player == view.O and interaction.user != view.player2:
            await interaction.response.send_message("It's not your turn!", ephemeral=True)
            return

        if view.current_player == view.X:
            self.style = discord.ButtonStyle.danger
            self.label = 'X'
            self.disabled = True
            view.board[self.y][self.x] = view.X
            view.current_player = view.O
            content = f"🎮 **Tic-Tac-Toe**\n{view.player1.mention} vs {view.player2.mention}\n\nIt is now {view.player2.mention}'s turn"
        else:
            self.style = discord.ButtonStyle.success
            self.label = 'O'
            self.disabled = True
            view.board[self.y][self.x] = view.O
            view.current_player = view.X
            content = f"🎮 **Tic-Tac-Toe**\n{view.player1.mention} vs {view.player2.mention}\n\nIt is now {view.player1.mention}'s turn"

        winner = view.check_winner()
        if winner is not None:
            engine_cog = view.bot.get_cog('Engine')
            from cogs.engine import save_data

            if winner == view.X:
                content = f"🏆 **{view.player1.mention} won against {view.player2.mention}!**\n🪙✨ **+50 Coins** added to profile!"
                if engine_cog:
                    uid = str(view.player1.id)
                    engine_cog.users.setdefault(uid, {"xp": 0, "level": 1, "coins": 0})
                    engine_cog.users[uid]["coins"] = engine_cog.users[uid].get("coins", 0) + 50
                    await save_data(engine_cog.users)
            elif winner == view.O:
                if view.player2.bot:
                    content = f"🏆 **{view.player2.mention} (Bot) won against {view.player1.mention}!**"
                else:
                    content = f"🏆 **{view.player2.mention} won against {view.player1.mention}!**\n🪙✨ **+50 Coins** added to profile!"
                    if engine_cog:
                        uid = str(view.player2.id)
                        engine_cog.users.setdefault(uid, {"xp": 0, "level": 1, "coins": 0})
                        engine_cog.users[uid]["coins"] = engine_cog.users[uid].get("coins", 0) + 50
                        await save_data(engine_cog.users)
            else:
                content = f"🤝 **It's a tie between {view.player1.mention} and {view.player2.mention}!**\n🪙 **+5 Coins** added to each profile!"
                if engine_cog:
                    for player in (view.player1, view.player2):
                        if not player.bot:
                            pid = str(player.id)
                            engine_cog.users.setdefault(pid, {"xp": 0, "level": 1, "coins": 0})
                            engine_cog.users[pid]["coins"] = engine_cog.users[pid].get("coins", 0) + 5
                    await save_data(engine_cog.users)

            for child in view.children:
                child.disabled = True

            view.stop()
            await interaction.response.edit_message(content=content, view=view)
            return

        if view.player2.bot and view.current_player == view.O:
            await interaction.response.edit_message(
                content=f"🎮 **Tic-Tac-Toe**\n{view.player1.mention} vs {view.player2.mention}\n\n🧠 *Dion Engine predicting best move...*",
                view=view
            )
            
            await asyncio.sleep(1.0)
            
            best_move = view.get_best_move()
            if best_move:
                bx, by = best_move
                view.board[by][bx] = view.O
                
                for child in view.children:
                    if child.x == bx and child.y == by:
                        child.style = discord.ButtonStyle.success
                        child.label = 'O'
                        child.disabled = True
                        break
                        
                view.current_player = view.X
                content = f"🎮 **Tic-Tac-Toe**\n{view.player1.mention} vs {view.player2.mention}\n\nIt is now {view.player1.mention}'s turn"
                
                winner = view.check_winner()
                if winner is not None:
                    engine_cog = view.bot.get_cog('Engine')
                    from cogs.engine import save_data

                    if winner == view.X:
                        content = f"🏆 **{view.player1.mention} won against {view.player2.mention}!**\n🪙✨ **+50 Coins** added to profile!"
                        if engine_cog:
                            uid = str(view.player1.id)
                            engine_cog.users.setdefault(uid, {"xp": 0, "level": 1, "coins": 0})
                            engine_cog.users[uid]["coins"] = engine_cog.users[uid].get("coins", 0) + 50
                            await save_data(engine_cog.users)
                    elif winner == view.O:
                        content = f"🏆 **{view.player2.mention} (Bot) won against {view.player1.mention}!**"
                    else:
                        content = f"🤝 **It's a tie between {view.player1.mention} and {view.player2.mention}!**\n🪙 **+5 Coins** added to profile!"
                        if engine_cog:
                            uid = str(view.player1.id)
                            engine_cog.users.setdefault(uid, {"xp": 0, "level": 1, "coins": 0})
                            engine_cog.users[uid]["coins"] = engine_cog.users[uid].get("coins", 0) + 5
                            await save_data(engine_cog.users)

                    for child in view.children:
                        child.disabled = True
                    view.stop()
            
            if view.message:
                await view.message.edit(content=content, view=view)
        else:
            await interaction.response.edit_message(content=content, view=view)


class TicTacToeView(discord.ui.View):
    children: List[TicTacToeButton]
    X = -1
    O = 1
    Tie = 2

    def __init__(self, bot, player1: discord.Member, player2: discord.Member):
        super().__init__(timeout=180)
        self.bot = bot
        self.player1 = player1
        self.player2 = player2
        self.current_player = self.X
        self.message = None
        self.board = [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0],
        ]

        for y in range(3):
            for x in range(3):
                self.add_item(TicTacToeButton(x, y))

    def check_winner(self):
        for i in range(3):
            if self.board[i][0] == self.board[i][1] == self.board[i][2] and self.board[i][0] != 0:
                return self.board[i][0]
            if self.board[0][i] == self.board[1][i] == self.board[2][i] and self.board[0][i] != 0:
                return self.board[0][i]

        if self.board[0][0] == self.board[1][1] == self.board[2][2] and self.board[0][0] != 0:
            return self.board[0][0]
        if self.board[0][2] == self.board[1][1] == self.board[2][0] and self.board[0][2] != 0:
            return self.board[0][2]

        if all(i != 0 for row in self.board for i in row):
            return self.Tie

        return None

    def get_best_move(self):
        best_val = -1000
        best_move = None
        
        for y in range(3):
            for x in range(3):
                if self.board[y][x] == 0:
                    self.board[y][x] = self.O
                    move_val = self.minimax(0, False)
                    self.board[y][x] = 0
                    if move_val > best_val:
                        best_val = move_val
                        best_move = (x, y)
        return best_move

    def minimax(self, depth, is_max):
        score = self.evaluate_board()
        if score == 10:
            return score - depth
        if score == -10:
            return score + depth
        if not any(i == 0 for row in self.board for i in row):
            return 0

        if is_max:
            best = -1000
            for y in range(3):
                for x in range(3):
                    if self.board[y][x] == 0:
                        self.board[y][x] = self.O
                        best = max(best, self.minimax(depth + 1, False))
                        self.board[y][x] = 0
            return best
        else:
            best = 1000
            for y in range(3):
                for x in range(3):
                    if self.board[y][x] == 0:
                        self.board[y][x] = self.X
                        best = min(best, self.minimax(depth + 1, True))
                        self.board[y][x] = 0
            return best

    def evaluate_board(self):
        for i in range(3):
            if self.board[i][0] == self.board[i][1] == self.board[i][2]:
                if self.board[i][0] == self.O: return 10
                elif self.board[i][0] == self.X: return -10
            if self.board[0][i] == self.board[1][i] == self.board[2][i]:
                if self.board[0][i] == self.O: return 10
                elif self.board[0][i] == self.X: return -10
        if self.board[0][0] == self.board[1][1] == self.board[2][2]:
            if self.board[0][0] == self.O: return 10
            elif self.board[0][0] == self.X: return -10
        if self.board[0][2] == self.board[1][1] == self.board[2][0]:
            if self.board[0][2] == self.O: return 10
            elif self.board[0][2] == self.X: return -10
        return 0

    async def on_timeout(self):
        for child in self.children:
            child.disabled = True
        if self.message:
            try:
                await self.message.edit(content="⏳ **Game timed out due to inactivity!**", view=self)
            except discord.HTTPException:
                pass


class StreakSaveView(discord.ui.View):
    def __init__(self, bot, games_cog, previous_streak, previous_last_country, previous_used_countries, previous_last_user_id, channel):
        super().__init__(timeout=10)
        self.bot = bot
        self.games_cog = games_cog
        self.previous_streak = previous_streak
        self.previous_last_country = previous_last_country
        self.previous_used_countries = previous_used_countries
        self.previous_last_user_id = previous_last_user_id
        self.channel = channel
        self.saved = False
        self.message = None

    @discord.ui.button(label="Save Streak (50 🪙)", style=discord.ButtonStyle.primary, emoji="🛡️")
    async def save_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        engine_cog = self.bot.get_cog('Engine')
        if not engine_cog:
            await interaction.response.send_message("❌ Economy system is unavailable.", ephemeral=True)
            return

        user_id = str(interaction.user.id)
        user_data = engine_cog.users.get(user_id, {"coins": 0})
        user_coins = user_data.get("coins", 0)

        if user_coins < 50:
            await interaction.response.send_message("❌ You do not have enough coins! (Requires 50 🪙)", ephemeral=True)
            return

        engine_cog.users[user_id]["coins"] = user_coins - 50
        engine_cog.users.setdefault("dion_bank", {"coins": 0})
        engine_cog.users["dion_bank"]["coins"] = engine_cog.users["dion_bank"].get("coins", 0) + 50
        
        from cogs.engine import save_data
        await save_data(engine_cog.users)

        self.saved = True
        self.stop()
        button.disabled = True
        await interaction.response.edit_message(content="🛡️ **Streak has been saved!**", view=self)

        self.games_cog.chain_state = {
            "last_country": self.previous_last_country,
            "last_user_id": self.previous_last_user_id,
            "used_countries": self.previous_used_countries,
            "streak": self.previous_streak,
            "last_played_time": time.time(),
            "last_message_id": 0
        }

        last_letter = self.previous_last_country[-1]
        flag = get_flag_emoji(self.previous_last_country)
        next_msg = await self.channel.send(
            f"🛡️ **Streak Saved by {interaction.user.mention}!** Paid **50 🪙** to Dion's Bank.\n"
            f"The streak remains at **{self.previous_streak}** (Last: `{self.previous_last_country.title()}` {flag}).\n"
            f"Next country must start with **{last_letter.upper()}**."
        )
        self.games_cog.chain_state["last_message_id"] = next_msg.id

    async def on_timeout(self):
        if not self.saved:
            self.games_cog.reset_chain()
            for child in self.children:
                child.disabled = True
            try:
                if self.message:
                    await self.message.edit(content="⏳ **Streak save expired!**", view=self)
            except:
                pass
            await self.channel.send("⏳ **Time's up!** The streak could not be saved and has reset to 0.")
            await self.games_cog.send_rules_msg(self.channel)


class Games(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        config = load_chain_config()
        self.chain_channel_id = config.get("channel_id")
        self.chain_mode = config.get("mode", "bot")
        self.reset_chain()

    def reset_chain(self):
        self.chain_state = {
            "last_country": "",
            "last_user_id": 0,
            "used_countries": set(),
            "streak": 0,
            "last_played_time": 0.0,
            "last_message_id": 0
        }

    async def send_rules_msg(self, channel):
        mode_text = "🧑‍🤝‍🧑 **User vs User (Multiplayer)**" if self.chain_mode == "players" else "🤖 **User vs Dion Bot (Co-op)**"
        embed = discord.Embed(
            title="🌍 Country Word Chain Game",
            description=(
                f"**Current Mode:** {mode_text}\n\n"
                "📜 **Rules & How to Play:**\n"
                "1. Enter a country name that starts with the **last letter** of the previous country.\n"
                "2. ⚠️ **IMPORTANT:** You **MUST reply** directly to the bot's latest game message to guess. This ignores normal chats!\n"
                "3. You have only **15 seconds** to reply (Anti-Google speed check!).\n"
                "4. You cannot post twice in a row.\n"
                "5. Duplicate/wrong countries break the streak.\n\n"
                "🎁 **Rewards:**\n"
                "🪙 **+15 Coins** added to your profile per correct guess!\n"
                "🔥 Milestone announcements every 10 streaks!"
            ),
            color=0x005A9C
        )
        msg = await channel.send(embed=embed)
        self.chain_state["last_message_id"] = msg.id
        self.chain_state["last_played_time"] = time.time()

    async def trigger_streak_save_challenge(self, channel, reason_msg):
        # Trigger streak save only if streak > 0
        if self.chain_state["streak"] > 0:
            previous_streak = self.chain_state["streak"]
            previous_last_country = self.chain_state["last_country"]
            previous_used_countries = self.chain_state["used_countries"].copy()
            previous_last_user_id = self.chain_state["last_user_id"]
            
            # Reset immediately in case they don't buy it
            self.reset_chain()
            
            view = StreakSaveView(
                self.bot, self, previous_streak, previous_last_country, 
                previous_used_countries, previous_last_user_id, channel
            )
            prompt_msg = await channel.send(
                f"💥 **{reason_msg}**\n"
                f"Streak broken at **{previous_streak}**. Click below within 10s to save the streak for **50 🪙**!",
                view=view
            )
            self.chain_state["last_message_id"] = prompt_msg.id
            view.message = prompt_msg
        else:
            self.reset_chain()
            await self.send_rules_msg(channel)

    @app_commands.command(name='tictactoe', description="Play Tic-Tac-Toe with a friend or Dion!")
    async def tictactoe(self, interaction: discord.Interaction, opponent: discord.Member):
        """Play Tic-Tac-Toe with a friend or Dion!"""
        if opponent == interaction.user:
            await interaction.response.send_message("You cannot play against yourself!", ephemeral=True)
            return
        if opponent.bot and opponent != self.bot.user:
            await interaction.response.send_message("You cannot play against other bots!", ephemeral=True)
            return

        view = TicTacToeView(self.bot, interaction.user, opponent)
        await interaction.response.send_message(
            content=f"🎮 **Tic-Tac-Toe**\n{interaction.user.mention} vs {opponent.mention}\n\nIt is {interaction.user.mention}'s turn!",
            view=view
        )
        view.message = await interaction.original_response()

    @app_commands.command(name='set_country_chain', description="Sets the active channel for the Country Word Chain game.")
    @app_commands.describe(
        channel="The channel for playing Country Word Chain",
        mode="Game mode: 'bot' (VS Dion) or 'players' (User vs User)"
    )
    @app_commands.choices(mode=[
        app_commands.Choice(name="User vs Bot (Co-op)", value="bot"),
        app_commands.Choice(name="User vs User (Multiplayer)", value="players")
    ])
    @app_commands.default_permissions(manage_channels=True)
    async def set_country_chain(self, interaction: discord.Interaction, channel: discord.TextChannel, mode: str = "bot"):
        """Sets the active channel for the Country Word Chain game."""
        self.chain_channel_id = channel.id
        self.chain_mode = mode
        save_chain_config(channel.id, mode)
        self.reset_chain()
        
        await interaction.response.send_message(f"🌍 Country Chain channel set to {channel.mention} in **{mode}** mode!")
        await self.send_rules_msg(channel)

    @app_commands.command(name='stop_country_chain', description="Stops the Country Word Chain game in this channel.")
    @app_commands.default_permissions(manage_channels=True)
    async def stop_country_chain(self, interaction: discord.Interaction):
        """Stops the Country Word Chain game in this channel."""
        if self.chain_channel_id is None:
            await interaction.response.send_message("❌ No Country Word Chain game is currently active.", ephemeral=True)
            return
            
        self.chain_channel_id = None
        save_chain_config(None, self.chain_mode)
        self.reset_chain()
        await interaction.response.send_message("🌍 **Country Word Chain game has been stopped.** Channel bindings cleared.")

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return

        if self.chain_channel_id is None or message.channel.id != self.chain_channel_id:
            return

        if message.content.startswith("/"):
            return

        if self.chain_state["last_message_id"] > 0:
            if not message.reference or message.reference.message_id != self.chain_state["last_message_id"]:
                return

        country_input = re.sub(r'[^\w\s-]', '', message.content).strip().lower()

        current_time = time.time()
        if self.chain_state["last_country"] and self.chain_state["last_played_time"] > 0:
            elapsed = current_time - self.chain_state["last_played_time"]
            if elapsed > 15.0:
                await message.add_reaction("❌")
                await self.trigger_streak_save_challenge(
                    message.channel, 
                    f"⏳ {message.author.mention} took **{elapsed:.1f}s** to answer (limit: 15s)!"
                )
                return

        if self.chain_state["last_user_id"] == message.author.id:
            await message.add_reaction("❌")
            await message.channel.send(
                f"⚠️ {message.author.mention}, you cannot guess twice in a row!", 
                delete_after=5
            )
            return

        if country_input not in COUNTRIES:
            await message.add_reaction("❌")
            await self.trigger_streak_save_challenge(
                message.channel,
                f"⚠️ `{message.content}` is not recognized as a valid country!"
            )
            return

        if self.chain_state["last_country"]:
            last_char = self.chain_state["last_country"][-1]
            if country_input[0] != last_char:
                await message.add_reaction("❌")
                await self.trigger_streak_save_challenge(
                    message.channel,
                    f"⚠️ `{message.content}` does not start with **{last_char.upper()}**!"
                )
                return

        if country_input in self.chain_state["used_countries"]:
            await message.add_reaction("❌")
            await self.trigger_streak_save_challenge(
                message.channel,
                f"⚠️ `{message.content}` has already been used in this chain!"
            )
            return

        flag = get_flag_emoji(country_input)
        self.chain_state["last_country"] = country_input
        self.chain_state["last_user_id"] = message.author.id
        self.chain_state["used_countries"].add(country_input)
        self.chain_state["streak"] += 1
        self.chain_state["last_message_id"] = message.id
        self.chain_state["last_played_time"] = time.time()

        await message.add_reaction("✅")

        engine_cog = self.bot.get_cog('Engine')
        xp_awarded = 10
        coins_awarded = 15
        if engine_cog:
            user_id = str(message.author.id)
            engine_cog.users.setdefault(user_id, {"xp": 0, "level": 1, "coins": 0, "last_message": 0})
            
            engine_cog.users[user_id]["coins"] = engine_cog.users[user_id].get("coins", 0) + coins_awarded
            engine_cog.users[user_id]["xp"] += xp_awarded
            
            current_level = engine_cog.users[user_id]["level"]
            xp_needed = engine_cog.get_xp_for_level(current_level)
            if engine_cog.users[user_id]["xp"] >= xp_needed:
                engine_cog.users[user_id]["xp"] -= xp_needed
                engine_cog.users[user_id]["level"] += 1
                try:
                    await message.channel.send(f"🎉 **{message.author.mention}** leveled up to **Level {engine_cog.users[user_id]['level']}**!")
                except:
                    pass
            from cogs.engine import save_data
            await save_data(engine_cog.users)

        coin_txt = await message.channel.send(f"🪙 **+15 Coins** added to {message.author.mention}'s vault! (Streak: **{self.chain_state['streak']}**)")
        
        if self.chain_state["streak"] % 10 == 0:
            await message.channel.send(
                f"🔥 **Incredible!** The server is on a **{self.chain_state['streak']} country streak!** "
                f"The next country must start with **{country_input[-1].upper()}**."
            )

        if self.chain_mode == "bot":
            last_letter = country_input[-1]
            possible_countries = [c for c in COUNTRIES if c.startswith(last_letter) and c not in self.chain_state["used_countries"]]
            
            if possible_countries:
                async with message.channel.typing():
                    await asyncio.sleep(1.5)
                    bot_choice = random.choice(possible_countries)
                    bot_flag = get_flag_emoji(bot_choice)
                    
                    self.chain_state["last_country"] = bot_choice
                    self.chain_state["last_user_id"] = self.bot.user.id
                    self.chain_state["used_countries"].add(bot_choice)
                    self.chain_state["streak"] += 1
                    
                    bot_msg = await message.channel.send(f"🤖 **Dion:** `{bot_choice.title()}` {bot_flag} (Streak: **{self.chain_state['streak']}**)")
                    await bot_msg.add_reaction("✅")
                    
                    self.chain_state["last_message_id"] = bot_msg.id
                    self.chain_state["last_played_time"] = time.time()
                    
                    if self.chain_state["streak"] % 10 == 0:
                        await message.channel.send(
                            f"🔥 **Incredible!** The server is on a **{self.chain_state['streak']} country streak!** "
                            f"The next country must start with **{bot_choice[-1].upper()}**."
                        )
            else:
                await message.channel.send(f"🏳️ **I cannot find any unused country starting with {last_letter.upper()}! You win!** Streak: **{self.chain_state['streak']}**")
                self.reset_chain()
                await self.send_rules_msg(message.channel)
        else:
            self.chain_state["last_message_id"] = message.id
            self.chain_state["last_played_time"] = time.time()

async def setup(bot):
    await bot.add_cog(Games(bot))
