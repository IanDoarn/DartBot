description = 'Skips the current song if the command is issued by the requester or starts the vote to skip if they are not'

async def command(dartbot, message):
    state = dartbot.music.get_voice_state(message.server)
    perms = message.author.permissions_in(message.channel)
    if not state.is_playing():
        msg = 'Not playing any music right now.'
    else:
        voter = message.author
        if voter == state.current.requester or perms.kick_members or message.author.id == dartbot.owner:
            msg = 'Requester requested skipping song.'
            state.skip()
        elif voter.id not in state.skip_votes:
            state.skip_votes.add(voter.id)
            total_votes = len(state.skip_votes)
            if total_votes >= 3:
                msg = 'Skip vote passed, skipping song.'
                state.skip()
            else:
                msg = 'Skip vote added, currently at [{}/3]'.format(total_votes)
        else:
            msg = 'You have already voted to skip this song.'
    await dartbot.client.send_message(message.channel, msg)