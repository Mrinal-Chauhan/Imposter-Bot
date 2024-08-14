import discord
from discord.ext import commands
import config


class MyBot(commands.Bot):
    def __init__(self, command_prefix: str, intents: discord.Intents, **kwargs) -> None:
        super().__init__(command_prefix, intents=intents, **kwargs)

    async def setup_hook(self) -> None:
        await self.load_extension('utils.cogs')
        print('Cogs loaded!')
        await self.tree.sync()

    async def on_ready(self):
        await self.change_presence(activity=discord.activity.Game(name='with Trust'))
        print('Bot tayyar hai bhai!')
    


if __name__ == '__main__':
    bot = MyBot(command_prefix='!',intents=discord.Intents.all())
    bot.run(config.TOKEN)

    