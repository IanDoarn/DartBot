import discord

_client = discord.Client()

class Handles(object):

    def __init__(self, client):
        _client = client

        self.server = None
        self.client = client

    async def join_channel(self, message):
        self.server = message.server
        bot = self.server.me
        # print(server.channels)
        print(message.content)
        msg = 'joinVoice'
        if len(message.content) > 10:
            channelName = message.content[11:]
            for channels in self.server.channels:
                perms = channels.permissions_for(bot)
                if channels.name == channelName:
                    if channels.type.name == 'voice':
                        if str(perms.value)[2] == '4':
                            voice = await self.client.join_voice_channel(channels)
                            msg = 'Joining channel ' + voice.channel.name
                            break
                        else:
                            msg = 'DartBot is not allowed in ' + channels.name + '. Please check the channel permissions.'
                            break
                    else:
                        msg = "Given Channel is not a voice channel."
                        break
                msg = "Channel does not exist"

        else:
            for channels in self.server.channels:
                #print(channels)
                perms = channels.permissions_for(bot)
                if channels.type.name == 'voice' and str(perms.value)[2] == '4':
                    voice = await self.client.join_voice_channel(channels)
                    self.client.join_voice_channel(channels)
                    msg = 'Joined channel ' + voice.channel.name
        return msg

    async def change_channel(self, message):
        server = message.server
        voice = server.voice_self.client
        bot = server.me
        # print(server.channels)
        print(message.content)
        msg = 'joinVoice'
        if len(message.content) > 10:
            channelName = message.content[11:]
            for channels in server.channels:
                perms = channels.permissions_for(bot)
                if channels.name == channelName:
                    if channels.type.name == 'voice':
                        if str(perms.value)[2] == '4':
                            await voice.move_to(channels)
                            msg = 'Joining channel ' + voice.channel.name
                            break
                        else:
                            msg = 'DartBot is not allowed in ' + channels.name + '. Please check the channel permissions.'
                            break
                    else:
                        msg = "Given Channel is not a voice channel."
                        break
                msg = "Channel does not exist"

        else:
            for channels in server.channels:
                #print(channels)
                perms = channels.permissions_for(bot)
                if channels.type.name == 'voice' and str(perms.value)[2] == '4':
                    await voice.move_to(channels)
                    msg = 'Joined channel ' + voice.channel.name
        return msg



    @_client.event
    async def on_ready():
        print('Logged in as')
        print(_client.user.name)
        print(_client.client.user.id)
        print('------')

    @_client.event
    async def on_message(self, message):
        # we do not want the bot to reply to itself
        if message.author == self.client.user:
            return

        if message.content.startswith('!hello'):
            print(message.content)
            msg = 'Hello {0.author.mention}'
            await self.client.send_message(message.channel, msg)

        if message.content.startswith('!help'):
            print(message.content)
            msg = 'I need an adult!'
            await self.client.send_message(message.channel, msg)

        if message.content.startswith('tot'):
            print(message.content)
            msg = 'gay'
            await self.client.send_message(message.channel, msg)

        if message.content.startswith('!joinVoice'):
            server = message.server
            msg = 'voice channel'
            try:
                if server.voice_self.client.is_connected:
                    print('changing channel')
                    msg = await self.change_channel(message)
            except:
                print('joining new channel')
                msg = await self.join_channel(message)

            await self.client.send_message(message.channel, msg)

        if message.content.startswith('!leave'):
            server = message.server
            voice = self.client.voice_self.client_in(server)
            print(voice.channel.name)
            await voice.disconnect()
            print(self.client.is_voice_connected(server))
            msg = 'Disconnected from ' + voice.channel.name
            await self.client.send_message(message.channel, msg)

        '''if message.content.startswith('!test'):
            server = message.server
            msg = 'testing'
            print('perms testing')
            print(' ')
            bot = server.me
            for channels in server.channels:
                print(channels)
                perms = channels.permissions_for(bot)
                print(str(perms.value)[2])'''


def main(token):
    h = Handles(_client)
    _client.run(token)
