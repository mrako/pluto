import logging as log


def github_auth_headers():
    return {'Authorization': 'Bearer '+app.config['GITHUB_ACCESS_TOKEN']}


def add_error(result, msg):
    result['success'] = False
    if 'errors' in result:
        result['errors'].append(msg)
    else:
        result['errors'] = [msg]


def query_db(*args, **kwargs):
    field_name = args[0]
    try:
        return {"success": True,
                field_name: args[1](**kwargs)}
    except:
        msg = f"Retrieving {field_name} failed"
        log.exception(msg)
        return {
            "success": False,
            "errors": [msg]
        }
