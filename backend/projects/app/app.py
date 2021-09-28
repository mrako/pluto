import sys


def handler(event, context):
    print("RUNNING THE LAMBDA FUNCTION!!!!")
    return 'Hello from AWS Lambda using Python' + sys.version + '!'
