__author__ = 'ipetrash'
# TODO: Приветствие зависит от времени выполнения скрипта

import argparse


def main(namespace):
    args = namespace.parse_args()

    if args.user is not None:
        print("Hello, %s!" % args.user)
    else:
        print("Hello, Py!")


def create_parser():
    parser = argparse.ArgumentParser(description='Hello World Example!')
    parser.add_argument('--user', type=str, help=' user name.')
    return parser

if __name__ == '__main__':
    namespace = create_parser()
    main(namespace)
