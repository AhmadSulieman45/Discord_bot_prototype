from discord.ext.commands import Cog, command
import requests

class Linguistics(Cog):
    def __init__(self, bot):
        self.bot = bot
        self.libre_url = 'https://translate.mentality.rip'
        self.dic_url = 'https://api.dictionaryapi.dev/api/v2/entries'

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up('linguistics')
            print('Linguistics Cog ready')

    async def get_json(self, url, type="POST", payload=None):
        response = requests.request(type, url, data=payload)
        res_json = response.json()
        return res_json

    async def detect_lang(self, sentence):
        payload = {'q' : sentence}
        res_json = await self.get_json(f'{self.libre_url}/detect', "POST", payload)
        return res_json[0]['language']

    async def get_translation(self, sentence, source_lang, target_lang):
        if source_lang == 'auto':
            source_lang = await self.detect_lang(sentence)
        payload = {'q' : sentence, 'source' : source_lang, 'target' : target_lang}
        res_json = await self.get_json(f'{self.libre_url}/translate', "POST", payload)
        return res_json['translatedText']

    @command(name='languages', aliases=['langs'])
    async def list_languages(self, ctx):
        res_json = await self.get_json(f'{self.libre_url}/languages', "POST")
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

    @command(name='define')
    async def define(self, ctx, *, message):
        """
        Supported languages:
            en_US	English (US)
            hi	Hindi
            es	Spanish
            fr	French
            ja	Japanese
            ru	Russian
            en_GB	English (UK)
            de	German
            it	Italian
            ko	Korean
            pt-BR	Brazilian Portuguese
            ar	Arabic
            tr	Turkish
        i.e:
            ^define en_US love
        """
        message = message.split(' ')
        if(len(message) < 2):
            await ctx.send('You didn\'t use the command probably use ^help define for more information')
            return
        lng_code = message[0]
        word = message[-1]
        res_json = await self.get_json(f'{self.dic_url}/{lng_code}/{word}', "GET")
        # print(res_json)
        # await ctx.send(res_json[0]['phonetics'][0]['audio'])
        try:
            for mean in res_json[0]['meanings']:
                part_spec = mean['partOfSpeech']
                for _def in mean['definitions']:
                    __def = _def['definition']
                    await ctx.send(f'Part of speech : {part_spec}, definiton : {__def}')
        except:
            await ctx.send('This word probably doesn\'t have a defintion in the database')
        
def setup(bot):
    bot.add_cog(Linguistics(bot))