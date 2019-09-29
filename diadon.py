from sys import exit, argv
from os import path
import json

given_args = argv[1:]

args = ['-d', '--diaspora', '-m', '--mastodon', '-h', '--help', 'config', '-dm', '--diadon']

help_message = r"""     _   _               _                 
  __| | (_)   __ _    __| |   ___    _ __  
 / _` | | |  / _` |  / _` |  / _ \  | '_ \ 
| (_| | | | | (_| | | (_| | | (_) | | | | |
 \__,_| |_|  \__,_|  \__,_|  \___/  |_| |_|

USAGE:
    just type diadon '<your text here>' to share it on diaspora if the length of the text is more than length for tooting on mastodon. by default it's set to 140.

    to ignore max lentgh and toot on mastodon , use -m  or --mastodon argument (diadon -m  'your text here')
    to ignore max length and share on diaspora, use -d  or --diaspora argument (diadon -d  'your text here')
    to share on diaspora and toot on mastodon , use -dm or --diadon   argument (diadon -dm 'your text here')

FIRST TIME USE:
    create a new mastodon application in <your pod address>/settings/applications/new
    then configure mastodon and diaspora accounts

CONFIGURATIN:
    change max length               : '$ diadon config -max <max num> (can't be more than 500)'
    change diaspora account settings: '$ diadon config -d <pod address> <username> <password>'
    change mastodon account settings: '$ diadon config -m <pod address> <client_secret> <access_token> <client_key>'
        (if you dont have them, get as described in "FIRST TIME USE")"""

if len(given_args)==0:
    exit(help_message)

keys = json.load(open(path.expanduser("~") + "/.diadon/keys.json", "r"))
mastodonMax = int(keys["mastodonMax"])

imgFileNames = []

def shareOnDiaspora():
    from diaspy.connection import Connection
    from diaspy.streams import Stream

    api = Connection(pod = keys["d_keys"]["pod"], username=keys["d_keys"]["username"], password = keys["d_keys"]["password"])
    api.login()
    stream = Stream(api)
    diasporaMedia = []
    for filename in imgFileNames:
        diasporaMedia.append(stream._photoupload(filename=filename))
    stream.post(text=post, photos=diasporaMedia, provider_display_name="diadon")
    print('successfully shared on diaspora')

def tootOnMastodon():
    from mastodon import Mastodon

    api = Mastodon(keys["m_keys"]["client_key"], keys["m_keys"]["client_secret"], keys["m_keys"]["access_token"], keys["m_keys"]["pod"])
    mastodonMedia = []
    for filename in imgFileNames:
        with open(filename, "rb") as f:
            mastodonMedia.append(api.media_post(f.read(), "image/png"))
    api.status_post(post, media_ids = mastodonMedia)
    print('successfully tooted on mastodon')

for argnum, arg in enumerate(given_args):
    if arg == '-h' or arg == '--help':
        exit(help_message)

    if arg == 'config':
        if given_args[argnum+1] == '-m' or given_args[argnum+1]=='--mastodon':
            with open(path.expanduser("~") + "/.diadon/keys.json", "r+") as jsonFile:
                data = json.load(jsonFile)
                try:
                    if ('թութ․հայ') in given_args[argnum+2]:
                        given_args[argnum+2] = 'https://xn--69aa8bzb.xn--y9a3aq'
                    data["m_keys"]["pod"] = given_args[argnum+2]
                    data["m_keys"]["client_secret"] = given_args[argnum+3]
                    data["m_keys"]["access_token"] = given_args[argnum+4]
                    data["m_keys"]["client_key"] = given_args[argnum+5]
                except:
                    exit('please enter all keys')
                jsonFile.seek(0)
                json.dump(data, jsonFile)
                jsonFile.truncate()
            exit()
        elif given_args[argnum+1] == '-d' or given_args[argnum+1]=='--diaspora':
            with open(path.expanduser("~") + "/.diadon/keys.json", "r+") as jsonFile:
                data = json.load(jsonFile)
                try:
                    if "http://" not in given_args[argnum+2] or "https://" not in given_args[argnum+2]:
                        given_args[argnum+2] = "https://" + given_args[argnum+2]
                    data["d_keys"]["pod"] = given_args[argnum+2]
                    data["d_keys"]["username"] = given_args[argnum+3]
                    data["d_keys"]["password"] = given_args[argnum+4]
                except:
                    exit('please enter all keys')
                jsonFile.seek(0)
                json.dump(data, jsonFile)
                jsonFile.truncate()
            exit()
        elif given_args[argnum+1] == '-max':
            with open(path.expanduser("~") + "/.diadon/keys.json", "r+") as jsonFile:
                data = json.load(jsonFile)
                if int(given_args[argnum+2])>500:
                    exit("max length can't be more than 500")
                if not given_args[argnum+2]:
                    exit("please enter the max number")
                try:
                    data["mastodonMax"] = int(given_args[argnum+2])
                except:
                    exit("please enter an integer")
                jsonFile.seek(0)
                json.dump(data, jsonFile)
                jsonFile.truncate()
                exit()   
        else:
            exit(help_message)
    
    if arg not in args:
        post = arg
        for mediaArg in given_args[argnum+1:]:
            imgFileNames.append(mediaArg)
    if arg == '-dm' or arg=='--diadon' or arg == '-d' or arg=='--diaspora' or arg == '-m' or arg == '--mastodon':
        try:
            post = given_args[argnum+1]   
        except:
            exit('the post is empty')
        for mediaArg in given_args[argnum+2:]:
            try:
                imgFileNames.append(mediaArg)
            except:
                print("no media")
    if (len(post)<mastodonMax and arg != '-d' and arg != '--diaspora') or (arg == '-m' or arg =='--mastodon') or arg =='-dm' or arg=='--diadon':

        if (len(post)>500):
            shareOnDiasp = '1'
            while shareOnDiasp[0].lower() != 'y' and shareOnDiasp[0].lower() != 'n':
                shareOnDiasp = input("the length of a toot can't be more than 500 symbols. share the post on diaspora? [y,n] ")
            if shareOnDiasp[0].lower() == 'n':
                exit()
            else:
                shareOnDiaspora()
                exit()
        tootOnMastodon()
        if arg=='-dm' or arg=='--diadon':
            shareOnDiaspora()
            exit()
        exit()
    else:
        shareOnDiaspora()
        exit()
