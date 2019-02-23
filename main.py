from mastodon import Mastodon
# from keys import *
import sys, os
import diaspy, json

given_args = sys.argv[1:]
args = ['-d', '--diaspora', '-m', '--mastodon', '-h', '--help', 'config', 'mastodon']
post = ''

keys = json.load(open("keys.json", "r"))
mastodonMax = keys["mastodonMax"]

help_message = """USAGE: 
    just type diadon <your text here> to share it on diaspora if the length of the text is more than length for tooting on mastodon. by default it's set to 140.

    to override max length and share on diaspora add -d or --diaspora argument (diadon -d <your text here>)
    to override max lentgh and toot on mastodon add -m or --mastodon argument (diadon -m <your text here>)

FIRST TIME USE:
    first of all you need to create a new mastodon application in <your pod address>/settings/applications/new 
    then you have to configure mastodon and diaspora accounts

CONFIGURATIN:
    to change diaspora account settings type: diadon config <pod address> <username> <password>
    to change mastodon account settings type: diadon config <pod address> <client_secret> <access_token> <client_key> (if you dont have them get them by following 'FIRST TIME USE')
        """

for argnum, arg in enumerate(given_args):
    if arg == '-h' or arg == '--help':
        print(help_message)
        break

    if arg == 'config':
        if given_args[argnum+1] == '-m' or given_args[argnum+1]=='--mastodon':
            with open("keys.json", "r+") as jsonFile:
                data = json.load(jsonFile)
                try:
                    data["m_keys"]["pod"] = given_args[argnum+2]
                    data["m_keys"]["client_secret"] = given_args[argnum+3]
                    data["m_keys"]["access_token"] = given_args[argnum+4]
                    data["m_keys"]["client_key"] = given_args[argnum+5]
                except:
                    print("please enter all keys")
                    break
                jsonFile.seek(0)
                json.dump(data, jsonFile)
                jsonFile.truncate()
            break
        elif given_args[argnum+1] == '-d' or given_args[argnum+1]=='--diaspora':
            with open("keys.json", "r+") as jsonFile:
                data = json.load(jsonFile)
                try:
                    data["d_keys"]["pod"] = given_args[argnum+2]
                    data["d_keys"]["username"] = given_args[argnum+3]
                    data["d_keys"]["password"] = given_args[argnum+4]
                except:
                    print("please enter all keys")
                    break
                jsonFile.seek(0)
                json.dump(data, jsonFile)
                jsonFile.truncate()
            break
        else:
            printHelp()

    if arg not in args or arg =='-d' or arg == '--diaspora' or arg =='-m' or arg == '--mastodon':
        if arg not in args:
            post = ' '.join(given_args[argnum:])
        else:
            post = ' '.join(given_args[argnum+1:])
        if len(post)==0:
            print("the post is empty")
        elif len(post)<mastodonMax and arg != '-d' and arg != '--diaspora':
            api = Mastodon(keys["m_keys"]["client_key"], keys["m_keys"]["client_secret"], keys["m_keys"]["access_token"], keys["m_keys"]["pod"])
            # api.toot(post)
            print('successfully tooted on mastodon')
        else:
            api = diaspy.connection.Connection(pod = keys["d_keys"]["pod"], username=keys["d_keys"]["username"], password = keys["d_keys"]["password"])
            api.login()
            # diaspy.streams.Stream(api).post(post)
            print('successfully shared on diaspora')
        break
