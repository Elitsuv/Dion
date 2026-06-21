import discord
from discord.ext import commands
from discord import app_commands
from typing import List

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

class Games(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='tictactoe', description="Play Tic-Tac-Toe with a friend!")
    async def tictactoe(self, interaction: discord.Interaction, opponent: discord.Member):
        """Play Tic-Tac-Toe with a friend!"""
        if opponent == interaction.user:
            await interaction.response.send_message("You cannot play against yourself!", ephemeral=True)
            return
        if opponent.bot:
            await interaction.response.send_message("You cannot play against a bot!", ephemeral=True)
            return

        view = TicTacToeView(interaction.user, opponent)
        await interaction.response.send_message(
            content=f"🎮 **Tic-Tac-Toe**\n{interaction.user.mention} vs {opponent.mention}\n\nIt is {interaction.user.mention}'s turn!",
            view=view
        )

async def setup(bot):
    await bot.add_cog(Games(bot))
