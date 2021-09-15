# coding=utf-8
import logging
import toml

from src.util.singleton import Config

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='amazing.log',
)

# {'mysql': {'master': 'mysql://root@localhost/test?charset=utf8'}}
conf = Config()
config_file = conf.get('config_file')
local_config = toml.load(config_file)
db_conf = local_config['mysql']

print(db_conf)
