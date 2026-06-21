import discord
from discord.ext import commands
from discord import app_commands
from typing import List
import asyncio
import json
import os
import random
import time

CONFIG_FILE = "chain_config.json"

def load_chain_config():
    if not os.path.exists(CONFIG_FILE):
        return None
    with open(CONFIG_FILE, "r") as f:
        try:
            return json.load(f).get("channel_id")
        except:
            return None

def save_chain_config(channel_id):
    with open(CONFIG_FILE, "w") as f:
        json.dump({"channel_id": channel_id}, f)

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

        # Valid move
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
                content = f"🏆 **{view.player1.mention} won against {view.player2.mention}!** (+50 🪙)"
                if engine_cog:
                    uid = str(view.player1.id)
                    engine_cog.users.setdefault(uid, {"xp": 0, "level": 1, "coins": 0})
                    engine_cog.users[uid]["coins"] = engine_cog.users[uid].get("coins", 0) + 50
                    save_data(engine_cog.users)
            elif winner == view.O:
                if view.player2.bot:
                    content = f"🏆 **{view.player2.mention} (Bot) won against {view.player1.mention}!**"
                else:
                    content = f"🏆 **{view.player2.mention} won against {view.player1.mention}!** (+50 🪙)"
                    if engine_cog:
                        uid = str(view.player2.id)
                        engine_cog.users.setdefault(uid, {"xp": 0, "level": 1, "coins": 0})
                        engine_cog.users[uid]["coins"] = engine_cog.users[uid].get("coins", 0) + 50
                        save_data(engine_cog.users)
            else:
                content = f"🤝 **It's a tie between {view.player1.mention} and {view.player2.mention}!** (+5 🪙 each)"
                if engine_cog:
                    for player in (view.player1, view.player2):
                        if not player.bot:
                            pid = str(player.id)
                            engine_cog.users.setdefault(pid, {"xp": 0, "level": 1, "coins": 0})
                            engine_cog.users[pid]["coins"] = engine_cog.users[pid].get("coins", 0) + 5
                    save_data(engine_cog.users)

            for child in view.children:
                child.disabled = True

            view.stop()
            await interaction.response.edit_message(content=content, view=view)
            return

        # Handle Bot opponent's turn if applicable
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
                        content = f"🏆 **{view.player1.mention} won against {view.player2.mention}!** (+50 🪙)"
                        if engine_cog:
                            uid = str(view.player1.id)
                            engine_cog.users.setdefault(uid, {"xp": 0, "level": 1, "coins": 0})
                            engine_cog.users[uid]["coins"] = engine_cog.users[uid].get("coins", 0) + 50
                            save_data(engine_cog.users)
                    elif winner == view.O:
                        content = f"🏆 **{view.player2.mention} (Bot) won against {view.player1.mention}!**"
                    else:
                        content = f"🤝 **It's a tie between {view.player1.mention} and {view.player2.mention}!** (+5 🪙)"
                        if engine_cog:
                            uid = str(view.player1.id)
                            engine_cog.users.setdefault(uid, {"xp": 0, "level": 1, "coins": 0})
                            engine_cog.users[uid]["coins"] = engine_cog.users[uid].get("coins", 0) + 5
                            save_data(engine_cog.users)

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

