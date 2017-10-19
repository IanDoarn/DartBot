import dart.handles as h
description = 'Adds song or playlist to the queue and starts playing them immediately'

async def command(dartbot, message):
    server_voice = None
    for voice in dartbot.client.voice_clients:
        if voice.guild == message.author.guild:
            server_voice = voice
    if server_voice is None:
        await message.channel.send('I am not connected to any voice chat, dummy!')
        return

    info_msg = await message.channel.send('Downloading track info. Please wait.')

    video_link = message.content[len(dartbot.prefix)+len('play '):]
    results = dartbot.downloader.extract_info(video_link, download=False)
    urllist = []
    meta = []
    if 'entries' in results:
        for entry in results['entries']:
            urllist.append(entry['url'])
            meta.append(entry)
    else:
        urllist.append(results['url'])
        meta.append(results)

    print(len(urllist))
    first = h.SongObject(urllist[0], voice_client=server_voice, metadata=meta[0])
    if len(urllist) > 1:
        prev = first
        for i in range(1, len(urllist)):
            buf = h.SongObject(urllist[i], voice_client=prev.voice_client, metadata=meta[i])
            prev.next = buf
            prev = buf

    first.play()
    info_msg.delete()
