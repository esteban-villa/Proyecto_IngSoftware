class Config:
    SECRET_KEY = 'B!1weNAt1T^%KvhUI*S'
    
class DevelopmentConfig(Config):
    DEBUG = True
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = ''
    MYSQL_DB = 'db_proyecto'
    
config = {
    'development':DevelopmentConfig
}