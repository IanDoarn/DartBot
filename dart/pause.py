description = 'Pauses the music player'

async def command(dartbot, message):
    state = dartbot.music.get_voice_state(message.server)
    perms = message.author.permissions_in(message.channel)
    if perms.kick_members or message.author.id == dartbot.owner:
        if state.is_playing():
            player = state.player
            player.pause()