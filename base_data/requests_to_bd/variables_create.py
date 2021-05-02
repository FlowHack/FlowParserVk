from settings import DEFAULT_VALUE_FOR_BD

USER_DATA_DB = '''
CREATE TABLE IF NOT EXISTS {tb_name}(
    access_token TEXT NOT NULL
)
'''
USER_DATA_DEFAULT = [f'"{DEFAULT_VALUE_FOR_BD}"']

SETTINGS_DB = '''
CREATE TABLE IF NOT EXISTS {tb_name}(
    auto_update INTEGER NOT NULL,
    first_start INTEGER NOT NULL,
    start_free_version INTEGER NOT NULL
)
'''
SETTINGS_DEFAULT = ['1', '1', '0']

GET_REQUESTS_DB = '''
CREATE TABLE IF NOT EXISTS {tb_name}(
    pk INTEGER PRIMARY KEY NOT NULL,
    type_request TEXT NOT NULL, 
    count_people INTEGER NOT NULL,
    response TEXT NOT NULL,
    time_request INTEGER NOT NULL,
    last_parse INTEGER NOT NULL
)
'''
ADDITIONAL_GET_REQUEST_DB = '''
CREATE TABLE IF NOT EXISTS {tb_name}(
    pk_attachment INTEGER NOT NULL,
    response TEXT NOT NULL
)
'''
