import discord
import requests
from discord import app_commands
from discord.ext import commands

from functions import *

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='/', intents=intents)

TOK_FILE = "token.txt"

def get_token():
  tokfile = open(TOK_FILE, 'r')
  token = tokfile.read()
  tokfile.close()
  return token

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

token = get_token()
bot.run(token)