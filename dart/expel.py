import discord
description = 'Removes bot from voice channel, if in any'

async def command(dartbot, message):
    server_voice = None
    for voice in dartbot.client.voice_clients:
        if voice.guild == message.author.guild:
            server_voice = voice
    if server_voice is not None:
        await server_voice.disconnect(force=True)
    else:
        await message.channel.send('I am not connected to any voice chat, dummy!')