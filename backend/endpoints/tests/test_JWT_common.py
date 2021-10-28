from unittest.mock import MagicMock

import requests
import unittest
import os

from utils.jwt_common import JWTParser, JWTVerificationException


class MockCognitoResponse:
    def __init__(self, url, **kwargs):
        # Get url parameter values - applies only for single digits.
        pass

    def json(self):
        return {
              "keys": [
                {
                  "alg": "RS256",
                  "e": "AQAB",
                  "kid": "pSxliCVEmFQ0XSjyn+Tay/1LGBcHnqPptFrUPx7iQv8=",
                  "kty": "RSA",
                  "n": "uhvK43jhSLaQf5PWXNox9wuKh8S5QlAJF2uS72Xht8iArv-C8ouAk0r5u2LXeINOjvguAh65xDEgDMmP4XwsvtrQyJ8-kRpNfEmNXmHmgliORBCqpdnIyAsZqkCc6Oq9dWO66ZHWPW9uZ8BqVbqGzRsm2yGp5VIcrjjmb_Yrcl6-UOYIOGr8P3Mcb39dFGCW_SQKtzO9H0piTIJUupOkIMm1MQ92SbCh9la9asSN2nVIAjvekMQL9iOvOzYiFBvp4hfkLoaiS83C2gIHWMfnolgtXGDOE5PLoYoGBn-LUVqEQX31jX99T5-q2JNN3WzcbFVqrABlWd_osHWEmMMf_w",
                  "use": "sig"
                },
                {
                  "alg": "RS256",
                  "e": "AQAB",
                  "kid": "jh9oJngxBZKyh6Fd0voN5V2xlayksfFKH6Plf9bBkAI=",
                  "kty": "RSA",
                  "n": "rPp1_Vkh3QzjrbY_UzzCBII4Nb0DfEUFbv_0CMRNL0x7Yvg1FSBwCbc5ZCVZe6gTE3HdUz508dNbgyaBQwFewS78C8K2bHoadXoqQGgTT1QHLnBknXsgt-xWiDZ3v4JE2e_Las0QBBcYC7imMRG0yPRZYzSN26jyJGdXP7RlxB6U3M6rZDtQ__inArNJBZoqzLO-uCYDD_2kQlduNL6q-T3Z8_EbZgUH59YWOhrGTsV17FlELP8pwxyq745oSxZB23x6IgW-qaqFtPVEzhGWjEvW9Ice_3X94J4hOIqWj7JuP5ycjFk6p4tieyPOV5RjlE1vOHwOKLgItD3yVkaG7Q",
                  "use": "sig"
                }
              ]
            }


