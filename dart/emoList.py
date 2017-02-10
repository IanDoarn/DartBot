description = 'Lists all emojis in the console'

async def command(dartbot, message):
    emojis = dartbot.client.get_all_emojis()
    for emoji in emojis:
        print(emoji.name)