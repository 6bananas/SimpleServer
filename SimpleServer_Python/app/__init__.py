from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import DatabaseConfig
from flask_sock import Sock
from flask_cors import CORS

app = Flask(__name__)

# 支持跨域
CORS(app)

# websocket
sock = Sock(app)

# 添加配置文件
app.config.from_object(DatabaseConfig)

# 初始化扩展，传入程序实例app，创建db
db = SQLAlchemy(app)

# 将导入放在文件末尾以避免循环导入
from app import routes
from app import database
from app import server
