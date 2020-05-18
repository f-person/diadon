#!/usr/bin/python3
import argparse
import json
from getpass import getpass
from threading import Thread
from os import mkdir, path

from diaspy.connection import Connection
from diaspy.people import User
from diaspy.models import Post
from diaspy.streams import Stream
from mastodon import Mastodon


def get_diaspora_configs() -> dict:
    pod_url = input("diaspora* pod url: ")
    username = input("Username: ")
    password = getpass()

    return {
        'pod_url': pod_url,
        'username': username,
        'password': password
    }


def get_mastodon_configs() -> dict:
    instance_url = input("Mastodon instance url: ")
    (client_id, client_secret) = Mastodon.create_app(
            'diadon',
            api_base_url=instance_url,
            scopes=['read', 'write'],
            website='https://github.com/f-person/diadon')
    api = Mastodon(client_id,
                   client_secret,
                   api_base_url=instance_url)

    email = input("Email: ")
    password = getpass()

    access_token = api.log_in(email, password, scopes=['read', 'write'])

    return {
        'instance_url': instance_url,
        'client_id': client_id,
        'client_secret': client_secret,
        'access_token': access_token
    }


def get_mastodon_max_config() -> int:
    mastodon_max = int(input("Mastodon max: "))

    while mastodon_max > 500:
        print("Mastodon max cannot be higher than 500")
        mastodon_max = int(input("Mastodon max: "))

    return mastodon_max


def write_configurations(new_configs: dict):
    config_dir_path = path.join(path.expanduser('~'), '.config/diadon')
    config_file_path = path.join(config_dir_path, 'keys.json')

    if path.isdir(config_dir_path):
        if path.isfile(config_file_path):
            with open(config_file_path, 'r+') as configs_file:
                configs = json.load(configs_file)

                for key in new_configs.keys():
                    configs[key] = new_configs[key]

                configs_file.seek(0)
                json.dump(configs, configs_file, indent=4)
                configs_file.truncate()
        else:
            with open(config_file_path, 'w') as configs_file:
                configs_file.write(json.dumps(new_configs, indent=4))
    else:
        mkdir(config_dir_path)
        with open(config_file_path, 'w') as configs_file:
            configs_file.write(json.dumps(new_configs, indent=4))


def read_configurations() -> dict:
    config_dir_path = path.join(path.expanduser('~'), '.config/diadon')
    config_file_path = path.join(config_dir_path, 'keys.json')

    with open(config_file_path, 'r') as configs_file:
        configs = json.load(configs_file)
        return configs


def shorten_text(text: str) -> str:
    return text[:140] + '...' if len(text) > 140 else text[:140]


def share_on_diaspora(configs: dict, post_text: str, image_filenames: [str],
                      reply_to_latest_post: bool = False):
    api = Connection(pod=configs['diaspora']['pod_url'],
                     username=configs['diaspora']['username'],
                     password=configs['diaspora']['password'])
    api.login()

    success_message = "shared on diaspora*"

    if reply_to_latest_post:
        handle = '%s@%s' % (configs['diaspora']['username'],
                            configs['diaspora']['pod_url'].split('://')[1])
        user = User(api, handle=handle)

        latest_post = Post(api, user.stream[0].id, fetch=False, comments=False)
        latest_post.comment(post_text)

        success_message = "replied to %s" % shorten_text(str(user.stream[0]))
    else:
        stream = Stream(api)

        post_media = []
        for filename in image_filenames:
            post_media.append(stream._photoupload(filename))

        stream.post(text=post_text,
                    photos=post_media,
                    provider_display_name='diadon')

    print(success_message)


def toot_on_mastodon(configs: dict, post_text: str, image_filenames: [str],
                     reply_to_latest_post: bool = False):
    api = Mastodon(configs['mastodon']['client_id'],
                   configs['mastodon']['client_secret'],
                   configs['mastodon']['access_token'],
                   configs['mastodon']['instance_url'])

    post_media = []
    for filename in image_filenames:
        with open(filename, 'rb') as f:
            post_media.append(api.media_post(f.read(), 'image/png'))

    latest_status_id = None
    success_message = "tooted on Mastodon"

    if reply_to_latest_post:
        account_id = api.account_verify_credentials()['id']
        latest_status = api.account_statuses(account_id, limit=1)[0]
        latest_status_id = latest_status['id']

        success_message = ("replied to %s" %
                           shorten_text(latest_status['content']))

    api.status_post(post_text, in_reply_to_id=latest_status_id,
                    media_ids=post_media)

    print(success_message)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
            description="diadon is a tool for posting on diaspora/mastodon.")

    group = parser.add_mutually_exclusive_group()
    group.add_argument('--config', action='store',
                       const='dm', default=None, nargs='?',
                       help="Configure diadon")
    group.add_argument('-d', '--diaspora', action='store_true',
                       help="Share on diaspora*")
    group.add_argument('-m', '--mastodon', action='store_true',
                       help="Toot on Mastodon")
    group.add_argument('-dm', '--diadon', action='store_true',
                       help="Share on diaspora and Toot on Mastodon")

    parser.add_argument('-r', '--reply', action='store_true',
                        help="Reply to the latest toot/post")
    parser.add_argument('post_text', nargs='?', default='',
                        help="The body of post to share")
    parser.add_argument('-i', '--images', nargs='*', default=[],
                        help="Media to post (Not more than 4 for Mastodon)")

    args = parser.parse_args()

    if args.diadon:
        configs = read_configurations()
        Thread(target=share_on_diaspora,
               args=(configs, args.post_text, args.images,
                     args.reply,)).start()
        toot_on_mastodon(configs, args.post_text, args.images, args.reply)
    elif args.diaspora:
        share_on_diaspora(read_configurations(), args.post_text, args.images,
                          args.reply)
    elif args.mastodon:
        toot_on_mastodon(read_configurations(), args.post_text, args.images,
                         args.reply)
    elif args.config == 'dm':
        diaspora_configs = get_diaspora_configs()
        mastodon_configs = get_mastodon_configs()
        write_configurations({'diaspora': diaspora_configs,
                              'mastodon': mastodon_configs})
    elif args.config == 'd' or args.config == 'diaspora':
        diaspora_configs = get_diaspora_configs()
        write_configurations({'diaspora': diaspora_configs})
    elif args.config == 'm' or args.config == 'mastodon':
        mastodon_configs = get_mastodon_configs()
        write_configurations({'mastodon': mastodon_configs})
    elif args.config == 'mm' or args.config == 'mastodon_max':
        mastodon_max = get_mastodon_max_config()
        write_configurations({'mastodon_max': mastodon_max})
    else:
        configs = read_configurations()
        if 'mastodon_max' not in configs.keys():
            mastodon_max = 140
        else:
            mastodon_max = configs['mastodon_max']

        if mastodon_max > len(args.post_text):
            toot_on_mastodon(configs, args.post_text, args.images, args.reply)
        else:
            share_on_diaspora(configs, args.post_text, args.images, args.reply)
