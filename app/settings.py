import re
from os import environ

from dotenv import load_dotenv

load_dotenv()


def str2bool(string_value):
    """Converts string representation of boolean to boolean value

    Args:
        string_value (str): String representation of boolean

    Returns:
        bool: True or False
    """
    return string_value.lower() == 'true'


# telegram app id
API_ID = environ.get('API_ID')
# telegram app hash
API_HASH = environ.get('API_HASH')

# channels id to mirroring
CHATS = []

# channels mapping
# [source:target1,target2];[source2:...]
CM = environ.get('CHAT_MAPPING')
MAPPING = {}
if CM is not None:
    matches = re.findall(r'\[(.*?)@(.*?)]', CM, re.MULTILINE)
    print (matches)
    for match in matches:
        source = int(match[0])
        target = match[1]
        MAPPING[source] = target
    CHATS = list(MAPPING.keys())

TIMEOUT_MIRRORING = float(environ.get('TIMEOUT_MIRRORING', '0.1'))
# amount messages before timeout
LIMIT_TO_WAIT = 50
# auth session string: can be obtain by run login.py
SESSION_STRING = environ.get('SESSION_STRING')

# remove urls from messages
REMOVE_URLS = str2bool(environ.get('REMOVE_URLS', 'False'))
REMOVE_URLS_WL = environ.get('REMOVE_URLS_WL')
REMOVE_URLS_WL_DATA = None
if REMOVE_URLS_WL is not None:
    REMOVE_URLS_WL_DATA = REMOVE_URLS_WL.split(',')

LOG_LEVEL = environ.get("LOG_LEVEL", "INFO").upper()
