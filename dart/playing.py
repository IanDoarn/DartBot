description = 'Prints the current song info into the channel the command came from'

async def command(dartbot, message):
    state = dartbot.music.get_voice_state(message.server)
    if state.current is None:
        msg = 'Not playing anything.'
    else:
        skip_count = len(state.skip_votes)
        msg = 'Now playing {} [skips: {}/3]'.format(state.current, skip_count)
    await dartbot.client.send_message(message.channel, msg)