description = 'Says \"hello\" back'

async def command(dartbot, message):
    # print(message.content)
    msg = 'Hello {0.author.mention}'.format(message)
    await dartbot.client.send_message(message.channel, msg)