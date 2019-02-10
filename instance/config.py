class Config:
    # these belong in a safer place (perhaps as exports in your bash_profile)
    # see https://scotch.io/tutorials/build-a-restful-api-with-flask-the-tdd-way
    SECRET_KEY = 'thisissooosecret_itshouldntevenbehere'
    CSRF_ENABLED = True
    DEBUG = False


class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///dev.db'
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'
    DEBUG = True


app_config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig
}
