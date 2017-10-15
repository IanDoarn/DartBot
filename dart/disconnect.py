description = 'Disconnects the bot from the server'

async def command(dartbot, message):
    # print(message.content)
    await message.channel.send('I sleep')
    await dartbot.client.close()