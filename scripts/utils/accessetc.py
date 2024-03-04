import os
import json

def read_db_info(path_to_db_info):

    with open(path_to_db_info) as f:
        db_info = json.load(f)

    db_info = db_info['default']

    config = {
    'user': db_info['USER'],
    'password': db_info['PASSWORD'],
    'host': db_info['HOST'],
    'database' : db_info['NAME'],
    'raise_on_warnings' : True
    } 

    return config