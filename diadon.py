#!/usr/bin/python3
import json
from getpass import getpass
from os import mkdir, path
from sys import argv, exit

from diaspy.connection import Connection
from diaspy.streams import Stream
from mastodon import Mastodon

given_args = argv[1:]

args = ['-d', '--diaspora',
        '-m', '--mastodon',
        '-dm', '--diadon'
        '-h', '--help',
        'config']

help_message = r"""     _   _               _
  __| | (_)   __ _    __| |
 / _` | | |  / _` |  / _` |  / _ \  | '_ \
| (_| | | | | (_| | | (_| | | (_) | | | | |
 \__,_| |_|  \__,_|  \__,_|  \___/  |_| |_|

USAGE:
    just type diadon '<your text here>' to share it on diaspora
    if the length of the text is more than length for tooting on mastodon.
    by default it's set to 140.

    to ignore max lentgh and toot on mastodon , use -m  or --mastodon argument:
        $ diadon -m  'your text here'
    to ignore max length and share on diaspora, use -d  or --diaspora argument:
        $ diadon -d  'your text here'
    to share on diaspora and toot on mastodon , use -dm or --diadon   argument:
        $ diadon -dm 'your text here'

FIRST TIME USE:
    just put diadon.py as diadon somewhere in your path
    and run the setup command:
        $ diadon setup

CONFIGURATIN:
    change max length               :
        $ diadon config -max <max num> (can't be more than 500)
    change diaspora account settings:
        $ diadon config -d <pod> <username> <password>
    change mastodon account settings:
        $ diadon config -m <pod> <client_secret> <access_token> <client_key>
        (if you dont have them, get as described in "FIRST TIME USE")"""

if len(given_args) == 0:
    exit(help_message)

if given_args[0] == 'setup':
    configuration = {}

    mastodon_base_url = input('Enter your Mastodon instance url'
                              '(just press enter to not configure mastodon): ')
    if mastodon_base_url != '':
        (client_id, client_secret) = Mastodon.create_app(
                'diadon',
                scopes=['write'],
                api_base_url=mastodon_base_url,
                website='https://github.com/f-person/diadon')
        api = Mastodon(
                client_id,
                client_secret,
                api_base_url=mastodon_base_url)

        username = input('Email: ')
        password = getpass()
        access_token = api.log_in(username, password, scopes=['write'])

        configuration['m_keys'] = {
            'pod': mastodon_base_url,
            'client_key': client_id,
            'client_secret': client_secret,
            'access_token': access_token,
        }

    diaspora_base_url = input('Enter your diaspora pod url'
                              '(just press enter to not configure diaspora): ')
    if diaspora_base_url != '':
        username = input('Username: ')
        password = getpass()

        configuration['d_keys'] = {
            'pod': diaspora_base_url,
            'username': username,
            'password': password,
        }

    if path.isdir(path.expanduser('~') + '/.diadon'):
        if path.isfile(path.expanduser('~') + '/.diadon/keys.json'):
            with open(path.expanduser('~') +
                      '/.diadon/keys.json', 'r+') as json_file:
                data = json.load(json_file)

                for key in configuration.keys():
                    data[key] = configuration[key]

                json_file.seek(0)
                json.dump(data, json_file, indent=2)
                json_file.truncate()
        else:
            with open(path.expanduser('~') +
                      '/.diadon/keys.json', 'w') as json_file:
                configuration['mastodonMax'] = 140
                json_file.write(json.dumps(configuration, indent=2))
    else:
        mkdir(path.expanduser('~') + '/.diadon')
        with open(path.expanduser('~') +
                  '/.diadon/keys.json', 'w') as json_file:
            configuration['mastodonMax'] = 140
            json_file.write(json.dumps(configuration, indent=2))

    exit()

keys = json.load(open(path.expanduser('~') + '/.diadon/keys.json', 'r'))
mastodon_max = int(keys['mastodonMax'])

images = []


def share_on_diaspora():
    api = Connection(pod=keys['d_keys']['pod'],
                     username=keys['d_keys']['username'],
                     password=keys['d_keys']['password'])
    api.login()
    stream = Stream(api)
    diasporaMedia = []
    for filename in images:
        diasporaMedia.append(stream._photoupload(filename=filename))
    stream.post(text=post,
                photos=diasporaMedia,
                provider_display_name="diadon")
    print('successfully shared on diaspora')


