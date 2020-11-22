# -------------------------------------------------------------
# Import Statements
# -------------------------------------------------------------
import os
import googletrans
import requests
import sys
import webbrowser
import bs4
import time
import asyncio
import pymongo
import discord
from pymongo import MongoClient
from wit import Wit
from discord.ext import commands
from dotenv import load_dotenv
from unit_converter.converter import convert, converts

# -------------------------------------------------------------
# Keys, related functions and global declarations
# -------------------------------------------------------------
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
MONGO = os.getenv("MONGO")
cluster = MongoClient(MONGO)
discord_database = cluster["Discord"]
reminder_collection = discord_database["Reminders"]
# WIT_TOKEN = os.getenv("WIT_TOKEN")
# witclient = Wit(WIT_TOKEN)
client = discord.Client()
# -------------------------------------------------------------
# Bot commands 
# # -------------------------------------------------------------
async def reminder_poster():
    while not client.is_closed():
        try:
            if reminder_collection.find_one({"_id":int(time.time())}) != None: 
                x = reminder_collection.find_one({"_id":int(time.time())})
                global reminder_message
                reminder_message = x["message"]
                server_id = x["server"]
                channel_id = x["channel"]
                message_id = x["message_id"]
                reminder_collection.delete_one(x)
                channel = bot.get_channel(int(x["channel"]))
                await channel.send(f"{reminder_message} https://discordapp.com/channels/{server_id}/{channel_id}/{message_id}")
            
            await asyncio.sleep(1)
        except Exception as e:
            print(e)
            await asyncio.sleep(1)

bot = commands.Bot(command_prefix='!')

@bot.command(name="rem", help="Set a reminder for yourself.")
async def reminder_func(ctx, x, y, *, arg):
    x_var = int(x)
    unit = str(y)
    if x_var < 1:
        await ctx.send("Invalid value for time, please enter a whole number greater than or equal to one.")
        return
    def simplifier(i,z):
        if i==1:
            return z
        else:
            return z+"s" 
    if unit == "sc" or unit == "second" or unit == "seconds":
        time_in_secs = x_var
        unit = simplifier(x_var, "second")
    elif unit == "mi" or unit == "minute" or unit == "minutes":
        time_in_secs = (x_var * 60)
        unit = simplifier(x_var, "minute")
    elif unit == "hr" or unit == "hour" or unit == "hours":
        time_in_secs = (x_var * 3600)
        unit = simplifier(x_var, "hour")
    elif unit == "dy" or unit == "day" or unit == "days":
        time_in_secs = (x_var * 86400)
        unit = simplifier(x_var, "day")
    elif unit == "wk" or unit == "week" or unit == "weeks":
        time_in_secs = (x_var * 604800)
        unit = simplifier(x_var, "week")
    elif unit == "mn" or unit == "month" or unit == "months":
        time_in_secs = (x_var * 2629743)
        unit = simplifier(x_var, "month")
    elif unit == "yr" or unit == "year" or unit == "years":
        time_in_secs = (x_var * 31556926)
        unit = simplifier(x_var, "year")
    else:
        await ctx.send("Unsupported time format; time must be in one of: seconds, minutes, hours, days, weeks, months or years.")
        return
    time_to_remind = (int(time.time()) + time_in_secs)
    comment_info = {"_id":time_to_remind, "message": arg,"server":ctx.message.guild.id, "channel": ctx.channel.id, "message_id": ctx.message.id}
    reminder_collection.insert_one(comment_info)
    await ctx.send(f"I will remind you in {x} {unit}.")

@bot.command(name="jc", help="Wise joins voice channel.")
async def join(ctx):
    channel = ctx.author.voice.channel
    await channel.connect()
@bot.command(name="ec", help="Wise leaves voice channel.")
async def leave(ctx):
    await ctx.voice_client.disconnect()

@bot.command(name="tr", help="Translates from auto detected language to a specified language.")
async def translate_func(ctx, i, x):
    translator = googletrans.Translator()
    tr = translator.translate(text= x, dest=i, src="auto")
    await ctx.send(f"'{tr.text}' translated to {i} from {tr.src}")

@bot.command(name="wi", help="Scrapes wikipedia for the first three sentences of a description.")
async def parse(ctx,*, x):
    i = x.replace(" ", "_")
    url = "https://en.wikipedia.org/wiki/"+i
    res = requests.get(url)
    info = bs4.BeautifulSoup(res.text, "html.parser", parse_only=bs4.SoupStrainer("p"))
    text = bs4.BeautifulSoup.get_text(info)
    final_text = text.replace("...", ".").split(".",3)[:3]
    await ctx.send(f"{final_text[0]}. {final_text[1]}. {final_text[2]}\nRead more: <{url}>")

@bot.command(name="cv", help="Converts units from x to y")
async def convert_func(ctx, x, y):
    ans = float(converts(x, y))
    await ctx.send(f"{x} is {ans:.2f}{y}'s")


@bot.command(name="file_bug_report", help="file bug report")
async def file_bug(ctx, *, arg):
    user = bot.get_user(98322098304331776)
    await user.send(f"{ctx.author} from {ctx.guild} has reported the following issue(s):\n{arg}")
    await ctx.send("Your bug report has been submitted, thank you.")
    

# -------------------------------------------------------------
# Error catch functions
# -------------------------------------------------------------
@reminder_func.error
async def on_reminder_error(ctx, error):
    await ctx.send("Invalid value for time, please enter a whole number greater than or equal to one.")

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

# -------------------------------------------------------------
# Run command (Keep at the end.)
# -------------------------------------------------------------
client.loop.create_task(reminder_poster())
bot.run(TOKEN)
# -------------------------------------------------------------
#Required for development
    #pip install googletrans
    #pip install -U python-dotenv
    #pip install discord.py
    #pip install beautifulsoup4
    #pip install wit
    #pip install pynacl
    #pip install unit-converter
    #pip install pymongo
    #pip install pymongo[srv]
    #A separate file in the same directory named ".env" 
        #containing a variable "DISCORD_TOKEN = 'your-discord-bot-token'"


#To do: fix permission check before joining voice channel.