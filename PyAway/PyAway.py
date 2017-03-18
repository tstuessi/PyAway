'''
PyAway: A Python Wrapper for the HomeAway API

Feel free to implement your own OAuth system and way of dealing with Tokens, but I have provided one that does not require a redirect url.
'''

import requests
import webbrowser
import base64
import json
import pickle

from PAExceptions import PAException

class AccessToken:
    '''
    Information about a HomeAway Access Token
    '''
    def __init__(self, email=None, token_type=None, access_token=None, refresh_token=None):
        self.email = email
        self.token_type = token_type
        self.access_token = access_token
        self.refresh_token = refresh_token
    
    def __str__(self):
        return "Email: {}\nToken Type: {}\nAccess Token: {}\nRefresh Token: {}".format(self.email, self.token_type, self.access_token, self.refresh_token)

    def save(self, filename):
        with open(filename, "wb") as f:
            pickle.dump(self, f)

class PyAway:
    '''
    Starting class for HomeAway
    '''
    # TODO: make it so that the token_file is default and automatically saves/loads
    def __init__(self, client_id, client_secret, token_file=None, token=None):
        self.client_id = client_id
        self.client_secret = client_secret
        self.token = token

        if token_file is not None:
            with open(token_file, "rb") as t:
                self.token = pickle.load(t)
        elif self.token is None:
            self.get_new_token()


    def get_new_token(self):
        print("Getting new token.")
        webbrowser.open("https://ws.homeaway.com/oauth/authorize?client_id={}".format(self.client_id))
        print("Go ahead and authorize us to use your information.")
        oauth_code = input("Enter the code they give you here: ")

        # now that we have the OAuth code, let's get a token
        # if this isn't working, check the encoding of the string you are passing
        # to the encoding function. It's probably unicode and that might fuck with it.
        headers = {
                   "Content-Type" : "application/x-www-form-urlencoded", 
                  }
        data = {"code": oauth_code}

        r = requests.post("https://ws.homeaway.com/oauth/token", headers=headers, data=data, auth=(self.client_id, self.client_secret))
        return_json = r.json()
        if r.status_code != 200:
            raise PAException(r.status_code, return_json["message"], return_json["errorCode"])

        self.token = AccessToken(email=return_json["email"], token_type=return_json["token_type"], access_token=return_json["access_token"], refresh_token=return_json["refresh_token"])

    
