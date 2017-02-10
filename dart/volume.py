description = 'Changes the volume of the music player, from 0 to 100'

async def command(dartbot, message):
    state = dartbot.music.get_voice_state(message.server)
    msg = 'volume'
    player = state.player
    perms = message.author.permissions_in(message.channel)
    if perms.kick_members or message.author.id == dartbot.owner:
        if state.is_playing():
            if len(message.content) <= 7:
                msg = str(player.volume * 100) +'%'
            else:
                if state.is_playing():
                    player.volume = int(message.content[8:]) / 100
                    if player.volume > 1.0:
                        player.volume = 1.0
                    state.volume = player.volume
                    msg = ('Set the volume to {:.0%}'.format(player.volume))
        else:
            msg = 'No song currently playing.'
    await dartbot.client.send_message(message.channel, msg)