# utils/oauth_utils.py
import os
import requests
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
from flask import current_app

class GoogleOAuth:
    def __init__(self):
        self.client_id = os.environ.get('GOOGLE_CLIENT_ID')
        self.client_secret = os.environ.get('GOOGLE_CLIENT_SECRET')
    
    def verify_token(self, token):
        try:
            idinfo = id_token.verify_oauth2_token(
                token, google_requests.Request(), self.client_id)
            return idinfo
        except Exception as e:
            return None
