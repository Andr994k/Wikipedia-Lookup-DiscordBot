import fandom
import discord

async def get_wiki_result(interaction: discord.Interaction, query, wiki):
    try:
        result = fandom.summary(query, wiki)
        await interaction.followup.send(result)
    except:
        await interaction.followup.send("Could not find results, did you mean....")
        print(fandom.search(query, wiki))
        #await interaction.followup.send(fandom.search(query, wiki))