#hello husky

from dart import handles

token = 'MjY3NTA1MDY2MzA5NzEzOTMw.C1QcmA.OVS6j0lFRkGEEyccz7G0rIygrEA' # discord bot app token

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Launch Dart-bot')
    parser.add_argument('-r', '--run', nargs=1, help='Run a new bot', required=False, metavar='[TOKEN]')
    parser.add_argument('-j', '--join_test', action='store_true', help='Join Test Server', required=False)

    args = vars(parser.parse_args())

    if args['run']:
        handles.DartbotHandles(args['run'][0])

    if args['join_test']:
        handles.DartbotHandles(token)
