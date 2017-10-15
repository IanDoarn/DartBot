description = 'Says \"hello\" back'

async def command(dartbot, message):
    # print(message.content)
    await message.channel.send('Real shit! {0.author.mention}'.format(message))