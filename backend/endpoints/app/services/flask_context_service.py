import logging as log
from uuid import UUID

from sqlalchemy.exc import NoResultFound

from dao import user_dao
from utils.jwt_common import JWTParser, JWTParserInitialisationException


class ContextCreationException(Exception):
    pass


class ContextBuilder:

    def __init__(self,
                 keys_file_path: str = None,
                 verify_token_expiration: bool = True,
                 audience_claim: str = 'aud'):
        self.keys_file_path = keys_file_path
        self.verify_token_expiration = verify_token_expiration
        self.audience_claim = audience_claim
        self.jwt_parser = None

    def build_context(self, request):
        try:
            context = request.environ.get('awsgi.context', None)
            event = request.environ.get('awsgi.event', None)

            if event is None:
                auth_header = request.headers.get('Authorization')
                if not auth_header:
                    raise ContextCreationException("No awsgi event or Authorization header. Unauthorized.")

                if auth_header.startswith('Bearer '):
                    token = auth_header[len('Bearer '):len(auth_header)]
                else:
                    token = auth_header

                self.jwt_parser = JWTParser(keys_file_path=self.keys_file_path)
                claims = self.jwt_parser.parse_token(
                    token=token,
                    audience_claim=self.audience_claim,
                    verify_expiration=self.verify_token_expiration)
            else:
                claims = event.get('requestContext', {}).get('authorizer', {}).get('claims', None)

            if claims is None:
                raise Exception("No claims. Unauthorized.")

            # Get the user uuid
            sub = claims.get('sub', None)
            if sub is None:
                raise Exception("No sub in claims. Unauthorized.")

            user = user_dao.get_user(UUID(sub))
            context = {'request': request,
                       'lambda_context': context,
                       'lambda_event': event,
                       'pluto_user': user}
            return context
        except JWTParserInitialisationException as e:
            raise e
        except NoResultFound as e:
            log.exception(f"User '{sub}' not found")
            raise ContextCreationException("Creating context failed")
        except Exception:
            msg = "Creating context failed"
            log.exception(msg)
            raise ContextCreationException(msg)
