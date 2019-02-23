from mastodon import Mastodon
from keys import *
import sys, os
import diaspy, json

given_args = sys.argv[1:]
args = ['-d', '--diaspora', '-m', '--mastodon', '-h', '--help', 'config', 'mastodon']
post = ''
str_post =''
for argnum, arg in enumerate(given_args):
    if arg not in args:
        post = ' '.join(given_args[argnum:])
        if len(post)==0:
            print("the post is empty")
        if len(post)<200:
            api = Mastodon(m_keys.client_key, m_keys.client_secret, m_keys.access_token, m_keys.pod)
            # api.toot(post)
            print('successfully tooted on mastodon')
        else:
            api = diaspy.connection.Connection(pod = d_keys.pod, username=d_keys.username, password = d_keys.password)
            api.login()
            # diaspy.streams.Stream(api).post(post)
            print('successfully shared on diaspora')
        break


# if '-d' in sys.argv:
#     if ()
#     print('shared on diaspora')
# else if '-m' in sys.argv:
#     print('shared on mastodon')


# api = Mastodon(m_keys.client_key, m_keys.client_secret, m_keys.access_token, api_base_url="https://xn--69aa8bzb.xn--y9a3aq")
# api.toot("")