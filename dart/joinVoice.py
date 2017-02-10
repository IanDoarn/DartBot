description = 'Has the bot join a voice channel, or move to another voice channel'

async def command(dartbot, message):
    server = message.server
    msg = 'join voice'
    perms = message.author.permissions_in(message.channel)
    if perms.kick_members or message.author.id == dartbot.owner:
        try:
            if server.voice_client.is_connected:
                # print('changing channel')
                msg = await dartbot.change_channel(message)
        except:
            # print('joining new channel')
            msg = await dartbot.join_channel(message)

    await dartbot.client.send_message(message.channel, msg)


