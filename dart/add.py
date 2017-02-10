from dart.handles import VoiceEntry

description = 'Adds a song to the music playlist. If there is no playlist, one is started, and the bot starts playing music in the connected voice channel.'

async def command(dartbot, message):
    server = message.server
    state = dartbot.music.get_voice_state(server)
    volume = state.volume
    if dartbot.client.is_voice_connected(server):
        voice = dartbot.client.voice_client_in(server)
        if len(message.content) <= 5:
            msg = 'Please include a link to add to the playlist.'
        else:
            try:
                player = await voice.create_ytdl_player(message.content[5:], after=state.toggle_next)
            except Exception as e:
                fmt = 'An error occurred while processing this request: ```py\n{}: {}\n```'
                msg = fmt.format(type(e).__name__, e)
            else:
                entry = VoiceEntry(message, player)
                msg = 'Enqueued ' + str(entry)
                await state.songs.put(entry)
                player.volume = volume
                # player.start()
    else:
        msg = "I am not in a voice channel, please add me to one first."
    await dartbot.client.send_message(message.channel, msg)