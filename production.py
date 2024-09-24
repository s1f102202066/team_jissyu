class ProductionConfig:
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'postgresql://user:password@localhost/mydatabase'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
