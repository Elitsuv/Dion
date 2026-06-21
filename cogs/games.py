import discord
from discord.ext import commands
from discord import app_commands
from typing import List
import asyncio

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
            if winner == view.X:
                content = f"🏆 **{view.player1.mention} won against {view.player2.mention}!**"
            elif winner == view.O:
                content = f"🏆 **{view.player2.mention} won against {view.player1.mention}!**"
            else:
                content = f"🤝 **It's a tie between {view.player1.mention} and {view.player2.mention}!**"

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
                    if winner == view.X:
                        content = f"🏆 **{view.player1.mention} won against {view.player2.mention}!**"
                    elif winner == view.O:
                        content = f"🏆 **{view.player2.mention} won against {view.player1.mention}!**"
                    else:
                        content = f"🤝 **It's a tie between {view.player1.mention} and {view.player2.mention}!**"

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

    def __init__(self, player1: discord.Member, player2: discord.Member):
        super().__init__(timeout=180)
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

    @app_commands.command(name='tictactoe', description="Play Tic-Tac-Toe with a friend or Dion!")
    async def tictactoe(self, interaction: discord.Interaction, opponent: discord.Member):
        """Play Tic-Tac-Toe with a friend or Dion!"""
        if opponent == interaction.user:
            await interaction.response.send_message("You cannot play against yourself!", ephemeral=True)
            return
        if opponent.bot and opponent != self.bot.user:
            await interaction.response.send_message("You cannot play against other bots!", ephemeral=True)
            return

        view = TicTacToeView(interaction.user, opponent)
        await interaction.response.send_message(
            content=f"🎮 **Tic-Tac-Toe**\n{interaction.user.mention} vs {opponent.mention}\n\nIt is {interaction.user.mention}'s turn!",
            view=view
        )
        view.message = await interaction.original_response()

async def setup(bot):
    await bot.add_cog(Games(bot))
