import argparse
import sys

from asyncrisk import app, app_env


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', dest='port', default='5000', help='Specify port -- usually for testing.')
    parser.add_argument('--host', dest='host', default='localhost', help='Specify host -- usually for testing.')

    args = parser.parse_args()

    if args.init:
        sys.exit(0)
    else:
        app.run(host=args.host, port=args.port, debug=app_env.debug)


if __name__ == '__main__':
    main()
