#!/usr/bin/python3
import argparse
import json
from getpass import getpass
from threading import Thread
from os import mkdir, path

from diaspy.connection import Connection
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
            scopes=['write'],
            website='https://github.com/f-person/diadon')
    api = Mastodon(client_id,
                   client_secret,
                   api_base_url=instance_url)

    email = input("Email: ")
    password = getpass()

    access_token = api.log_in(email, password, scopes=['write'])

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


def share_on_diaspora(configs: dict, post_text: str, image_filenames: [str]):
    api = Connection(pod=configs['diaspora']['pod_url'],
                     username=configs['diaspora']['username'],
                     password=configs['diaspora']['password'])
    api.login()

    stream = Stream(api)

    post_media = []
    for filename in image_filenames:
        post_media.append(stream._photoupload(filename))

    stream.post(text=post_text,
                photos=post_media,
                provider_display_name='diadon')

    print("shared on diaspora*")


def toot_on_mastodon(configs: dict, post_text: str, image_filenames: [str]):
    api = Mastodon(configs['mastodon']['client_id'],
                   configs['mastodon']['client_secret'],
                   configs['mastodon']['access_token'],
                   configs['mastodon']['instance_url'])

    post_media = []
    for filename in image_filenames:
        with open(filename, 'rb') as f:
            post_media.append(api.media_post(f.read(), 'image/png'))

    api.status_post(post_text, media_ids=post_media)

    print("tooted on Mastodon")


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
                       help="Share on diaspra and Toot on Mastodon")

    parser.add_argument('post_text', nargs='?', default='',
                        help="The body of post to share")
    parser.add_argument('-i', '--images', nargs='*', default=[],
                        help="Media to post (Not more than 4 for Mastodon)")

    args = parser.parse_args()

    if args.diadon:
        configs = read_configurations()
        Thread(target=share_on_diaspora,
               args=(configs, args.post_text, args.images,)).start()
        toot_on_mastodon(configs, args.post_text, args.images)
    elif args.diaspora:
        share_on_diaspora(read_configurations(), args.post_text, args.images)
    elif args.mastodon:
        toot_on_mastodon(read_configurations(), args.post_text, args.images)
    elif args.config == 'dm':
        diaspora_configs = get_diaspora_configs()
        mastodon_configs = get_mastodon_configs()
        write_configurations({'diaspra': diaspora_configs,
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
            toot_on_mastodon(configs, args.post_text, args.images)
        else:
            share_on_diaspora(configs, args.post_text, args.images)
