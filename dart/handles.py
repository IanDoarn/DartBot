import discord

client = discord.Client()

def pm(destination, message):
    #function used to send pms to users
    return

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
                        voice = await client.join_voice_channel(channels)
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
                voice = await client.join_voice_channel(channels)
                client.join_voice_channel(channels)
                msg = 'Joined channel ' + voice.channel.name
    return msg

async def change_channel(message):
    server = message.server
    voice = server.voice_client
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



@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

@client.event
async def on_message(message):
    print(message.content)
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

    if message.content.startswith('!hello'):
        print(message.content)
        msg = 'Hello {0.author.mention}'.format(message)
        await client.send_message(message.channel, msg)

    if message.content.startswith('!help'):
        print(message.content)
        msg = 'I need an adult!'
        await client.send_message(message.channel, msg)

    if message.content.startswith('tot'):
        print(message.content)
        msg = 'gay'
        await client.send_message(message.channel, msg)

    if message.content.startswith('!joinVoice'):
        server = message.server
        try:
            if server.voice_client.is_connected:
                print('changing channel')
                msg = await change_channel(message)
        except:
            print('joining new channel')
            msg = await join_channel(message)

        await client.send_message(message.channel, msg)

    if message.content.startswith('!leave'):
        server = message.server
        voice = client.voice_client_in(server)
        print(voice.channel.name)
        await voice.disconnect()
        print(client.is_voice_connected(server))
        msg = 'Disconnected from ' + voice.channel.name
        await client.send_message(message.channel, msg)

    if message.content.startswith('!add'):
        msg = 'add song'
        server = message.server
        voice = client.voice_client_in(server)
        if message.content.find('you', 4) is not -1:
            player = await voice.create_ytdl_player(message.content[5:])
            msg = 'Added \"' + player.title + '\" to the play list.'
            player.start()
        elif message.content.find('clyp.it', 4) is not -1:
            print('http://a.clyp.it/' + message.content[21:] + '.mp3')
            player = voice.create_ffmpeg_player('http://a.clyp.it/' + message.content[21:] + '.mp3')
            msg = 'Added ' + '\"figuring out clyp.it api to get title goes here\"' + ' to the play list.'
            player.start()
        elif len(message.content) <= 5:
            msg = 'Please include a link to add to the playlist.'
        else:
            msg = 'Website not supported, contact the dev to see if it can be added.'
        await client.send_message(message.channel, msg)


    '''if message.content.startswith('!playclyp'):
        server = message.server
        voice = client.voice_client_in(server)
        player = voice.create_ffmpeg_player('https://api.clyp.it/ys0wcghh.mp3')
        player.start()'''

    if message.content.startswith('!disconnect'):
        print(message.content)
        await client.close()

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
    client.run(token)