def toot_on_mastodon():
    api = Mastodon(keys['m_keys']['client_key'],
                   keys['m_keys']['client_secret'],
                   keys['m_keys']['access_token'],
                   keys['m_keys']['pod'])
    mastodonMedia = []
    for filename in images:
        with open(filename, 'rb') as f:
            mastodonMedia.append(api.media_post(f.read(), 'image/png'))
    api.status_post(post, media_ids=mastodonMedia)
    print("successfully tooted on mastodon")


for argnum, arg in enumerate(given_args):
    if arg == '-h' or arg == '--help':
        exit(help_message)

    if arg == 'config':
        if (given_args[argnum+1] == '-m' or
                given_args[argnum+1] == '--mastodon'):
            with open(path.expanduser('~') +
                      '/.diadon/keys.json', 'r+') as json_file:
                data = json.load(json_file)
                try:
                    if ('թութ․հայ') in given_args[argnum+2]:
                        given_args[argnum+2] = \
                                'https://xn--69aa8bzb.xn--y9a3aq'
                    data['m_keys']['pod'] = given_args[argnum+2]
                    data['m_keys']['client_secret'] = given_args[argnum+3]
                    data['m_keys']['access_token'] = given_args[argnum+4]
                    data['m_keys']['client_key'] = given_args[argnum+5]
                except BaseException:
                    exit('please enter all keys')
                json_file.seek(0)
                json.dump(data, json_file, indent=2)
                json_file.truncate()
            exit()
        elif (given_args[argnum+1] == '-d' or
                given_args[argnum+1] == '--diaspora'):
            with open(path.expanduser('~') +
                      "/.diadon/keys.json", "r+") as json_file:
                data = json.load(json_file)
                try:
                    if ('http://' not in given_args[argnum+2] or
                            'https://' not in given_args[argnum+2]):
                        given_args[argnum+2] = "https://"
                        + given_args[argnum+2]
                    data['d_keys']['pod'] = given_args[argnum+2]
                    data['d_keys']['username'] = given_args[argnum+3]
                    data['d_keys']['password'] = given_args[argnum+4]
                except BaseException:
                    exit("please enter all keys")
                json_file.seek(0)
                json.dump(data, json_file, indent=2)
                json_file.truncate()
            exit()
        elif given_args[argnum+1] == '-max':
            with open(path.expanduser('~') +
                      "/.diadon/keys.json", "r+") as json_file:
                data = json.load(json_file)
                if int(given_args[argnum+2]) > 500:
                    exit("max length can't be more than 500")
                if not given_args[argnum+2]:
                    exit("please enter the max number")
                try:
                    data['mastodonMax'] = int(given_args[argnum+2])
                except BaseException:
                    exit("please enter an integer")
                json_file.seek(0)
                json.dump(data, json_file, indent=2)
                json_file.truncate()
                exit()
        else:
            exit(help_message)

    if arg not in args:
        post = arg
        for mediaArg in given_args[argnum+1:]:
            images.append(mediaArg)
    if (arg == '-dm' or arg == '--diadon' or
            arg == '-d' or arg == '--diaspora' or
            arg == '-m' or arg == '--mastodon'):
        try:
            post = given_args[argnum+1]
        except BaseException:
            exit("the post is empty")
        for mediaArg in given_args[argnum+2:]:
            try:
                images.append(mediaArg)
            except BaseException:
                print("no media")

    if ((len(post) < mastodon_max and arg != '-d' and arg != '--diaspora') or
            (arg == '-m' or arg == '--mastodon') or
            (arg == '-dm' or arg == '--diadon')):
        if (len(post) > 500):
            should_share_on_diaspora = '1'
            while (should_share_on_diaspora[0].lower() != 'y' and
                    should_share_on_diaspora[0].lower() != 'n'):
                input_prompt = ("the length of a toot can't be more than"
                                "500 symbols. share the post on diaspora?"
                                "[y,n] ")
                should_share_on_diaspora = input()
            if should_share_on_diaspora[0].lower() == 'n':
                exit()
            else:
                share_on_diaspora()
                exit()
        toot_on_mastodon()
        if arg == '-dm' or arg == '--diadon':
            share_on_diaspora()
            exit()
        exit()
    else:
        share_on_diaspora()
        exit()