class TestJwtCommon(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        region = 'aws-region-in-use'
        userpool_id = 'aws-user-pool-id-FOang4duh'
        client_id = '12f6wrg4h5g28jkfofofofofo'
        os.environ['AWS_REGION'] = region
        os.environ['USER_POOL_ID'] = userpool_id
        os.environ['APP_CLIENT_ID'] = client_id

        requests.get = MagicMock(side_effect=MockCognitoResponse)
        url = f"https://cognito-idp.{region}.amazonaws.com/{userpool_id}/.well-known/jwks.json"
        response = requests.get(url).json()

    def test_parse_expired_access_token(self):
        try:
            parser = JWTParser()
            parser.parse_token(
                'eyJraWQiOiJqaDlvSm5neEJaS3loNkZkMHZvTjVWMnhsYXlrc2ZGS0g2UGxmOWJCa0FJPSIsImFsZyI6IlJTMjU2In0.eyJvcmlnaW5fanRpIjoiOTA0MzFiMDEtOTM2NC00MTliLTg0MzYtM2ZkNjZlNWMxOThmIiwic3ViIjoiYTQ2YzYyY2UtYTg0ZS00ZWMwLWJiODctYjQ5Njg4N2UzYWNmIiwiZXZlbnRfaWQiOiI2Y2I1NGJmMi02YTYxLTQ5YjQtYjM1ZC1hMjQ3YjQ4Yjg3YTEiLCJ0b2tlbl91c2UiOiJhY2Nlc3MiLCJzY29wZSI6ImF3cy5jb2duaXRvLnNpZ25pbi51c2VyLmFkbWluIiwiYXV0aF90aW1lIjoxNjM1MTUyMzk0LCJpc3MiOiJodHRwczpcL1wvY29nbml0by1pZHAuZXUtd2VzdC0xLmFtYXpvbmF3cy5jb21cL2V1LXdlc3QtMV9LQXlOaFMyaVEiLCJleHAiOjE2MzUxNTU5OTQsImlhdCI6MTYzNTE1MjM5NCwianRpIjoiN2NlZTJmNzEtMDRmNi00MDFiLWFhNDctYjgxZWZmMGIxMDBlIiwiY2xpZW50X2lkIjoiNTZ0NGRuaDhuNXY4amtkNDFmOXNzdjAybXQiLCJ1c2VybmFtZSI6ImE0NmM2MmNlLWE4NGUtNGVjMC1iYjg3LWI0OTY4ODdlM2FjZiJ9.ZRUoIdoDdYqxS07iYLdjjPqbv9Kcyd9w0k095NAUt4V1MdibJUERiLCH3PmtkCHVSCqC5diUHmuVktfsnVcXe-KTeEATqrwJKgyCApQMYPeCLfkJAagyfH4Jzpf_8O6nDndmG3SBXJOcCVXlfu3qhMhoCSSP6v1gkOGxC_Kh55rn8FywWedNHiT9JJ1f76Rv1GXJjmnYmM67ja0e7IGnEpw-6h9znOHV0zV_INCBL6cPkfEiSiD3R_OxcWxpkxjSoI4JNL0XNKo2s7urQn85nR0ZfK25Kpc402FVja65iPu79gZT9LLw2gn4AtANOj-L6MJl1F6Z3PDjxh1iq1MpFg',
                'client_id')
            self.fail("Token expiration should of been verified")
        except JWTVerificationException as e:
            self.assertEqual('Token has expired', str(e))

    def test_parse_access_token(self):
        os.environ['AWS_REGION'] = 'eu-west-1'
        os.environ['USER_POOL_ID'] = 'eu-west-1_KAyNhS2iQ'
        os.environ['APP_CLIENT_ID'] = '56t4dnh8n5v8jkd41f9ssv02mt'

        parser = JWTParser()
        parser.parse_token(
            'eyJraWQiOiJqaDlvSm5neEJaS3loNkZkMHZvTjVWMnhsYXlrc2ZGS0g2UGxmOWJCa0FJPSIsImFsZyI6IlJTMjU2In0.eyJvcmlnaW5fanRpIjoiOTA0MzFiMDEtOTM2NC00MTliLTg0MzYtM2ZkNjZlNWMxOThmIiwic3ViIjoiYTQ2YzYyY2UtYTg0ZS00ZWMwLWJiODctYjQ5Njg4N2UzYWNmIiwiZXZlbnRfaWQiOiI2Y2I1NGJmMi02YTYxLTQ5YjQtYjM1ZC1hMjQ3YjQ4Yjg3YTEiLCJ0b2tlbl91c2UiOiJhY2Nlc3MiLCJzY29wZSI6ImF3cy5jb2duaXRvLnNpZ25pbi51c2VyLmFkbWluIiwiYXV0aF90aW1lIjoxNjM1MTUyMzk0LCJpc3MiOiJodHRwczpcL1wvY29nbml0by1pZHAuZXUtd2VzdC0xLmFtYXpvbmF3cy5jb21cL2V1LXdlc3QtMV9LQXlOaFMyaVEiLCJleHAiOjE2MzUxNTU5OTQsImlhdCI6MTYzNTE1MjM5NCwianRpIjoiN2NlZTJmNzEtMDRmNi00MDFiLWFhNDctYjgxZWZmMGIxMDBlIiwiY2xpZW50X2lkIjoiNTZ0NGRuaDhuNXY4amtkNDFmOXNzdjAybXQiLCJ1c2VybmFtZSI6ImE0NmM2MmNlLWE4NGUtNGVjMC1iYjg3LWI0OTY4ODdlM2FjZiJ9.ZRUoIdoDdYqxS07iYLdjjPqbv9Kcyd9w0k095NAUt4V1MdibJUERiLCH3PmtkCHVSCqC5diUHmuVktfsnVcXe-KTeEATqrwJKgyCApQMYPeCLfkJAagyfH4Jzpf_8O6nDndmG3SBXJOcCVXlfu3qhMhoCSSP6v1gkOGxC_Kh55rn8FywWedNHiT9JJ1f76Rv1GXJjmnYmM67ja0e7IGnEpw-6h9znOHV0zV_INCBL6cPkfEiSiD3R_OxcWxpkxjSoI4JNL0XNKo2s7urQn85nR0ZfK25Kpc402FVja65iPu79gZT9LLw2gn4AtANOj-L6MJl1F6Z3PDjxh1iq1MpFg',
            'client_id',
            verify_expiration=False)

    def test_parse_expired_id_token(self):
        os.environ['AWS_REGION'] = 'eu-west-1'
        os.environ['USER_POOL_ID'] = 'eu-west-1_KAyNhS2iQ'
        os.environ['APP_CLIENT_ID'] = '56t4dnh8n5v8jkd41f9ssv02mt'

        try:
            parser = JWTParser()
            parser.parse_token(
                'eyJraWQiOiJwU3hsaUNWRW1GUTBYU2p5bitUYXlcLzFMR0JjSG5xUHB0RnJVUHg3aVF2OD0iLCJhbGciOiJSUzI1NiJ9.eyJzdWIiOiJhNDZjNjJjZS1hODRlLTRlYzAtYmI4Ny1iNDk2ODg3ZTNhY2YiLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZSwiaXNzIjoiaHR0cHM6XC9cL2NvZ25pdG8taWRwLmV1LXdlc3QtMS5hbWF6b25hd3MuY29tXC9ldS13ZXN0LTFfS0F5TmhTMmlRIiwiY29nbml0bzp1c2VybmFtZSI6ImE0NmM2MmNlLWE4NGUtNGVjMC1iYjg3LWI0OTY4ODdlM2FjZiIsIm9yaWdpbl9qdGkiOiIzNjBmY2ZhZi0yNDQ2LTRiYmYtODgyNi1iZmU4YzhmYjk2YjAiLCJhdWQiOiI1NnQ0ZG5oOG41djhqa2Q0MWY5c3N2MDJtdCIsImV2ZW50X2lkIjoiYzk1YjNkYzItMTc4Yy00OTU5LWIzYjQtNjk3NmVmNGRmYWQ3IiwidG9rZW5fdXNlIjoiaWQiLCJhdXRoX3RpbWUiOjE2MzUyNDkyNzksImV4cCI6MTYzNTI1Mjg3OSwiaWF0IjoxNjM1MjQ5Mjc5LCJqdGkiOiIzM2IwN2Y3Ni0xMzRiLTQ1YjctYTIwMi0wZjIxZjNjOTY2NzMiLCJlbWFpbCI6Im1pa2tpLmxldm9uQGdtYWlsLmNvbSJ9.WziFuStSjWDEL5NbIrlL3ApcLV8pww0E6beIVCyGwu4QHuIlM7dTB4mgOD_73mXetKH536etWVmiM_CHkYCBCNkoCta5iWGNmh63khsWDiz3ioOrww7xaORuNjoThREmz46aBXXFpp2PZw-3sgnBRzgbsx0jYyyFHyiANr1AsUon5kBohAehAu4Pc8qQfS0Y6FbGW8D5irl7iPRtiOIDZXe7xFp8RT_ifHBuFhPu87f5KpTpG3EXgJ8lJWesec-4jypW398kDn1FWlrwn_iGthBLldbdmpaSHezKEYxaogiNy3-vxdXhGaq9rrJmTfe_MU12wtq_CHa1i2O5gX19lw',
                'aud')
            self.fail("Token expiration should of been verified")
        except JWTVerificationException as e:
            self.assertEqual('Token has expired', str(e))

    def test_parse_id_token(self):
        os.environ['AWS_REGION'] = 'eu-west-1'
        os.environ['USER_POOL_ID'] = 'eu-west-1_KAyNhS2iQ'
        os.environ['APP_CLIENT_ID'] = '56t4dnh8n5v8jkd41f9ssv02mt'

        parser = JWTParser()
        parser.parse_token(
            'eyJraWQiOiJwU3hsaUNWRW1GUTBYU2p5bitUYXlcLzFMR0JjSG5xUHB0RnJVUHg3aVF2OD0iLCJhbGciOiJSUzI1NiJ9.eyJzdWIiOiJhNDZjNjJjZS1hODRlLTRlYzAtYmI4Ny1iNDk2ODg3ZTNhY2YiLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZSwiaXNzIjoiaHR0cHM6XC9cL2NvZ25pdG8taWRwLmV1LXdlc3QtMS5hbWF6b25hd3MuY29tXC9ldS13ZXN0LTFfS0F5TmhTMmlRIiwiY29nbml0bzp1c2VybmFtZSI6ImE0NmM2MmNlLWE4NGUtNGVjMC1iYjg3LWI0OTY4ODdlM2FjZiIsIm9yaWdpbl9qdGkiOiIzNjBmY2ZhZi0yNDQ2LTRiYmYtODgyNi1iZmU4YzhmYjk2YjAiLCJhdWQiOiI1NnQ0ZG5oOG41djhqa2Q0MWY5c3N2MDJtdCIsImV2ZW50X2lkIjoiYzk1YjNkYzItMTc4Yy00OTU5LWIzYjQtNjk3NmVmNGRmYWQ3IiwidG9rZW5fdXNlIjoiaWQiLCJhdXRoX3RpbWUiOjE2MzUyNDkyNzksImV4cCI6MTYzNTI1Mjg3OSwiaWF0IjoxNjM1MjQ5Mjc5LCJqdGkiOiIzM2IwN2Y3Ni0xMzRiLTQ1YjctYTIwMi0wZjIxZjNjOTY2NzMiLCJlbWFpbCI6Im1pa2tpLmxldm9uQGdtYWlsLmNvbSJ9.WziFuStSjWDEL5NbIrlL3ApcLV8pww0E6beIVCyGwu4QHuIlM7dTB4mgOD_73mXetKH536etWVmiM_CHkYCBCNkoCta5iWGNmh63khsWDiz3ioOrww7xaORuNjoThREmz46aBXXFpp2PZw-3sgnBRzgbsx0jYyyFHyiANr1AsUon5kBohAehAu4Pc8qQfS0Y6FbGW8D5irl7iPRtiOIDZXe7xFp8RT_ifHBuFhPu87f5KpTpG3EXgJ8lJWesec-4jypW398kDn1FWlrwn_iGthBLldbdmpaSHezKEYxaogiNy3-vxdXhGaq9rrJmTfe_MU12wtq_CHa1i2O5gX19lw',
            'aud',
            verify_expiration=False)
