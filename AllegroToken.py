import requests
import json
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

CLIENT_ID = "fb505c0573c24dd7a73f873e07bb2c53"          # wprowadź Client_ID aplikacji
CLIENT_SECRET = "XORZBRIqkZLwBf2VNlM8vdCsz85EyBnvkD6gv3jmuD6KuLnqfm0OMJVbhEnNGFfH"      # wprowadź Client_Secret aplikacji
REDIRECT_URI = "http://localhost:8000"       # wprowadź redirect_uri
AUTH_URL = "https://allegro.pl/auth/oauth/authorize"
TOKEN_URL = "https://allegro.pl/auth/oauth/token"


def get_authorization_code():
    authorization_redirect_url = AUTH_URL + '?response_type=code&client_id=' + CLIENT_ID + \
                                 '&redirect_uri=' + REDIRECT_URI
    print("Login to Allegro - use url in your browser and then enter authorization code from returned url: ")
    print("---  " + authorization_redirect_url + "  ---")
    authorization_code = input('code: ')
    return authorization_code


def get_refresh_token(authorization_code):
    try:
        data = {'grant_type': 'authorization_code', 'code': authorization_code, 'redirect_uri': REDIRECT_URI}
        access_token_response = requests.post(TOKEN_URL, data=data, verify=False,
                                              allow_redirects=False, auth=(CLIENT_ID, CLIENT_SECRET))
        tokens = json.loads(access_token_response.text)
        access_token = tokens['refresh_token']
        return access_token
    except requests.exceptions.HTTPError as err:
        raise SystemExit(err)


def get_next_token(token):
    try:
        data = {'grant_type': 'refresh_token', 'refresh_token': token, 'redirect_uri': REDIRECT_URI}
        access_token_response = requests.post(TOKEN_URL, data=data, verify=False,
                                              allow_redirects=False, auth=(CLIENT_ID, CLIENT_SECRET))
        tokens = json.loads(access_token_response.text)
        refresh_token = tokens['refresh_token']
        access_token = tokens['access_token']
        with open('access_tokens_allegro.txt', 'w') as f:
            f.write(refresh_token)
            f.write("\n")
            f.write(access_token)
            f.close
        return access_token
    except requests.exceptions.HTTPError as err:
        raise SystemExit(err)


def main():
    authorization_code = get_authorization_code()
    refresh_token = get_refresh_token(authorization_code)
    print("refresh token = " + refresh_token)
    next_token = get_next_token(refresh_token)
    print("next access token = " + next_token)


if __name__ == "__main__":
    main()