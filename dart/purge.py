description = 'Deletes the last X messages, to a max of 100, by @mention, in the channel the command was issued in.'

async def command(dartbot, message):
    msg = 'Deletes the last X messages, to a max of 100, by @mention, in the channel the command was issued in.'
    count = 0
    target = None
    server = message.server
    channel = message.channel
    perms = message.author.permissions_in(channel)
    bot_perms = server.me.permissions_in(channel)
    if perms.manage_messages or message.author.id == dartbot.owner:
        if bot_perms.manage_messages:
            if len(message.content) > 7:
                if len(message.content) <= 10:
                    count = message.content[7:]
                    if int(count) <= 100:
                        await dartbot.client.purge_from(channel, limit=int(count))
                        msg = 'Removed ' + count + ' messages from ' + channel.name
                    else:
                        msg = 'This bot can only check up to 100 messages at a time.'
                elif len(message.content) > 10:
                    space2 = message.content.find(' ', 7)
                    count = message.content[7:space2]
                    if int(count) <= 100:
                        user = message.content[space2:]
                        user = user[3:-1]
                        target = server.get_member(user)
                        await dartbot.client.purge_from(channel, limit=int(count), check=lambda m: m.author == target)
                        msg = 'Checked the last ' + count + ' messages and removed all by' + target.name + ' from ' + channel.name
                    else:
                        msg = 'This bot can only check up to 100 messages at a time.'
        else:
            msg = 'I do not have message management permissions'
    else:
        msg = 'You do not have message management permissions in this channel.'

    await dartbot.client.send_message(message.channel, msg)