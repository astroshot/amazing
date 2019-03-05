# coding=utf-8
import os
import toml

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
config_file = 'config.toml'

# {'mysql': {'master': 'mysql://root@localhost/test?charset=utf8'}}
local_config = toml.load(open(os.path.join(PROJECT_ROOT, 'conf', config_file)))
db_conf = local_config['mysql']
