from app import db

class Machine(db.Model):
    id = db.Column(db.Integer, primary_key=True, comment='饮水机ID')
    location = db.Column(db.String(100), default=None, nullable=False, comment='位置')
    tds = db.Column(db.Double, default=None, nullable=False, comment='水质')
    state = db.Column(db.Integer, default=None, nullable=False, comment='状态')

    def to_dict(self):
        return {
            'id': self.id,
            'location': self.location,
            'tds': self.tds,
            'state': self.state
        }

class Drink(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='记录编号')
    cardnumber = db.Column(db.Integer, default=None, nullable=False, comment='校园卡号')
    machineid = db.Column(db.Integer, default=None, nullable=False, comment='饮水机ID')
    time = db.Column(db.DateTime, default=None, nullable=False, comment='饮水时间')
    consumption = db.Column(db.Integer, default=None, nullable=False, comment='饮水量')