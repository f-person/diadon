# diadon
tool which chooses between tooting on mastodon and sharing on diaspora

USAGE: 
    just type diadon <your text here> to share it on diaspora if the length of the text is more than length for tooting on mastodon. by default it's set to 140.

    to override max length and share on diaspora add -d or --diaspora argument (diadon -d <your text here>)
    to override max lentgh and toot on mastodon add -m or --mastodon argument (diadon -m <your text here>)

FIRST TIME USE:
    first of all you need to create a new mastodon application in <your pod address>/settings/applications/new 
    then you have to configure mastodon and diaspora accounts

CONFIGURATIN:
    to change diaspora account settings type: diadon config <pod address> <username> <password>
    to change mastodon account settings type: diadon config <pod address> <client_secret> <access_token> <client_key> (if you dont have them get them by following 'FIRST TIME USE')