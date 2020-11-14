import os
import googletrans
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
translator = googletrans.Translator()

bot = commands.Bot(command_prefix='!')

@bot.command(name='tr', help='Translates from auto detected language to a specified language.')
async def translate_func(ctx, i, x):
    tr = translator.translate(text= x, dest=i, src="auto")
    await ctx.send(f"'{tr.text}' translated to {i} from {tr.src}")

@translate_func.error
async def on_command_error(ctx, error):
    await ctx.send("An error has been raised, please follow the syntax of '!tr target-language text-to-translate', if that still doesn't work then the language you're trying to translate from or to might not be supported.")

bot.run(TOKEN)

