description = 'Lists availible commands and what they do.'

async def command(dartbot, message):
    msg = '`'
    for cmd in dartbot.command_list:
        msg += '{0.prefix}{1.__name__} - {1.description}\n'.format(dartbot, cmd)
    msg += '`'
    await message.channel.send(msg)