import discord
description = 'Plays the audio from the given link'

async def command(dartbot, message):
    server_voice = None
    for voice in dartbot.client.voice_clients:
        if voice.guild == message.author.guild:
            server_voice = voice
    if server_voice is None:
        await message.channel.send('I am not connected to any voice chat, dummy!')
        return

    video_link = message.content[len(dartbot.prefix)+len('play '):]
    results = dartbot.downloader.extract_info(video_link, download=False)
    urllist = []
    if 'entries' in results:
        for entry in results['entries']:
            urllist.append(entry['url'])
    else:
        urllist.append(results['url'])
    print(urllist)
    source = discord.FFmpegPCMAudio(urllist[0])
    server_voice.play(source)