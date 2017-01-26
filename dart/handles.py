import discord
import asyncio


class VoiceEntry:
    def __init__(self, message, player):
        self.requester = message.author
        self.channel = message.channel
        self.player = player

    def __str__(self):
        fmt = '*{0.title}* uploaded by {0.uploader} and requested by {1.display_name}'
        duration = self.player.duration
        if duration:
            fmt += ' [length: {0[0]}m {0[1]}s]'.format(divmod(duration, 60))
        return fmt.format(self.player, self.requester)


class VoiceState:
    def __init__(self, client_):
        self.current = None
        self.voice = None
        self.bot = client_
        self.play_next_song = asyncio.Event()
        self.songs = asyncio.Queue()
        self.skip_votes = set()  # a set of user_ids that voted
        self.audio_player = self.bot.loop.create_task(self.audio_player_task())
        self.volume = 0.6

    def is_playing(self):
        if self.voice is None or self.current is None:
            return False

        player = self.current.player
        return not player.is_done()

    @property
    def player(self):
        return self.current.player

    def skip(self):
        self.skip_votes.clear()
        if self.is_playing():
            self.player.stop()

    def toggle_next(self):
        self.bot.loop.call_soon_threadsafe(self.play_next_song.set)

    async def audio_player_task(self):
        """print('audio_player_task')"""
        while True:
            '''print('true')'''
            self.play_next_song.clear()
            self.current = await self.songs.get()
            '''print(self.current.channel)'''
            await self.bot.send_message(self.current.channel, 'Now playing ' + str(self.current))
            print(str(self.current))
            self.current.player.start()
            await self.play_next_song.wait()


class Music:
    """Voice related commands.
    Works in multiple servers at once.
    """
    def __init__(self, bot):
        self.bot = bot
        self.voice_states = {}

    def get_voice_state(self, server):
        state = self.voice_states.get(server.id)
        if state is None:
            state = VoiceState(self.bot)
            self.voice_states[server.id] = state

        return state

    def __unload(self):
        for state in self.voice_states.values():
            try:
                state.audio_player.cancel()
                if state.voice:
                    self.bot.loop.create_task(state.voice.disconnect())
            except:
                pass


def pm(destination, message):
    """function used to send pms to users"""
    return

async def join_channel(message):
    server = message.server
    bot = server.me
    # print(server.channels)
    # print(message.content)
    msg = 'joinVoice'
    if len(message.content) > 10:
        channel_name = message.content[11:]
        for channels in server.channels:
            perms = channels.permissions_for(bot)
            if channels.name == channel_name:
                if channels.type.name == 'voice':
                    if perms.connect and perms.speak and perms.use_voice_activation:
                        voice = await client.join_voice_channel(channels)
                        state = music.get_voice_state(message.server)
                        state.voice = voice
                        msg = 'Joining channel ' + voice.channel.name
                        break
                    else:
                        msg = 'I am not allowed in ' + channels.name + '. Please check the channel permissions.'
                        break
                else:
                    msg = "Given Channel is not a voice channel."
                    break
            msg = "Channel does not exist"

    else:
        for channels in server.channels:
            # print(channels)
            perms = channels.permissions_for(bot)
            if channels.type.name == 'voice' and perms.connect and perms.speak and perms.use_voice_activation:
                voice = await client.join_voice_channel(channels)
                client.join_voice_channel(channels)
                state = music.get_voice_state(message.server)
                state.voice = voice
                msg = 'Joined channel ' + voice.channel.name
    return msg

async def change_channel(message):
    server = message.server
    voice = server.voice_client
    bot = server.me
    # print(server.channels)
    # print(message.content)
    msg = 'joinVoice'
    if len(message.content) > 10:
        channel_name = message.content[11:]
        for channels in server.channels:
            perms = channels.permissions_for(bot)
            if channels.name == channel_name:
                if channels.type.name == 'voice':
                    if perms.connect and perms.speak and perms.use_voice_activation:
                        await voice.move_to(channels)
                        msg = 'Joining channel ' + voice.channel.name
                        break
                    else:
                        msg = 'I am not allowed in ' + channels.name + '. Please check the channel permissions.'
                        break
                else:
                    msg = "Given Channel is not a voice channel."
                    break
            msg = "Channel does not exist"

    else:
        for channels in server.channels:
            # print(channels)
            perms = channels.permissions_for(bot)
            if channels.type.name == 'voice' and perms.connect and perms.speak and perms.use_voice_activation:
                await voice.move_to(channels)
                msg = 'Joined channel ' + voice.channel.name
    return msg


client = discord.Client()
music = Music(client)
command = '!'  # just have to change this line to change command prefix
owner = '144634215693156353'


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


