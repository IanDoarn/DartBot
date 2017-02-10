description = 'totes'

async def command(dartbot, message):
    # print(message.content)
    msg = 'gay'
    await dartbot.client.send_message(message.channel, msg)