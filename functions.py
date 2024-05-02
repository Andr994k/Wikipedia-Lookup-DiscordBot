import fandom
import requests
from PIL import Image
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from io import BytesIO
import discord


def get_webpage_icon(url):
    
    response = requests.get(url)
    
    soup = BeautifulSoup(response.content, 'html.parser')
    
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
        print(icon_url)

        icon = requests.get(icon_url)

        img = Image.open(BytesIO(icon.content))

        img.save("./imgfiles/wikiicon.png")
        
        return "./imgfiles/wikiicon.png"
    else:
        return None

#icon_url=f"attachment://{get_webpage_icon(page.url)}"
async def get_wiki_result(interaction: discord.Interaction, query, wiki):
    #Try to make the embed, if it fails, send related searches
    #try:
    result = fandom.summary(query, wiki.name)
    if result != None and len(result) < 2048:
        file = discord.File("./imgfiles/wikiicon.png", filename="wikiicon.png")
        page = (fandom.page(title=query, wiki=wiki.name))
        embed = discord.Embed(title=page.title, url=page.url, description=result)
        embed.set_author(name=wiki.name + " Fandom",
                url=f"https://{wiki.name}.fandom.com/wiki/",
                )
        embed.set_thumbnail(url=f"attachment://{get_webpage_icon(page.url)}")

        await interaction.followup.send(file=file, embed=embed)

"""    except:
        await interaction.followup.send("Could not find results, did you mean....")
        await interaction.followup.send(fandom.search(query, wiki.name))"""