@client.event
async def on_message(message):
    # print(message.content)
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

    if message.content.startswith(command + 'hello'):
        # print(message.content)
        msg = 'Hello {0.author.mention}'.format(message)
        await client.send_message(message.channel, msg)

    if message.content.startswith(command + 'help'):
        # print(message.content)
        msg = 'I need an adult!'
        await client.send_message(message.channel, msg)

    if message.content.startswith('tot'):
        # print(message.content)
        msg = 'gay'
        await client.send_message(message.channel, msg)

    if message.content.startswith(command + 'disconnect'):
        if message.author.id == owner:
            # print(message.content)
            await client.close()
        else:
            await client.send_message(message.channel, 'You do not have permission to use that command')

# voice related commands below here
    if message.content.startswith(command + 'joinVoice'):
        server = message.server
        msg = 'join voice'
        perms = message.author.permissions_in(message.channel)
        if perms.manage_server or message.author.id == owner:
            try:
                if server.voice_client.is_connected:
                    # print('changing channel')
                    msg = await change_channel(message)
            except:
                # print('joining new channel')
                msg = await join_channel(message)

        await client.send_message(message.channel, msg)

    if message.content.startswith(command + 'summon'):
        print(message.content)
        summoned_channel = message.author.voice_channel
        server = message.server
        perms = message.author.permissions_in(message.channel)
        if perms.manage_server or message.author.id == owner:
            if summoned_channel is None:
                msg = 'You are not in a voice channel.'
            state = music.get_voice_state(message.server)
            if state.voice is None:
                voice = await client.join_voice_channel(summoned_channel)
                msg = 'Joined ' + summoned_channel.name
                state.voice = voice
            else:
                voice = server.voice_client
                state.voice = voice
                await voice.move_to(summoned_channel)
                msg = 'Joined ' + summoned_channel.name

        await client.send_message(message.channel, msg)

    if message.content.startswith(command + 'leave'):
        server = message.server
        voice = client.voice_client_in(server)
        state = music.get_voice_state(server)
        perms = message.author.permissions_in(message.channel)
        if perms.manage_server or message.author.id == owner:

            if state.is_playing():
                player = state.player
                player.stop()

            try:
                state.audio_player.cancel()
                del music.voice_states[server.id]
                await state.voice.disconnect()
            except:
                pass
        msg = 'Disconnected from ' + voice.channel.name
        await client.send_message(message.channel, msg)

    if message.content.startswith(command + 'bro'):
        msg = "what the fuck"
        await client.send_message(message.channel, msg)

    if message.content.startswith(command + 'add'):
        server = message.server
        state = music.get_voice_state(server)
        volume = state.volume
        if client.is_voice_connected(server):
            voice = client.voice_client_in(server)
            if len(message.content) <= 5:
                msg = 'Please include a link to add to the playlist.'
            else:
                player = await voice.create_ytdl_player(message.content[5:], after=state.toggle_next)
                entry = VoiceEntry(message, player)
                msg = 'Enqueued ' + str(entry)
                await state.songs.put(entry)
                player.volume = volume
                # player.start()
        else:
            msg = "I am not in a voice channel, please add me to one first."
        await client.send_message(message.channel, msg)

    if message.content.startswith(command + 'volume'):
        state = music.get_voice_state(message.server)
        msg = 'volume'
        player = state.player
        perms = message.author.permissions_in(message.channel)
        if perms.manage_server or message.author.id == owner:
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
        await client.send_message(message.channel, msg)

    if message.content.startswith(command + 'skip'):
        state = music.get_voice_state(message.server)
        perms = message.author.permissions_in(message.channel)
        if not state.is_playing():
            msg = 'Not playing any music right now.'
        else:
            voter = message.author
            if voter == state.current.requester or perms.manage_server or message.author.id == owner:
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
        await client.send_message(message.channel, msg)

    if message.content.startswith(command + 'playing'):
        state = music.get_voice_state(message.server)
        if state.current is None:
            msg = 'Not playing anything.'
        else:
            skip_count = len(state.skip_votes)
            msg = 'Now playing {} [skips: {}/3]'.format(state.current, skip_count)
        await client.send_message(message.channel, msg)

    if message.content.startswith(command + 'pause'):
        state = music.get_voice_state(message.server)
        perms = message.author.permissions_in(message.channel)
        if perms.manage_server or message.author.id == owner:
            if state.is_playing():
                player = state.player
                player.pause()

    if message.content.startswith(command + 'play'):
        state = music.get_voice_state(message.server)
        perms = message.author.permissions_in(message.channel)
        if perms.manage_server or message.author.id == owner:
            if state.is_playing():
                player = state.player
                player.resume()


def main(token):
    client.run(token)
