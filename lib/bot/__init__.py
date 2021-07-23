from asyncio.tasks import sleep
from glob import glob
from datetime import datetime
import discord
from discord import Intents
from discord.ext.commands import Bot as DiscordBot
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from pathlib import Path
from discord.ext.commands.context import Context
from discord.ext.commands.errors import CommandNotFound

PREFIX = '^'

parent_path = Path(__file__).parent
par_parent_path = parent_path.parent.resolve()

cogs_paths = glob(f'{par_parent_path}/cogs/*.py')
COGS = [path.split('/')[-1][:-3] for path in cogs_paths]

CURSE_WORDS = ['fuck you', 'fuck u', 'fku', 'fk u', 'fk you', 'fuckyou', 'fk', 'fuck']


class Ready(object):
    
    def __init__(self):
        for cog in COGS:
            setattr(self, cog, False)
    
    def ready_up(self, cog):
        setattr(self, cog, True)

    def all_ready(self):
        return all([getattr(self, cog) for cog in COGS])
     

class Bot(DiscordBot):
    
    def __init__(self):
        self.guild = None
        self.ready = False
        self.cogs_ready = Ready()
        self.prefix = PREFIX
        self.schedular = AsyncIOScheduler()

        super().__init__(
            command_prefix=self.prefix,
            intents=Intents.all(),
            case_insensitive=True
        )
    
    def run(self, version):
        self.VERSION = version
        
        print('runnig the setup(loading cogs)')
        self.setup()

        with open(f'{parent_path.resolve()}/token.0', 'r') as f:
            self.TOKEN = f.read()

        print('Runing the bot bbabbbyy')
        super().run(self.TOKEN, reconnect=True)

    def setup(self):
        for cog in COGS:
            self.load_extension(f'lib.cogs.{cog}')
            print(f'{cog} loaded.')


    async def process_commands(self, message):
        ctx = await self.get_context(message, cls=Context)
        if ctx.command is not None and ctx.guild is not None:
            if self.ready:
                await self.invoke(ctx)

            else: 
                await ctx.send('I\'m read not ready to recieve commands. Please wait a few seconds my server isn\'t that powerful')

            
    async def on_connect(self):
         print('Bot connected')

    async def on_ready(self):
        if not self.ready:
            self.guild = self.get_guild(self.guilds[0].id)
            channel_id = None
            for ch in self.guild.channels:
                if isinstance(ch, discord.channel.TextChannel):
                    channel_id = ch.id
                    break
            self.stdout = self.get_channel(channel_id)

            while not self.cogs_ready.all_ready():
                await sleep(0.5)

            self.ready = True
            print('Bot Ready..')

        else:
            print('Bot reconnected')
        
    async def on_disconnect(self):
         print('Bot disconnected')

    async def on_message(self, message):
        if not message.author.bot:
            if message.content.startswith(PREFIX):
                await self.process_commands(message)
            elif 'fuck you' in message.content.lower():
                await message.channel.send(f'FUCK YOU BITCH {message.author.mention}')

    async def on_error(self, err, *args, **kwargs):
        if err == 'on_command_error':
            await args[0].send('Something went wrong.')
        else:
            await self.stdout.send('An error occured.')
        raise
    
    async def on_command_error(self, ctx, exc):
        if isinstance(exc, CommandNotFound):
            pass
        elif hasattr(exc, "original"):
            raise exc.original
        else:
            raise exc
        
bot = Bot()
