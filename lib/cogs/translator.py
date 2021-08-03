from discord.ext.commands import Cog, command
import requests

class Translator(Cog):
    libre_url = None
    def __init__(self, bot):
        self.bot = bot
        self.libre_url = 'https://translate.mentality.rip/'
    
    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up('translator')
            print('Translator Cog ready')

    async def detect_lang(self, sentence):
        payload = {'q' : sentence}
        response = requests.post(f'{self.libre_url}/detect', data=payload)
        res_json = response.json()
        print(res_json)
        return res_json[0]['language']

    async def get_translation(self, sentence, source_lang, target_lang):
        if source_lang == 'auto':
            source_lang = await self.detect_lang(sentence)
        
        payload = {'q' : sentence, 'source' : source_lang, 'target' : target_lang}
        response = requests.post(f'{self.libre_url}/translate', data=payload)
        res_json = response.json()
        return res_json['translatedText']

    @command(name='languages', aliases=['langs'])
    async def list_languages(self, ctx):
        response = requests.post(f'{self.libre_url}/languages')
        res_json = response.json()
        for lang in res_json:
            l = lang['name']
            cd = lang['code']
            await ctx.send(f'language : {l}, code : {cd}')

    @command(name='detect')
    async def detect_language_command(self, ctx, *, message):
        lang = await self.detect_lang(message)
        await ctx.send(f'The language is most likely {lang}')

    @command(name='translate', aliases=['trans', 'translation', 't'])
    async def translate(self, ctx, *, message):
        message = message.split(' ')
        if(len(message) < 3):
            await ctx.send(f'You didn\'t input enough arguments, type (-help translate) for more info')
        else:
            source_lang = message[-2]
            target_lang = message[-1]
            sentence = message[:-2]
            translated = await self.get_translation(sentence, source_lang, target_lang)
            await ctx.send(translated)

def setup(bot):
    bot.add_cog(Translator(bot))