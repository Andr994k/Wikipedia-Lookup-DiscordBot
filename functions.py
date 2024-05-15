import fandom
import requests
import discord
import fast_colorthief
import os
from datetime import datetime
from PIL import Image
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from io import BytesIO

IMG_FILE_PATH = "./imgfiles/wikiicon.png"

def get_webpage_icon(url) -> None:
    """Get the icon of a webpage and save it to a file"""
    #Get wiki and parse it
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    #Look for the icon link
    #Icon is often stored in either link rel="icon" or link rel="shortcut icon"
    icon_link = soup.find("link", rel="icon")
    if not icon_link:
        icon_link = soup.find("link", rel="shortcut icon")
    
    if icon_link:
        #Icon is in the href associated with the link tag
        icon_url = icon_link.get('href')
        
        #Make url absolute using urljoin from urrlib.parse
        if not icon_url.startswith(('http://', 'https://')):
            icon_url = urljoin(url, icon_url)
        
        #Make a new request for the found image URL
        icon = requests.get(icon_url)

        #Open it using BytesIO (magic)
        img = Image.open(BytesIO(icon.content))


        if os.path.exists("./imgfiles"):
            #Save the image/override the previous image (don't want a clutter of images building up)
            img.save(IMG_FILE_PATH)
        else:
            os.makedirs("./imgfiles")
            img.save(IMG_FILE_PATH)

def get_primary_color() -> int:
    """Get the primary color of an image (used for determining the color of the discord embed)"""
    #Get dominant color
    dominant_color = fast_colorthief.get_dominant_color(IMG_FILE_PATH, 1)
    #Convert from RGB to hex
    dominant_color = '#{:02x}{:02x}{:02x}'.format(*dominant_color)
    return int(dominant_color[1:], 16)

def make_embed(wiki, title, description, page, url) -> tuple:
    """Make an embed with different parameters and return the embed and the file for the icon"""
    get_webpage_icon(page.url)
    file = discord.File(IMG_FILE_PATH, filename="wikiicon.png")
    embed = discord.Embed(title=title, url=url, description=description, color=get_primary_color(), timestamp=datetime.now())
    embed.set_author(name=wiki + " Fandom", url=f"https://{wiki}.fandom.com/wiki/", icon_url="attachment://wikiicon.png")
    return file, embed

async def get_wiki_result(interaction: discord.Interaction, query, wiki):
    """Gets the result from a wiki and sends it to the interaction, if it fails, sends related searches instead"""

    #Use list comprehension to capitalize after each space in the given query and wiki
    query = ' '.join(word.capitalize() for word in query.split(' '))
    wiki = ' '.join(word.capitalize() for word in wiki.split(' '))
    #Try to make the embed, if it fails, send related searches
    try:
        page = fandom.page(title=query, wiki=wiki)
        if page.content != None:
            file, embed = make_embed(wiki=wiki, title=page.title, description=page.summary, page=page, url=page.url)
            await interaction.followup.send(file=file, embed=embed)
        else:
            raise Exception("Result doesnt exist")
    except:
        await interaction.followup.send("Could not find results, showing related searches")
        #Search for related pages
        search = (fandom.search(query, wiki))
        #Make sure it returns atleast one result
        if len(search) == 0:
            await interaction.followup.send("No related searches found")
        else:
            #Make a list of titles with their respective URLs, the structure []() is for embedding links in discord
            descriptionlist = []
            for index, element in enumerate(search):
                page = fandom.page(pageid=search[index][1], wiki=wiki)
                descriptionlist.append(f"[{page.title}]({page.url})")
            #Get the first page in the search, used for getting the icon  
            page = fandom.page(pageid=search[0][1], wiki=wiki)
            #Split the list into a string with newlines for each comma
            descriptionlist = '\n'.join(descriptionlist)
            file, embed = make_embed(wiki=wiki, title="Related searches", description=descriptionlist, page=page, url=None)
            await interaction.followup.send(file=file, embed=embed)