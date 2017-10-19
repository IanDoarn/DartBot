description = 'Clears the rest of the playlist'

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

    audios = server_voice.source.get_playlist()
    first = audios.pop(0)
    if audios is not None:
        for i in audios:
            i.__del__()
    first.remove_future()
    await message.channel.send('Cleared queue')