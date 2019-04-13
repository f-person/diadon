# diadon
diadon is a tool for posting on diaspora/mastodon.

INSTALLATION:

    $ git clone https://github.com/f-person/diadon.git
    $ cd diadon
    $ python3 setup.py

USAGE:

    just type diadon '<your text here>' to share it on diaspora 
        if the length of the text is more than length for tooting on mastodon.
        by default it's set to 140.

    to ignore max lentgh and toot on mastodon ,  use -m  or --mastodon argument (diadon -m  'your text here')
    to ignore max length and share on diaspora,  use -d  or --diaspora argument (diadon -d  'your text here')
    to share on diaspora and toot on mastodon ,  use -dm or --diadon   argument (diadon -dm 'your text here')
    to post images use this pattern: '$ diadon [arg] 'post text' /full/path/to/image1 [/full/path/to/image2]'
        [] - optional

FIRST TIME USE:

    create a new mastodon application in <your pod address>/settings/applications/new
    then configure mastodon and diaspora accounts

CONFIGURATIN:

    change max length               : '$ diadon config -max <max num> (can't be more than 500)'
    change diaspora account settings: '$ diadon config -d <pod address> <username> <password>'
    change mastodon account settings: '$ diadon config -m <pod address> <client_secret> <access_token> <client_key>'
        (if you dont have them, get as described in "FIRST TIME USE")
