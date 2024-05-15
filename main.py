import discord
import os
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv
from functions import *
from list_scraper import Get_List

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='/', intents=intents)

#Load the .env file containing the token of our bot
load_dotenv()
TOKEN = os.getenv("TOKEN")

class Choice:
    def __init__(self, name, wiki):
        self.name = name
        self.wiki = wiki

@bot.event
async def on_ready():
    print("Connected!")
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} commands")
        pass
    except Exception as e:
        print(e)

wikidict = {
    "games": Get_List("https://wikis.fandom.com/wiki/Category:Games_hub"),
    "shows": Get_List("https://wikis.fandom.com/wiki/Category:TV_hub"),
    "movies": Get_List("https://wikis.fandom.com/wiki/Category:Movies_hub"),
    "music": Get_List("https://wikis.fandom.com/wiki/Category:Music_hub"),
    "books": Get_List("https://wikis.fandom.com/wiki/Category:Books_hub"),
    "lifestyle": Get_List("https://wikis.fandom.com/wiki/Category:Lifestyle_hub"),
    "other": Get_List("https://wikis.fandom.com/wiki/Category:Without_hub"),
    "comics": Get_List("https://wikis.fandom.com/wiki/Category:Comics_hub"),
    "tv": Get_List("https://wikis.fandom.com/wiki/Category:TV_hub"),
}

numberlist = [1,2,3,4,5,6,7,8,9]

Choice = app_commands.Choice

@bot.tree.command(name = "wiki", description = "Searches the given wiki for a given query")
@app_commands.describe(query = "The search subject", wiki = "The wikipedia you want to look up in")
async def lookup(interaction: discord.Interaction, query: str, wiki: str):
    await interaction.response.defer()
    await get_wiki_result(interaction, query, wiki)

@bot.tree.command(name = "wikilist", description = "Lists the available wikis")
@app_commands.describe(category = "The category of wikis")
@app_commands.choices(category=[
    #[Choice(name=key, value=value) for key, value in zip(wikidict.keys(), numberlist)],
    Choice(name='Games', value=1),
    Choice(name='Shows', value=2),
    Choice(name='Movies', value=3),
    Choice(name='Music', value=4),
    Choice(name='Books', value=5),
])
async def wikilist(interaction: discord.Interaction, category: Choice[int]):
    await interaction.response.defer()
    for key, value in wikidict.items():
        if category.name == key.capitalize():
            await interaction.followup.send(f"Here are the available wikis for **{key}**:\n{value}")

bot.run(TOKEN)