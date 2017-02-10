description = 'Makes the bot join, or move to the channel the users is currently in'

async def command(dartbot, message):
    print(message.content)
    summoned_channel = message.author.voice_channel
    server = message.server
    perms = message.author.permissions_in(message.channel)
    if perms.kick_members or message.author.id == dartbot.owner:
        if summoned_channel is None:
            msg = 'You are not in a voice channel.'
        state = dartbot.music.get_voice_state(message.server)
        if state.voice is None:
            voice = await dartbot.client.join_voice_channel(summoned_channel)
            msg = 'Joined ' + summoned_channel.name
            state.voice = voice
        else:
            voice = server.voice_client
            state.voice = voice
            await voice.move_to(summoned_channel)
            msg = 'Joined ' + summoned_channel.name

    await dartbot.client.send_message(message.channel, msg)