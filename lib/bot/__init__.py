from __future__ import generator_stop
from datetime import datetime
import discord
from discord import Intents
from discord import channel
from discord.ext.commands import Bot as DiscordBot
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from discord import Embed
from pathlib import Path
from discord.ext.commands.errors import CommandNotFound

from discord.partial_emoji import _EmojiTag
PREFIX = '^'

class Bot(DiscordBot):
    def __init__(self):
        self.guild = None
        self.ready = False
        self.prefix = PREFIX
        self.schedular = AsyncIOScheduler()

        super().__init__(
            command_prefix=self.prefix,
            intents=Intents.all()
        )
    
    def run(self, version):
        self.VERSION = version
        parent_path = Path(__file__).parent.resolve()
        with open(f'{parent_path}/token.0', 'r') as f:
            self.TOKEN = f.read()
        print('Runing the bot bbabbbyy')
        super().run(self.TOKEN, reconnect=True)

    async def on_connect(self):
         print('Bot connected')

    async def on_ready(self):
        if not self.ready:
            self.ready = True
            self.guild = self.get_guild(self.guilds[0].id)
            channel_id = None
            for ch in self.guild.channels:
                if isinstance(ch, discord.channel.TextChannel):
                    channel_id = ch.id
                    break
            self.general_channel = self.get_channel(channel_id)
            embed = Embed(  title='I have ZERO idea of how this is gonna be honestly',
                            description='Test butt is online And I\'m just messing with the embeds',
                            colour=0xc0392b,
                            timestamp=datetime.utcnow())
            embed.add_field(name='Maybe this is the Name', value='And hopefuly this is the value', inline=True)
            embed.add_field(name='This should be next to the last one i guess ? ', value='Hopefully ya3ni', inline=True)
            embed.set_author(name='The holy Butt Bot', icon_url=self.guild.icon_url)
            embed.set_thumbnail(url=self.guild.icon_url)
            embed.set_image(url=self.guild.icon_url)
            embed.set_footer(text='Wow im dooown booi')
            await self.general_channel.send(embed=embed)
            print('Bot Ready..')
        else:
            print('Bot reconnected')
        
    async def on_disconnect(self):
         print('Bot disconnected')

    async def on_message(self, message):
        pass
    
    async def on_error(self, err, *args, **kwargs):
        if err == 'on_command_error':
            await args[0].send('Something went wrong.')
        else:
            await self.general_channel.send('An error occured.')
        raise
    
    async def on_command_error(self, ctx, exc):
        if isinstance(exc, CommandNotFound):
            pass
        elif hasattr(exc, "original"):
            raise exc.original
        else:
            raise exc

bot = Bot()