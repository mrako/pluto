import os
import time
import json
import requests
from jose import jwk, jwt
from jose.utils import base64url_decode


def get_key_index(keys, kid):
    index = -1
    for key in keys:
        index += 1
        if kid == key['kid']:
            return index
    return None


class JWTParserInitialisationException(Exception):
    pass


class JWTVerificationException(Exception):
    pass


class JWTParser:

    def __init__(self, keys_file_path=None):
        self.app_client_id = os.environ.get('APP_CLIENT_ID', None)

        if keys_file_path is not None:
            with open(keys_file_path, 'r') as json_file:
                self.keys = json.load(json_file)['keys']
        else:
            self.region = os.environ.get('AWS_REGION', None)
            self.userpool_id = os.environ.get('USER_POOL_ID', None)

            if self.region is None or self.userpool_id is None or self.app_client_id is None:
                raise JWTParserInitialisationException(
                    "AWS_REGION, USER_POOL_ID and APP_CLIENT_ID must be defined as environment variables")

            self.keys_url = f"https://cognito-idp.{self.region}.amazonaws.com/{self.userpool_id}/.well-known/jwks.json"
            self.keys = requests.get(self.keys_url).json()['keys']

    def parse_token(self, token: str, verify_expiration: bool = True, audience_claim: str = 'aud'):
        """
        Parses and validates a JWT token

        Parameters
        ----------
        token : str
            The JWT token string to parse
        verify_expiration: bool
            Whether or not to verify if the token has expired (default is True)
        audience_claim : str
            Claim name the audience should be parsed from ('aud', 'client_id', None)
            use 'client_id' if parsing an access token
            use 'aud' if parsing id token
            use None if you wish not to verify the audience

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
        if audience and audience != self.app_client_id:
            raise JWTVerificationException(f"Incorrect audience. Audience claim used: {audience_claim}")

        return claims
