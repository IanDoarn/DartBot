import discord
description = 'Gets info about current song'

async def command(dartbot, message):
    server_voice = None
    for voice in dartbot.client.voice_clients:
        if voice.guild == message.author.guild:
            server_voice = voice
    if server_voice is None:
        await message.channel.send('I am not connected to any voice chat, dummy!')
        return

    if server_voice.source is None:
        await message.channel.send('There is nothing in the queue right now')
        return

    song = server_voice.source

    if song.metadata is not None:
        embed = discord.Embed(title=song.metadata['title'], description='Uploader: ' + song.metadata['uploader'], color=0xff00ff)
        await message.channel.send(embed=embed)