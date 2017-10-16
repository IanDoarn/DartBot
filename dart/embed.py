import discord
from discord import emoji
description = 'Embed testing'


async def command(self, message):
    embed = discord.Embed(title="Tile", description="Desc", color=0x00ff00)
    saved = await message.channel.send(embed=embed)
    await saved.add_reaction('👍')
