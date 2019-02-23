from mastodon import Mastodon
import keys

api = Mastodon(keys.client_key, keys.client_secret, keys.access_token, api_base_url="https://xn--69aa8bzb.xn--y9a3aq")
api.toot("python-ով թթելու փորձ")