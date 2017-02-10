description = 'Deletes an emoji | Format: !emodelete [name]'

async def command(dartbot, message):
    msg = message.content
    result = 0
    if len(msg) > 11:
        name = msg[11:]
        emoji_list = dartbot.client.get_all_emojis()
        print(name)
        try:
            for emoji in emoji_list:
                if name == emoji.name:
                    print(str(emoji) + ' ' + str(emoji.server))
                    await dartbot.client.delete_custom_emoji(emoji)
                    result = 1
        except Exception as e:
            print(str(e))
            await dartbot.client.send_message(message.channel, 'Failed to delete emoji because: ' + str(e))
        if result == 1:
            await dartbot.client.send_message(message.channel,'Deleted emoji successfully')