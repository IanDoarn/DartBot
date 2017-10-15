#hello husky

from dart import handles

#REF: http://discordpy.readthedocs.io/en/rewrite/

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Launch Dart-bot')
    parser.add_argument('-r', '--run', nargs=1, help='Run a new bot', required=True, metavar='[BOT_TOKEN]')
    parser.add_argument('-t', '--test', nargs=1, help='(Requires -r first) Run a new bot with a specific user ID as the "Owner". Note: only the owner can use the bot commands', required=False, metavar='[OWNER_ID]')
    parser.add_argument('-v', '--version_info', action='store_true', help='Get version info', required=False)

    args = vars(parser.parse_args())

    if args['version_info']:
        import discord
        print(discord.version_info)

    if args['run']:
        if args['test']:
            print('Starting server with {0}'.format(args['test'][0]))
            handles.DartbotHandles(args['run'][0], int(args['test'][0]))
        else:
            handles.DartbotHandles(args['run'][0])

