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


class DartbotHandles:

    async def change_channel(self, message):
        """Moves the bot to a different voice channel, given a message.
        Returns a string with the result.
        Only works if a voice_client for the server already exists"""
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

    async def join_channel(self, message):
        """Method that given a message, makes the bot join a join channel.
        Generates a voice_client for the server, and returns a string for the result.
        Only works if a voice_client does not already exist for the server."""
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
                            voice = await self.client.join_voice_channel(channels)
                            state = self.music.get_voice_state(message.server)
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
                    voice = await self.client.join_voice_channel(channels)
                    self.client.join_voice_channel(channels)
                    state = self.music.get_voice_state(message.server)
                    state.voice = voice
                    msg = 'Joined channel ' + voice.channel.name
        return msg

    def get_music(self):
        return self.music

    async def on_ready(self):
        """Prints to console when the bot is connected and ready."""
        print('Logged in as')
        print(self.client.user.name)
        print(self.client.user.id)
        print('------')

    async def on_message(self, message):
        """Whenever the client receives a message"""
        # print(message.content)
        # we do not want the bot to reply to itself
        if message.author == self.client.user:
            return

        if message.author.id == '213867524037672960':
            await self.client.send_file(message.author, 'D:\Pictures\santashh.jpg')

        if not message.content.startswith(self.prefix):
            pass
        elif message.content.startswith(self.prefix + 'help'):
            if len(message.content) > len(self.prefix + 'help'):
                found = False
                for command in self.command_list:
                    if message.content[len(self.prefix + 'help '):] == command.__name__:
                        try:
                            await self.client.send_message(message.channel, command.description)
                            found = True
                        except Exception as e:
                            await self.client.send_message(message.channel, 'No description found: ' + str(e))
                            found = True
                if not found:
                    await self.client.send_message(message.channel, 'There is no command by that name')
            else:
                cmd_dump = ''
                for cmd in self.command_list:
                    cmd_dump += cmd.__name__ + '\n'
                await self.client.send_message(message.channel, 'Command list:\n' + cmd_dump + 'Type ' + self.prefix + 'help [command] for help on a specific command')
        else:
            found = False
            for command in self.command_list:
                if message.content.startswith(self.prefix + command.__name__):
                    try:
                        await command.command(self, message)
                        found = True
                    except Exception as e:
                        await self.client.send_message(message.channel, 'Something went wrong: ' + str(e))
                        found = True
            if not found:
                await self.client.send_message(message.channel, 'There is no command by that name')

    def __init__(self, token):
        import os.path
        configs = open(os.path.dirname(__file__) + '/../command_list.txt', 'r')
        cmd_list = configs.readlines()
        _cmd_list = []
        print(str(cmd_list))
        for i in range(len(cmd_list)):
            if cmd_list[i].endswith("\n"):
                _cmd_list.append(cmd_list[i][:len(cmd_list[i])-1])
            else:
                _cmd_list.append(cmd_list[i])
        print(str(_cmd_list))
        self.command_list = []
        import importlib
        for cmd in _cmd_list:
            try:
                print('Importing ' + cmd)
                command = importlib.import_module('dart.' + cmd)
                command.__name__ = cmd
                self.command_list.append(command)
            except ModuleNotFoundError:
                print('Could not import ' + cmd)
        self.client = discord.Client()
        self.client.event(self.on_ready)
        self.client.event(self.on_message)
        self.music = Music(self.client)
        self.prefix = '!'  #Set this to w/e you want the command pre-fix to be
        self.owner = '144634215693156353'  #Discord user ID for who ever is running the bot
        #HomieRicky 142761888642629632
        #Dartrunner 144634215693156353
        #print(discord.version_info)
        self.client.run(token)
