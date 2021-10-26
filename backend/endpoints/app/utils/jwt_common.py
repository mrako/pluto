import os
import time
import requests
from jose import jwk, jwt
from jose.utils import base64url_decode
from functools import wraps
from flask import request

def get_key_index(keys, kid):
    index = -1
    for key in keys:
        index += 1
        if kid == key['kid']:
            return index
    return None


class JWTVerificationException(Exception):
    pass


class JWTParser:

    def __init__(self):
        self.region = os.environ['AWS_REGION']
        self.userpool_id = os.environ['USER_POOL_ID']
        self.app_client_id = os.environ['APP_CLIENT_ID']
        self.keys_url = f"https://cognito-idp.{self.region}.amazonaws.com/{self.userpool_id}/.well-known/jwks.json"
        self.keys = requests.get(self.keys_url).json()['keys']

    def parse_token(self, token: str, audience_claim: str, verify_expiration: bool = True):
        """
        Parses and validates a JWT token

        Parameters
        ----------
        token : str
            The JWT token string to parse
        audience_claim : str
            Claim name the audience should be parsed from ('aud', 'client_id')
            use 'client_id' if parsing an access token
            use 'aud' if parsing id token
        verify_expiration: bool
            Whether or not to verify if the token has expired (default is True)
        """
        # get the kid from the headers prior to verification
        headers = jwt.get_unverified_headers(token)
        kid = headers['kid']

        # search for the kid in the downloaded public keys
        key_index = get_key_index(self.keys, kid)
        if key_index is None:
            raise JWTVerificationException('Matching key not found from Cognito')

        # construct the public key
        public_key = jwk.construct(self.keys[key_index])

        # get the last two sections of the token,
        # message and signature (encoded in base64)
        message, encoded_signature = str(token).rsplit('.', 1)

        # decode the signature
        decoded_signature = base64url_decode(encoded_signature.encode('utf-8'))

        # verify the signature
        if not public_key.verify(message.encode("utf8"), decoded_signature):
            raise JWTVerificationException('Invalid JWT signature')

        # since we passed the verification, we can now safely
        # use the unverified claims
        claims = jwt.get_unverified_claims(token)

        # Verify the token expiration
        if verify_expiration and time.time() > claims['exp']:
            raise JWTVerificationException('Token has expired')

        # and the Audience  (use claims['client_id'] if verifying an access token)
        audience = claims.get(audience_claim, None)
        if audience != self.app_client_id:
            raise JWTVerificationException(f"Incorrect audience. Audience claim used: {audience_claim}")

        return claims
