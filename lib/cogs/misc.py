from discord.ext.commands import Cog, command
from discord import Member
from typing import Optional
import random
class Misc(Cog):

    def __init__(self, bot):
        self.bot = bot
    
    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up('misc')
            print('Misc Cog ready')
            
    @command(name='slap', aliases=['hit', 'smack'])
    async def slap_member(self, ctx, member: Member, *, reason: Optional[str] = 'They\'re domestic or something IDK MAN (people are sick..)'):
        """
            This here ladies and gentlemen is a function that takes a mention to a person you wanna slap smack and smacks them :) with a mention ;)
        """
        await ctx.send(f'{ctx.author.mention} slapped {member.mention} cuzz {reason}')

    @command(name='Hello', aliases=['Hi', 'Hey', 'Yo', 'Whats up', 'What\'s up'])
    async def ping(self, ctx):
        """
            Okaaayy, soo this basicaly says hi back to you :)
        """
        await ctx.send(f'Wazzup {ctx.author.mention}!')
    
    @command(name='calc')
    async def calc(self, ctx, message:str):
        """
            Give it a mathematical expression it will calculate it for you :) very smart bot very genius <3
            i.e : 5+5
                  7*7
                  69*420
        """
        await ctx.send(eval(message))

    @command(name='random', aliases=['rand', 'rnd', 'choose', 'choice', 'pickone', 'pick'])
    async def rand(self, ctx, *, message):
        """
            Give it bunch of choices it will choose a random one for you. (spaced by spaces)
            i.e : Berger Pizza Shawerma IDK WHAT
        """
        options = message.split(' ')
        if len(options) < 1:
            await ctx.send('You didn\'t provide anything to choose from')
        else:
            await ctx.send(random.choice(options))
            print(options)
            
def setup(bot):
    bot.add_cog(Misc(bot))