from datetime import datetime, timezone

import requests
import json

class BskyClient():
    def __init__(self, bsky_handle, bsky_app_password):
        self.bsky_handle = bsky_handle
        self.bsky_app_password = bsky_app_password

    def create_session(self):
        url = 'https://bsky.social/xrpc/com.atproto.server.createSession'

        payload = json.dumps({
            "identifier": self.bsky_handle,
            "password": self.bsky_app_password
        })
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        response.raise_for_status()

        self.session = response.json()

    def send_post(self, post):
        url = f'{self.session['didDoc']['service'][0]['serviceEndpoint']}/xrpc/com.atproto.repo.createRecord'

        payload = json.dumps({
            "repo": self.session['handle'],
            "collection": "app.bsky.feed.post",
            "record": {
                "$type": "app.bsky.feed.post",
                "text": post,
                "createdAt": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
            }
        })
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': f'Bearer {self.session['accessJwt']}'
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        response.raise_for_status()