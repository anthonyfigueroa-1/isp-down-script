import requests
import os

def get_bearer():
    secret = os.environ["SECRET"]
    client = os.environ["CLIENT"]

    url = "https://app.ninjaone.com/ws/oauth/token"

    header = {
            "accept": "application/json",
            "Content-Type": "application/x-www-form-urlencoded"
            }

    payload = {
            "grant_type": "client_credentials",
            "client_id": client,
            "client_secret": secret,
            "scope": ["monitoring"]
            }

    response = requests.post(url, headers=header, data=payload)

    print(f"Ninja bearer token request response: {response.status_code}") 

    print(response.json())

    return response.json().get("access_token")
get_bearer()
