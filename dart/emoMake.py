description = 'Makes custom emoji with web URL | Format: !emomake [URL] [name]'
import discord

async def command(dartbot, message):
    msg = message.content
    if len(msg) > 9:
        try:
            separator = msg.find(' ', 9)
            URL = msg[9:separator]
            emoji_name = msg[separator+1:]
            from PIL import Image
            import urllib.request
            import io
            #img_bytes = io.BytesIO(urllib.request.urlopen(URL).read())
            img_bytes = urllib.request.urlopen(URL).read()
            await dartbot.client.create_custom_emoji(message.server, name=emoji_name, image=img_bytes)
        except (discord.HTTPException or discord.Forbidden) as e:
            await dartbot.client.send_message(message.channel, 'Failed to make emoji because: ' + str(e))