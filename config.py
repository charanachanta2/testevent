import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'buildhub_production_secure_key_2026')
    DEBUG = False

class DevelopmentConfig(Config):
    DEBUG = True

config_by_name = {
    'development': DevelopmentConfig,
    'production': DevelopmentConfig
}
