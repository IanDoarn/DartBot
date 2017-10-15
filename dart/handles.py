import discord
import asyncio


class DartbotHandles:
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
        #self.client.event(self.on_ready)
        #self.client.event(self.on_message)
        #self.music = Music(self.client)
        self.prefix = '!'  #Set this to w/e you want the command pre-fix to be
        self.owner = '142761888642629632'  #Discord user ID for who ever is running the bot
        #HomieRicky 142761888642629632
        #Dartrunner 144634215693156353
        print(discord.version_info)
        self.client.run(token)
