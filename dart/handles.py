import discord
import asyncio


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
            #try:
            print('Importing ' + cmd)
            command = importlib.import_module('dart.' + cmd)
            command.__name__ = cmd
            self.command_list.append(command)
            #except ModuleNotFoundError:
                #print('Could not import ' + cmd)
        self.client = discord.Client()
        self.client.event(self.on_ready)
        self.client.event(self.on_message)
        self.prefix = 's!'  #Set this to w/e you want the command pre-fix to be
        self.owner = ownerID  #Discord user ID for who ever is running the bot
        self.client.run(token)


