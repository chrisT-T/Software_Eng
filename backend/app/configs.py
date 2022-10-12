from app.utils import config


class Config():
    # SQLAlchemy configs
    SQLALCHEMY_DATABASE_URI = config.get_yaml('db.URI', '')
    SQLALCHEMY_RECORD_QUERIES = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True


class DevConfig(Config):
    TYPE = 'dev'
    DEBUG = True


class ProdConfig(Config):
    TYPE = 'prod'
    DEBUG = False


class TestConfig(Config):
    TYPE = 'test'
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///test.db"


configs = {
    "default": DevConfig,
    "dev": DevConfig,
    "prod": ProdConfig,
    "test": TestConfig
}
