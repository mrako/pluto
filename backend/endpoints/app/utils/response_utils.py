import json


def build_response(result: dict, status_code: int):
    return {
        'statusCode': f"{status_code}",
        'body': json.dumps(result),
        'headers': {
            'Content-Type': 'application/json',
        }
    }
