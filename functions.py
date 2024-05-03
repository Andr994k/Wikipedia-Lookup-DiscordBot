import fandom
import requests
import discord
import fast_colorthief
import datetime
from PIL import Image
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from io import BytesIO

IMG_FILE_PATH = "./imgfiles/wikiicon.png"

def get_webpage_icon(url):
    
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

        #Save the image/override the previous image (don't want a clutter of images building up)
        img.save(IMG_FILE_PATH)

#Get the primary color of an image (used for determining the color of the discord embed)
def get_primary_color():
    path = IMG_FILE_PATH
    #Get dominant color
    dominant_color = fast_colorthief.get_dominant_color(path, 1)
    #Convert from RGB to hex
    dominant_color = '#{:02x}{:02x}{:02x}'.format(*dominant_color)
    return int(dominant_color[1:], 16)

def make_default_embed(wiki, title, search, page, url):
    get_webpage_icon(page.url)
    file = discord.File(IMG_FILE_PATH, filename="wikiicon.png")
    embed = discord.Embed(title=title, url=url, description=search, color=get_primary_color(), timestamp=datetime.datetime.now())
    embed.set_author(name=wiki.name + " Fandom", url=f"https://{wiki.name}.fandom.com/wiki/", icon_url="attachment://wikiicon.png")
    return file, embed

async def get_wiki_result(interaction: discord.Interaction, query, wiki):
    #Try to make the embed, if it fails, send related searches
    try:
        result = fandom.summary(query, wiki.name)
        if result != None and len(result) < 2048:
            page = (fandom.page(title=query, wiki=wiki.name))
            file, embed = make_default_embed(wiki=wiki, title=page.title, search=result, page=page, url=page.url)
            await interaction.followup.send(file=file, embed=embed)
        else:
            raise Exception("Result too long")
    except:
        await interaction.followup.send("Could not find results, showing related searches")
        #Search for related pages
        search = (fandom.search(query, wiki.name))
        #Make sure it returns atleast one result
        if len(search) == 0:
            await interaction.followup.send("No related searches found")
        else:
            #Make a list of titles with their respective URLs, the structure []() is for embedding links in discord
            descriptionlist = []
            for index, element in enumerate(search):
                page = fandom.page(pageid=search[index][1], wiki=wiki.name)
                descriptionlist.append(f"[{page.title}]({page.url})")
            #Get the first page in the search, used for getting the icon  
            page = fandom.page(pageid=search[0][1], wiki=wiki.name)
            #Split the list into a string with newlines for each comma
            descriptionlist = '\n'.join(descriptionlist)
            file, embed = make_default_embed(wiki=wiki, title="Related searches", search=descriptionlist, page=page, url=None)
            await interaction.followup.send(file=file, embed=embed)