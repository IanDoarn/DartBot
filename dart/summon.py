import discord
description = 'Brings the bot to the voice channel you\'re in'

async def command(dartbot, message):
    if message.author.voice is not None:
        try:
            await message.author.voice.channel.connect(timeout=10, reconnect=False)
        except discord.errors.ClientException:
            server_voice = None
            for voice in dartbot.client.voice_clients:
                if voice.guild == message.author.guild:
                    server_voice = voice
            if server_voice is not None:
                await server_voice.move_to(message.author.voice.channel)
    else:
        await message.channel.send('You are not in a voice channel {0.author.mention}'.format(message))