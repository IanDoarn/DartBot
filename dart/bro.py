description = 'bruh'

async def command(dartbot, message):
    msg = "what the fuck"
    await dartbot.client.send_message(message.channel, msg)