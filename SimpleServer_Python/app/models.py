from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, Double, DateTime

base = declarative_base()

class machine(base):
    __tablename__ = 'machine'
    id = Column(Integer, primary_key=True, comment='饮水机ID')
    location = Column(String(100), default=None, nullable=False, comment='位置')
    tds = Column(Double, default=None, nullable=False, comment='水质')
    state = Column(Integer, default=None, nullable=False, comment='状态')

class drink(base):
    __tablename__ = 'drink'
    id = Column(Integer, primary_key=True, autoincrement=True, comment='记录编号')
    cardnumber = Column(Integer, default=None, nullable=False, comment='校园卡号')
    machineid = Column(Integer, default=None, nullable=False, comment='饮水机ID')
    time = Column(DateTime, default=None, nullable=False, comment='饮水时间')
    consumption = Column(Integer, default=None, nullable=False, comment='饮水量')