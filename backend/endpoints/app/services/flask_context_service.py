import logging as log
from uuid import UUID

from dao import user_dao


class ContextCreationException(Exception):
    pass


def build_context(request):
    try:
        event = request.environ['awsgi.event']

        # "requestContext": {
        #     "resourceId": "d4pfum",
        #     "authorizer": {
        #         "claims": {
        #             "sub": "a46c62ce-a84e-4ec0-bb87-b496887e3acf",

        # Get the user uuid
        sub = event.get('requestContext', {}).get('authorizer', {}).get('claims', {}).get('sub', None)
        if sub is None:
            raise Exception("Event did not contain authenticated user subject field")

        user = user_dao.get_user(UUID(sub))
        context = {'request': request,
                   'lambda_context': request.environ['awsgi.context'],
                   'lambda_event': event,
                   'pluto_user': user}
        return context
    except:
        msg = "Creating context failed"
        log.exception(msg)
        raise ContextCreationException(msg)
