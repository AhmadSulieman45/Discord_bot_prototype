from discord import Intents
from discord.ext.commands import Bot as DiscordBot
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from pathlib import Path

PREFIX = '^'
OWNER_IDS = [142005491982139392]

class Bot(DiscordBot):
    def __init__(self):
        self.guild = None
        self.ready = False
        self.prefix = PREFIX
        self.owner_ids = OWNER_IDS
        self.schedular = AsyncIOScheduler()

        super().__init__(
            command_prefix=self.prefix, 
            owner_ids=self.owner_ids,
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
            print('Bot Ready..')
        else:
            print('Bot reconnected')
        
    async def on_disconnect(self):
         print('Bot disconnected')

    async def on_message(self, message):
        pass

bot = Bot()