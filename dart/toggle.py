description = 'Pause/Resume current song'

async def command(dartbot, message):
    server_voice = None
    for voice in dartbot.client.voice_clients:
        if voice.guild == message.author.guild:
            server_voice = voice
    if server_voice is None:
        await message.channel.send('I am not connected to any voice chat, dummy!')
        return

    if server_voice.source is None:
        await message.channel.send('There is nothing playing right now.')
        return

    if server_voice.is_paused():
        server_voice.resume()
    else:
        server_voice.pause()