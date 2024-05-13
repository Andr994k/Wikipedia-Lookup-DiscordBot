import discord
import requests
import os
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv
from functions import *

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='/', intents=intents)

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
        #synced = await bot.tree.sync()
        #print(f"Synced {len(synced)} commands")
        pass
    except Exception as e:
        print(e)

Choice = app_commands.Choice
@bot.tree.command(name = "wiki", description = "Searches the given wiki for a given query")
@app_commands.describe(query = "The search subject", wiki = "The wikipedia you want to look up in")
@app_commands.choices(wiki=[
    Choice(name='Terraria', value=1),
    Choice(name='Minecraft', value=2),
    Choice(name='EldenRing', value=3),
])
async def lookup(interaction: discord.Interaction, query: str, wiki: Choice[int]):
    await interaction.response.defer()
    await get_wiki_result(interaction, query, wiki)

bot.run(TOKEN)