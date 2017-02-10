description = 'Disconnects the bot from the server'

async def command(dartbot, message):
    if message.author.id == dartbot.owner:
        # print(message.content)
        await dartbot.client.close()
    else:
        await dartbot.client.send_message(message.channel, 'You do not have permission to use that command')