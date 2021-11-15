import os

BROWSER=os.environ.get('BROWSER', 'HeadlessChrome')
SERVER=os.environ.get('SERVER', 'https://pluto-dev.rnd.eficode.io')

ROBOT_USERNAME=os.environ.get('ROBOT_USERNAME', '')
ROBOT_PASSWORD=os.environ.get('ROBOT_PASSWORD', '')
GITHUB_TOKEN=os.environ.get('GITHUB_TOKEN', '')
