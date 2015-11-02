#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import click

# @click.group()
# def greet (): pass
#
# @greet.command ()
# def hello ( ** kwargs ): pass
#
# @greet.command ()
# def goodbye ( ** kwargs ): pass
#
# if __name__ == '__main__':
#     greet ()

# @click.command()
# @click.argument('filename', required=False)
# def touch(filename):
#     click.echo('filename=' + str(filename))
# touch()

# @click.command()
# @click.argument('src', nargs=-1)
# @click.argument('dst', nargs=1)
# def copy(src, dst):
#     for fn in src:
#         click.echo('move %s to folder %s' % (fn, dst))
#
# if __name__ == '__main__':
#     copy()


# @click.command()
# @click.argument('input', type=click.File('rb'))
# @click.argument('output', type=click.File('wb'))
# def inout(input, output):
#     while True:
#         chunk = input.read(1024)
#         if not chunk:
#             break
#         output.write(chunk)
#
# inout()

#
# @click.command()
# @click.argument('f', type=click.Path(exists=True))
# def touch(f):
#     click.echo(click.format_filename(f))
#
# touch()

# import os
# for k, v in os.environ.items():
#     print(k + ': ')
#     for i, val in enumerate(v.split(';'), 1):
#         print('    {}. {}'.format(i, val))
# quit()

# @click.command()
# @click.argument('src', envvar='SRC', type=click.File('r'))
# def echo(src):
#     click.echo(src.read())

# @click.command()
# @click.argument('files', nargs=1, type=int)
# def touch(files):
#     print(type(files))
#     click.echo(files)


# @click.command()
# @click.option('--value', type=[str, int])
# def touch(value):
#     print(value)
#     click.echo('%s=%s' % value)


# @click.command()
# @click.option('--message', '-m', multiple=True)
# def touch(message):
#     print(type(message), message)
#     click.echo('\n'.join(message))


# @click.command()
# @click.option('-m', '--message')
# def touch(message):
#     print(type(message), message)
#     click.echo('\n'.join(message))

# @click.command()
# @click.option('-v', '--verbose', count=True)
# def touch(verbose):
#     click.echo('Verbosity: %s' % verbose)

# @click.command()
# @click.option('-shoot/-no-shoot')
# @click.option('-flag', is_flag=True)
# @click.option('/debug;/no-debug')
# def touch(shoot, flag, debug):
#     click.echo('Verbosity: %s %s %s' % (shoot, flag, debug))


# import sys
#
# @click.command()
# @click.option('--upper', 'case', flag_value='upper', default=True)
# @click.option('--lower', 'case', flag_value='lower')
# def touch(case):
#     print(case)
#     click.echo(getattr(sys.platform, case)())
#
# touch()


# @click.command()
# @click.option('--hash-type', '-hash', type=click.Choice(['md5', 'sha1']))
# def digest(hash_type):
#     click.echo(hash_type)
#
# digest()

# @click.command()
# @click.option('--name', prompt=True)
# @click.option('--name2', prompt='Your name please')
# def hello(name, name2):
#     click.echo('Hello %s-%s!' % (name, name2))
#
# hello()


# @click.command()
# @click.option('--login', prompt='Your login please')
# @click.option('--password', prompt=True, hide_input=True, confirmation_prompt=True)
# # @click.password_option()
# def encrypt(password, login):
#     import codecs
#     click.echo('Encrypting password to %s %s' % (codecs.encode(password, 'ROT13'), login))
#
# encrypt()


# import os
#
#
# @click.command()
# # @click.option('--username', prompt=True, default=lambda: os.environ.get('JAVA_HOME', ''))
# @click.option('--username', prompt=True, default=lambda: 1)
# @click.option('--username', prompt=True, default=lambda: [1, 2, 3])
# def hello(username):
#     print("Hello,", username)
#
# hello()


# def print_version(ctx, param, value):
#     if not value or ctx.resilient_parsing:
#         return
#     click.echo('Version 1.0')
#     ctx.exit()
#
# @click.command()
# @click.option('--version', is_flag=True, callback=print_version, expose_value=False, is_eager=True)
# def hello():
#     click.echo('Hello World!')
#
# hello()


# def abort_if_false(ctx, param, value):
#     if not value:
#         ctx.abort()
#
# @click.command()
# @click.option('--yes', is_flag=True, callback=abort_if_false,
#               expose_value=False,
#               prompt='Are you sure you want to drop the db?')
# def dropdb():
#     click.echo('Dropped all tables!')


# @click.command()
# @click.confirmation_option(help='Are you sure you want to drop the db?')
# def dropdb():
#     click.echo('Dropped all tables!')
#
# dropdb()

