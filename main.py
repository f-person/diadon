from mastodon import Mastodon
# from keys import *
import sys, os
import diaspy, json

given_args = sys.argv[1:]
args = ['-d', '--diaspora', '-m', '--mastodon', '-h', '--help', 'config', 'mastodon']
post = ''


for argnum, arg in enumerate(given_args):
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
        # else if len(post)<200 or arg == '-m' or arg == '--mastodon':
        elif len(post)<200 and arg != '-d' and arg != '--diaspora':
            api = Mastodon(m_keys.client_key, m_keys.client_secret, m_keys.access_token, m_keys.pod)
            # api.toot(post)
            print('successfully tooted on mastodon')
        else:
            api = diaspy.connection.Connection(pod = d_keys.pod, username=d_keys.username, password = d_keys.password)
            api.login()
            # diaspy.streams.Stream(api).post(post)
            print('successfully shared on diaspora')
        break