import discord
from discord.ext import commands
from discord import app_commands
from app import MyBot
from games import Game
import text as txt
from enum import Enum
import time
from utils import features
import asyncio
import random



class Adesh(commands.Cog):
    def __init__(self, bot: MyBot):
        super().__init__()
        self.bot = bot
        self.voters = []
        self.players = []
        self.gamestate = 'standby'
        self.gameadmin = ''

    @commands.command()
    async def sync(self,ctx):
        await ctx.send('syncing')
        await self.bot.tree.sync()
        await ctx.send('synced')
        print('Synced!')
    

    # This is the Help Command
    @app_commands.command(name = 'help', description = 'Learn to get started with __ Bot')
    async def help(self,interaction: discord.Interaction):
        view = Help()
        embed = discord.Embed(
                title = "How to play Imposter Game",
                description = txt.TEXT_GAME,
                color=0x2ecc70
                            )
        await interaction.response.send_message(embed=embed,view=view)



    # Here comes the start game command
    class GameMode(Enum):
        WhosTheImposter = 1
        WhoElse = 2
    
    @app_commands.command(name = 'startgame', description = 'Start the game!')
    async def startgame(self, interaction: discord.Interaction, gamemode: GameMode):
        if self.gamestate == 'standby':
            
            self.gamestate = 'starting'

            self.gameadmin = interaction.user

            jointime = str(int(time.time())+31) # The time for joining the game: 30 seconds

            joinEmbed = discord.Embed(
                title = "React to Join!",
                description= txt.TEXT_JOIN.format(gamemode.name,'<t:'+jointime+':R>'),
                color= 0x34D645
            )
            
            await interaction.response.send_message(embed=joinEmbed) # send the message

            msg = await interaction.original_response() # Get the message object for the sent message


            await msg.add_reaction('✅')

            await asyncio.sleep(28)
            # The message is stored in the cache and to get the updated message with reactions.
            # To get the updated message, we retrieve it from the cache using its id.

            cache_msg = discord.utils.get(self.bot.cached_messages, id=msg.id) # Get the message out of the cache after reaction additions

            reaction = cache_msg.reactions # Iterable object containing reactions
            
            for reacts in reaction:
                if str(reacts) == '✅':
                    player = [user async for user in reacts.users()] # List containing the async generator object of the reacted users
            
            
            names = [str(i) for i in player] # list containing the names of the players
            names.remove('bot1#6338') # Removes the Bot from the list

            random.shuffle(names) # Shuffle the list
            self.players = names

            names = '• '+'\n• '.join(names) # Make a bullet list

            if self.players != []:

                # Starting of the Game: 

                orderEmbed = discord.Embed(
                    title="Order of Playing:",
                    description= txt.TEXT_ORDER.format(names),
                    color=0x34D645
                )
                await interaction.edit_original_response(embed=orderEmbed)

                wordsEmbed = discord.Embed(
                    title="Hold up, lemme cook..",
                    description= "**Whispering the words🤫🤥!**",
                    color=0x7DF9FF
                )

                await interaction.followup.send(embed=wordsEmbed)


                ################
                self.game = Game(self.bot,interaction,self.players)
                if gamemode.value == 1:
                    await self.game.WhosTheImposter()
                    self.gamestate = 'ingame'
                elif gamemode.value == 2:
                    await self.game.whoElse()
                    self.gamestate = 'ingame'
            else:
                await interaction.followup.send(f'{interaction.user.mention} No one joined ;/')
                self.gamestate = 'standby'
        else:
            await interaction.response.send_message('A game is already started! Please to wait for it to end.')



    @app_commands.command(name = 'vote', description = 'Launch the Voting Poll')
    async def vote(self, interaction: discord.Interaction):
        
        if self.gamestate == 'ingame':

            user = interaction.user.name

            if len(self.voters) < 2:
                if user in self.players:

                    if user not in self.voters:
                        
                        self.voters.append(user)

                        if len(self.voters) == 1:
                            await interaction.response.send_message('Waiting for one more vote to initiate the poll')

                    else:
                        await interaction.response.send_message('Need one more vote call from someone else!')
                else:
                    await interaction.response.send_message(f'Hey {interaction.user.mention}, You are not a part of this game!')




                
                
            
            # if len(self.voters) > 0 and user not in self.voters:

            if len(self.voters) >= 2:
                # Poll Here
                suspects = self.players

                inimsg = features.inipoll(suspects)

                emojiL = '🇦 🇧 🇨 🇩 🇪 🇫 🇬 🇭 🇮 🇯 🇰 🇱 🇲 🇳 🇴 🇵 🇶 🇷 🇸 🇹 🇺 🇻 🇼 🇽 🇾 🇿'.split()

                poll_embed = discord.Embed(
                    title="Who is the Imposter?",
                    description= txt.TEXT_POLL.format(inimsg),
                    color= 0x00FFFF
                )
                
                await interaction.response.send_message(embed=poll_embed)

                msg = await interaction.original_response()

                for num in range(len(suspects)):
                    await msg.add_reaction(emojiL[num])
                
                await asyncio.sleep(31)

                cachemsg = discord.utils.get(self.bot.cached_messages, id=msg.id)

                await asyncio.sleep(5)

                reactions = cachemsg.reactions

                polldata = []
                votedata = {}

                for reacts in reactions:
                    if str(reacts.emoji) in emojiL:
                        polldata.append((reacts.emoji,reacts.count))

                for i in range(len(polldata)):
                    votedata.update({self.players[i]:polldata[i][1]-1})
                
                print(votedata)
                

                finimsg = features.finipoll(votedata)

                result_msg = finimsg + '\n\n'

                sorted_items = sorted(votedata.items(), key=lambda x: x[1], reverse=True)

                result_flag = False

                if all(value == 0 for value in votedata.values()): # No votes
                    result_msg += 'No Votes, Continue the game!'
                elif sorted_items[0][1] == sorted_items[1][1]: # tie
                    result_msg += "It's a tie bro :/"
                else:
                    result_msg += "Prime Suspect: " + sorted_items[0][0]
                    result_flag = True

                finipoll_embed = discord.Embed(
                    title = "Vote Results:",
                    description = result_msg,
                    color= 0xff1919
                )
                result_embed = discord.Embed(
                    title="Results:",
                    description = f"{Game.WhosTheImposter().}"
                )
                await interaction.followup.send(embed=finipoll_embed)
                

        else:
            await interaction.response.send_message(f"{interaction.user.mention} No game started yet ¯\_(ツ)_/¯")    
    

    @app_commands.command(name = 'endgame', description = 'End an ongoing game!')
    async def endgame(self, interaction: discord.Interaction):
        if self.gamestate == 'ingame':
            if interaction.user.name == self.gameadmin.name:
                end_Embed = discord.Embed(
                    title = "The Game Ended",
                    description=f"The game was ended by {self.gameadmin.mention}!\nHope You enjoyed!",
                    color= 0xFF5733
                )
                await interaction.response.send_message(embed=end_Embed)
            else:
                await interaction.response.send_message(f'{interaction.user.mention} Only the one who has started can end the game!')
        else:
            await interaction.response.send_message(f'{interaction.user.mention} No Game to end bro-')




            
        


    
            




    @app_commands.command(name = 'test', description = 'test commands')
    async def test(self,interaction: discord.Interaction):

        # user = discord.utils.get(interaction.guild.members, name='cyret')
        # await user.send('hi murinaru')
        # print(str(user))
        msg_id = interaction.message.id

        await interaction.response.send_message(f'hi {interaction.user.mention}')
        # msg_id = interaction.user.fetch_message(interaction.message.id)
        
        print(msg_id)



class Help(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None

    @discord.ui.button(label="GAME",style=discord.ButtonStyle.green)
    async def menu1(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(
            title = "How to play Imposter Game",
            description = txt.TEXT_GAME,
            color=0x2ecc70
                        )
        await interaction.response.edit_message(embed=embed)

    @discord.ui.button(label="FEATURES",style=discord.ButtonStyle.blurple)
    async def menu2(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(
            title = "What does the Bot do?",
            description = txt.TEXT_FEATURES,
            color=0x5436cd
                        )
        await interaction.response.edit_message(embed=embed)

    @discord.ui.button(label="COMMANDS",style=discord.ButtonStyle.grey)
    async def menu3(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(
            title = "Bot Commands:",
            description = txt.TEXT_COMMANDS,
            color=0x8f929e
                        )
        await interaction.response.edit_message(embed=embed)

    @discord.ui.button(label="❌",style=discord.ButtonStyle.red)
    async def menu4(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("Happy to help you",ephemeral=True)
        self.value = False
        self.stop()

    

async def setup(bot: commands.Bot):
    await bot.add_cog(Adesh(bot))