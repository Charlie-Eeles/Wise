import os
import googletrans
import requests
import sys
import webbrowser
import bs4
from wit import Wit
from discord.ext import commands
from dotenv import load_dotenv
from unit_converter.converter import convert, converts

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
# WIT_TOKEN = os.getenv("WIT_TOKEN")
# witclient = Wit(WIT_TOKEN)
translator = googletrans.Translator()

bot = commands.Bot(command_prefix='!')

@bot.command(name="jc", help="Wise joins voice channel.")
async def join(ctx):
    channel = ctx.author.voice.channel
    await channel.connect()
@bot.command(name="lc", help="Wise leaves voice channel.")
async def leave(ctx):
    await ctx.voice_client.disconnect()

@bot.command(name="tr", help="Translates from auto detected language to a specified language.")
async def translate_func(ctx, i, x):
    tr = translator.translate(text= x, dest=i, src="auto")
    await ctx.send(f"'{tr.text}' translated to {i} from {tr.src}")

@bot.command(name="wi", help="Scrapes wikipedia for the first three sentences of a description.")
async def parse(ctx, x):
    res = requests.get("https://en.wikipedia.org/wiki/"+x)
    info = bs4.BeautifulSoup(res.text, "html.parser", parse_only=bs4.SoupStrainer("p"))
    text = bs4.BeautifulSoup.get_text(info)
    final_text = text.split(". ",3)[:3]
    await ctx.send(f"{final_text[0]}. {final_text[1]}. {final_text[2]}.")

@bot.command(name="cv", help="Converts units from x to y")
async def convert_func(ctx, x, y):
    ans = float(converts(x, y))
    await ctx.send(f"{ans:.2f}")
    

@translate_func.error
async def on_translation_error(ctx, error):
    await ctx.send("An error has been raised, please follow the syntax of '!tr target-language text-to-translate', if that still doesn't work then the language you're trying to translate from or translate to might not be supported.")

@parse.error
async def on_parse_error(ctx, error):
    await ctx.send("I'm sorry, I couldn't find that article. please remember that I only search anglophone wikipedia and if your article is more than one word it must be wrapped in quotation marks.") 

@join.error
async def on_join_error(ctx, error):
    await ctx.send("I'm sorry I can't join the voice channel you're in at the moment, please double check permissions and try again.")

@convert_func.error
async def on_convert_error(ctx, error):
    await ctx.send("Either the units you're using are unsupported or incompatible, please try again with new units.")

bot.run(TOKEN)




#Required for development
    #pip install googletrans
    #pip install -U python-dotenv
    #pip install discord.py
    #pip install beautifulsoup4
    #pip install wit
    #pip install pynacl
    #pip install unit-converter
    #A separate file in the same directory named ".env" 
        #containing a variable "DISCORD_TOKEN = 'your-discord-bot-token'"


#To do: fix permission check before joining voice channel.