import requests

session = requests.Session()

login_page = session.get('https://xn--69aa8bzb.xn--y9a3aq/auth/sign_in').text

authenticity_token = login_page[login_page.find('name="authenticity_token" value="')+33: login_page.find('name="authenticity_token" value="')+33+88]

