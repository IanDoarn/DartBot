description = 'Disconnects the bot from the server'

async def command(dartbot, message):
    # print(message.content)
    await message.channel.send('I sleep')
    for voice in dartbot.client.voice_clients:
        await voice.disconnect(force=True)
    await dartbot.client.close()