class Games(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.chain_channel_id = load_chain_config()
        self.reset_chain()

    def reset_chain(self):
        self.chain_state = {
            "last_country": "",
            "last_user_id": 0,
            "used_countries": set(),
            "streak": 0,
            "last_played_time": 0.0
        }

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
    @app_commands.default_permissions(manage_channels=True)
    async def set_country_chain(self, interaction: discord.Interaction, channel: discord.TextChannel):
        """Sets the active channel for the Country Word Chain game."""
        self.chain_channel_id = channel.id
        save_chain_config(channel.id)
        self.reset_chain()
        await interaction.response.send_message(
            f"🌍 **Country Word Chain** channel has been set to {channel.mention}!\n"
            f"The game has been initialized. Send a country name to start!"
        )

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return

        if self.chain_channel_id is None or message.channel.id != self.chain_channel_id:
            return

        # Skip slash commands running in the channel
        if message.content.startswith("/"):
            return

        country_input = message.content.strip().lower()

        # 1. Anti-Google timer check (10s limit)
        current_time = time.time()
        if self.chain_state["last_country"] and self.chain_state["last_played_time"] > 0:
            elapsed = current_time - self.chain_state["last_played_time"]
            if elapsed > 10.0:
                await message.add_reaction("❌")
                await message.channel.send(
                    f"⏳ {message.author.mention}, **Time's up!** You took **{elapsed:.1f}s** to answer (limit: 10s). **Streak reset to 0.**", 
                    delete_after=10
                )
                self.reset_chain()
                return

        # 2. Check double posting
        if self.chain_state["last_user_id"] == message.author.id:
            await message.add_reaction("❌")
            await message.channel.send(
                f"⚠️ {message.author.mention}, you cannot go twice in a row!", 
                delete_after=5
            )
            return

        # 3. Check if it's a valid country
        if country_input not in COUNTRIES:
            await message.add_reaction("❌")
            await message.channel.send(
                f"⚠️ `{message.content}` is not recognized as a valid country! **Streak reset to 0.**", 
                delete_after=5
            )
            self.reset_chain()
            return

        # 4. Check starting letter match
        if self.chain_state["last_country"]:
            last_char = self.chain_state["last_country"][-1]
            if country_input[0] != last_char:
                await message.add_reaction("❌")
                await message.channel.send(
                    f"⚠️ `{message.content}` does not start with **{last_char.upper()}**! **Streak reset to 0.**", 
                    delete_after=5
                )
                self.reset_chain()
                return

        # 5. Check if it was already used
        if country_input in self.chain_state["used_countries"]:
            await message.add_reaction("❌")
            await message.channel.send(
                f"⚠️ `{message.content}` has already been used in this chain! **Streak reset to 0.**", 
                delete_after=5
            )
            self.reset_chain()
            return

        # Valid Country! Update state
        self.chain_state["last_country"] = country_input
        self.chain_state["last_user_id"] = message.author.id
        self.chain_state["used_countries"].add(country_input)
        self.chain_state["streak"] += 1

        await message.add_reaction("✅")

        # Award Coins and XP via Engine cog
        engine_cog = self.bot.get_cog('Engine')
        xp_awarded = 10
        coins_awarded = 15
        if engine_cog:
            user_id = str(message.author.id)
            engine_cog.users.setdefault(user_id, {"xp": 0, "level": 1, "coins": 0, "last_message": 0})
            
            engine_cog.users[user_id]["coins"] = engine_cog.users[user_id].get("coins", 0) + coins_awarded
            engine_cog.users[user_id]["xp"] += xp_awarded
            
            # Check level up
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
            save_data(engine_cog.users)

        # Notify milestones
        if self.chain_state["streak"] % 10 == 0:
            await message.channel.send(
                f"🔥 **Incredible!** The server is on a **{self.chain_state['streak']} country streak!** "
                f"The next country must start with **{country_input[-1].upper()}**."
            )

        # Bot's Turn!
        last_letter = country_input[-1]
        possible_countries = [c for c in COUNTRIES if c.startswith(last_letter) and c not in self.chain_state["used_countries"]]
        
        if possible_countries:
            async with message.channel.typing():
                await asyncio.sleep(1.5)
                bot_choice = random.choice(possible_countries)
                
                self.chain_state["last_country"] = bot_choice
                self.chain_state["last_user_id"] = self.bot.user.id
                self.chain_state["used_countries"].add(bot_choice)
                self.chain_state["streak"] += 1
                
                bot_msg = await message.channel.send(f"🤖 **Dion:** `{bot_choice.title()}`")
                await bot_msg.add_reaction("✅")
                
                # Update last played time for the user's turn
                self.chain_state["last_played_time"] = time.time()
                
                if self.chain_state["streak"] % 10 == 0:
                    await message.channel.send(
                        f"🔥 **Incredible!** The server is on a **{self.chain_state['streak']} country streak!** "
                        f"The next country must start with **{bot_choice[-1].upper()}**."
                    )
        else:
            await message.channel.send(f"🏳️ **I cannot find any unused country starting with {last_letter.upper()}! You win!** Streak: **{self.chain_state['streak']}**")
            self.reset_chain()

async def setup(bot):
    await bot.add_cog(Games(bot))
