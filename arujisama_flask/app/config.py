import json
from .common import common_func

directory = common_func.get_cwd_directory("/app/config_files/")


class Config:
    DEBUG = True
    SECRET_KEY = common_func.get_secret_key()


class DevConfig(Config):
    DEBUG = True
    db_info_file = directory + "dbinfo.json"

    with open(db_info_file, mode="r") as fp:
        db_data = json.load(fp)
        database_uri = 'mysql+pymysql://{0}:{1}@{2}:{3}/{4}'.format(db_data['USER'], db_data['PWD'], db_data['HOST'],
                                                                    db_data['PORT'], db_data['NAME'])

    SQLALCHEMY_DATABASE_URI = database_uri
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    DEBUG = False


config_by_name = dict(
    dev=DevConfig,
    prod=ProductionConfig
)
