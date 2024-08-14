import discord
from discord.ext import commands
import words
import random


class Game:
    def __init__(self, bot: commands.Bot, interaction: discord.Interaction, players: list):
        super().__init__()
        self.bot = bot
        
        self.players = players
        self.interaction = interaction


    async def WhosTheImposter(self):
        # In this mode, there's only a single imposter.
        
        # The below list contains the user object list of the players
        player_list = [discord.utils.get(self.interaction.guild.members, name = username) for username in self.players]

        
        imposter = random.choice(player_list) # Randomly chosen imposter
        
        word = random.choice(words.wordlist) # Randomly chosen word

        # The below loop is for distribution of the word
        for num in range(len(player_list)):
            if str(player_list[num]) == str(imposter):
                await imposter.send(f'Shh! {imposter.mention}, You are the **IMPOSTER!**')
            else:
                await player_list[num].send(f"Hey {player_list[num].mention}, Your word is: **{word}**")

        
        await self.interaction.followup.send('Start Playing!')
        
        self.flag = True
        
        return imposter

   
    

    def whoElse(self):
        pass