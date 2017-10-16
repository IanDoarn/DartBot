import discord
import asyncio
import youtube_dl

class Playlist:
    def __init__(self, voice, client):
        self.voice = voice
        self.playlist = asyncio.Queue(loop=client.loop)

class VoiceHandler:
    def __init__(self, client):
        self.client = client
        self._new_voice = asyncio.Event(loop=client.loop)
        self.voices = []
        self._voices = client.voice_clients
        self.voice_checker = asyncio.Task(self.handle_new_voice)
        try:
            self.client.event(self.on_new_voice)
        except asyncio.CancelledError as e:
            print(str(e))

    def add(self, url):
        self.playlist.put(url)

    @asyncio.coroutine
    def handle_new_voice(self):
        while len(self._voices) == len(self.client.voice_clients):
            if len(self._voices) > len(self.client.voice_clients):
                for v in self._voices:
                    if v not in self.client.voice_clients:
                        yield from self.on_new_voice(v, removed=True)
                        pass
            elif len(self._voices) < len(self.client.voice_clients):
                for v in self.client.voice_clients:
                    if v not in self._voices:
                        yield from self.on_new_voice(v)
                        pass

    @asyncio.coroutine
    def on_new_voice(self, voice, removed=False):
        if not removed:
            self.voices.append(Playlist(voice, self.client))
        else:
            for v in self.voices:
                if v.voice == voice:
                    self.voices.remove(v)




class DartbotHandles:
    def verify_user(self, message):
        if self.owner is not None:
            if message.author.id == self.owner:
                return True
            else:
                return False
        else:
            return True

    def check_command(self, message):
        if(message.content.startswith(self.prefix)):
            return True
        else:
            return False

    async def on_ready(self):
        print('We have logged in as {0.user}'.format(self.client))
        #self.playlist = VoiceHandler(self.client)

    async def on_message(self, message):
        if message.author == self.client.user:
            return

        if self.check_command(message):
            if self.verify_user(message):
                msg = message.content
                cmd = msg[len(self.prefix):msg.index(' ') if ' ' in msg else len(msg)]
                for command in self.command_list:
                    if cmd == command.__name__:
                        await command.command(self, message)
            else:
                dm_chan = await message.author.create_dm()
                await dm_chan.send('Failed to do command: `{0.content}`   Access denied'.format(message), delete_after=30.0)

    def __init__(self, token, ownerID=None):
        import logging

        logger = logging.getLogger('discord')
        logger.setLevel(logging.DEBUG)
        handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
        handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
        logger.addHandler(handler)


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
            except ImportError:
                print('Could not import ' + cmd)
        self.client = discord.Client()
        self.client.event(self.on_ready)
        self.client.event(self.on_message)
        self.prefix = 's!'  #Set this to w/e you want the command pre-fix to be
        self.owner = ownerID  #Discord user ID for who ever is running the bot
        self.downloader = youtube_dl.YoutubeDL({
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        })
        self.client.run(token)


