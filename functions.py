import fandom
import requests
import discord
import fast_colorthief
from PIL import Image
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from io import BytesIO

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
        img.save("./imgfiles/wikiicon.png")

#Get the primary color of an image (used for determining the color of the discord embed)
def get_primary_color():

    path = "./imgfiles/wikiicon.png"

    #Get dominant color
    dominant_color = fast_colorthief.get_dominant_color(path, 1)

    #Convert from RGB to hex
    dominant_color = '#{:02x}{:02x}{:02x}'.format(*dominant_color)

    return int(dominant_color[1:], 16)


#icon_url=f"attachment://{get_webpage_icon(page.url)}"
async def get_wiki_result(interaction: discord.Interaction, query, wiki):
    #Try to make the embed, if it fails, send related searches
    
    try:
        result = fandom.summary(query, wiki.name)
        if result != None and len(result) < 2048:
            page = (fandom.page(title=query, wiki=wiki.name))
            get_webpage_icon(page.url)
            file = discord.File("./imgfiles/wikiicon.png", filename="wikiicon.png")
            embed = discord.Embed(title=page.title, url=page.url, description=result, color=get_primary_color())
            embed.set_author(name=wiki.name + " Fandom", url=f"https://{wiki.name}.fandom.com/wiki/", icon_url="attachment://wikiicon.png")
            await interaction.followup.send(file=file, embed=embed)
    except:
        await interaction.followup.send("Could not find results, showing related searches")
        search = (fandom.search(query, wiki.name))
        if len(search) == 0:
            await interaction.followup.send("No related searches found")
        else:
            result = fandom.random(pages=1, wiki=wiki.name)
            page_id = result[1]
            page = fandom.page(pageid=page_id, wiki=wiki.name)
            get_webpage_icon(page.url)
            search = [(t[0],) for t in search]
            search = ''.join(['{}\n'.format(t[0]) for t in search])

            file = discord.File("./imgfiles/wikiicon.png", filename="wikiicon.png")
            embed = discord.Embed(title="Related searches", description=search, color=get_primary_color())
            embed.set_author(name=wiki.name + " Fandom", url=f"https://{wiki.name}.fandom.com/wiki/", icon_url="attachment://wikiicon.png")
            await interaction.followup.send(file=file, embed=embed)