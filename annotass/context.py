from dataclasses import dataclass
from configparser import ConfigParser

config_ini = ConfigParser()
config_ini.read("config.ini")

@dataclass
class Context:
    version = config_ini.get("main", "VERSION")
    annotation_limit = config_ini.getint("annotass", "ANNOTATION_LIMIT")
    cache_fname = config_ini.get("annotass", "CACHE_FNAME")
    index_fname = config_ini.get("annotass", "INDEX_FNAME")
    store_fname = config_ini.get("annotass", "STORE_FNAME") 
    server_port = config_ini.getint("annotass", "SERVER_PORT")
    debug = config_ini.getboolean("annotass", "DEBUG")
    cors = config_ini.getboolean("annotass", "CORS")
    search_url = config_ini.get("annotass", "SEARCH_URL")
    manifest_url =  config_ini.get("annotass", "MANIFEST_URL")