import discord

_client = discord.Client()


async def join_channel(message):
    server = message.server
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
                        voice = await _client.join_voice_channel(channels)
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
                voice = await _client.join_voice_channel(channels)
                _client.join_voice_channel(channels)
                msg = 'Joined channel ' + voice.channel.name
    return msg

async def change_channel(message):
    server = message.server
    voice = server.voice__client
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
    print(_client.user.id)
    print('------')

@_client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == _client.user:
        return

    if message.content.startswith('!hello'):
        print(message.content)
        msg = 'Hello {0.author.mention}'
        await _client.send_message(message.channel, msg)

    if message.content.startswith('!help'):
        print(message.content)
        msg = 'I need an adult!'
        await _client.send_message(message.channel, msg)

    if message.content.startswith('tot'):
        print(message.content)
        msg = 'gay'
        await _client.send_message(message.channel, msg)

    if message.content.startswith('!joinVoice'):
        server = message.server
        try:
            if server.voice_client.is_connected:
                print('changing channel')
                msg = await change_channel(message)
        except:
            print('joining new channel')
            msg = await join_channel(message)

        await _client.send_message(message.channel, msg)

    if message.content.startswith('!leave'):
        server = message.server
        voice = _client.voice__client_in(server)
        print(voice.channel.name)
        await voice.disconnect()
        print(_client.is_voice_connected(server))
        msg = 'Disconnected from ' + voice.channel.name
        await _client.send_message(message.channel, msg)

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
    _client.run(token)
