import fandom
import discord

async def get_wiki_result(interaction: discord.Interaction, query, wiki):
    try:
        result = fandom.summary(query, wiki.name)
        page = (fandom.page(title=query, wiki=wiki.name))
        embed = discord.Embed(title=page.title, url=page.url, description=result)
        await interaction.followup.send(embed=embed)

    except:
        await interaction.followup.send("Could not find results, did you mean....")
        await interaction.followup.send(fandom.search(query, wiki.name))