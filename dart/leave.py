description = 'Makes the bot disconnect from any voice channel is it in, in the server the command came from.'

async def command(dartbot, message):
    server = message.server
    voice = dartbot.client.voice_client_in(server)
    state = dartbot.music.get_voice_state(server)
    perms = message.author.permissions_in(message.channel)
    if perms.kick_members or message.author.id == dartbot.owner:

        if state.is_playing():
            player = state.player
            player.stop()

        try:
            state.audio_player.cancel()
            del dartbot.music.voice_states[server.id]
            await state.voice.disconnect()
        except:
            pass
    msg = 'Disconnected from ' + voice.channel.name
    await dartbot.client.send_message(message.channel, msg)