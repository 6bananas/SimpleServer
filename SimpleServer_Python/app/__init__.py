from flask import Flask
from flask_cors import CORS
from flask_sock import Sock
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, template_folder='../templates')

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost:3306/simpleserver'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 支持跨域
CORS(app)

# websocket
sock = Sock(app)

db = SQLAlchemy(app)

# 将导入放在文件末尾以避免循环导入
from app import routes
from app import crud
from app import server
