class DatabaseConfig(object):
    HOSTNAME = '127.0.0.1'
    PORT = 3306
    USERNAME = 'root'
    PASSWORD = 'root'
    DATABASE = 'dataserver'
    SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{USERNAME}:{PASSWORD}@{HOSTNAME}:{PORT}/{DATABASE}?charset=utf8'
