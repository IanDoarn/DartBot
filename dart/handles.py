import discord
import threading
import youtube_dl
import time


class SongObject(discord.FFmpegPCMAudio):
    def __init__(self, source, voice_client=None, metadata=None, next=None):
        super().__init__(source)
        self.metadata = metadata
        self.next = next
        self.voice_client = voice_client
        self.t = threading.Thread(target=self.check_playing_thread)

    def play(self):
        if self.voice_client is None:
            raise TypeError
        else:
            try:
                self.voice_client.play(self)
                self.t.start()
            except discord.ClientException as e:
                print(str(e))


    def check_playing_thread(self):
        while self.voice_client.is_playing() or self.voice_client.is_paused():
            time.sleep(1)
        if self.next is not None:
            self.get_next().play()

    def get_last(self):
        if self.next is None:
            return self
        else:
            return self.get_last()

    def get_next(self):
        return self.next

    def get_playlist(self, recursive=[]):
        recursive.append(self)
        if self.next is None:
            return recursive
        else:
            return self.next.get_playlist(recursive)

    def remove_future(self):
        self.next=None



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
        try:
            import logging
            logger = logging.getLogger('discord')
            logger.setLevel(logging.DEBUG)
            handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
            handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
            logger.addHandler(handler)
        except PermissionError as e:
            print('Could not start logger: ' + str(e))

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

