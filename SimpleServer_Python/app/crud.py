from flask import jsonify
from app.models import *
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import func

# 修改饮水机状态
def change_state(id, state):
    try:
        machine = Machine.query.get(id)
        if not machine:
            return jsonify({"msg": "item not found"}), 500
        machine.state = state
        db.session.commit()
        return jsonify({"msg": "change state success"}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": "sqlalchemy error: " + str(e)}), 500
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "unexpected error: " + str(e)}), 500

# 查询饮水机位置、状态、水质
def query_info():
    try:
        machines = Machine.query.all()
        result = [machine.to_dict() for machine in machines]
        return jsonify(result), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": "sqlalchemy error: " + str(e)}), 500
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "unexpected error: " + str(e)}), 500

# 查询某饮水机某段时间内的饮水总量
def query_sum(id, begin_time, end_time):
    try:
        """
        sql = f"select machine.id as id, sum(drink.consumption) as sum from machine, drink \
            where machine.id={id} and drink.time>'{begin_time}' and drink.time<'{end_time}' group by machine.id"
        result = session.execute(text(sql)).fetchone()
        """
        result = db.session.query(Machine.id, func.sum(Drink.consumption).label("sum")) \
            .join(Drink, Machine.id == Drink.machineid) \
            .filter(Machine.id == id, Drink.time > begin_time, Drink.time < end_time) \
            .group_by(Machine.id) \
            .first()
        if result is None or result.sum is None:
            return jsonify({"sum": "0"}), 200
        return jsonify({"sum": result.sum}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": "sqlalchemy error: " + str(e)}), 500
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "unexpected error: " + str(e)}), 500

# 查询某学生某段时间在所有饮水机的饮水总量
def query_stu_sum(cardnumber, begin_time, end_time):
    try:
        """
        sql = f"select cardnumber, sum(drink.consumption) as sum from drink \
            where cardnumber={cardnumber} and time>'{begin_time}' and time<'{end_time}' group by cardnumber"
        result = session.execute(text(sql)).fetchone()
        """
        result = db.session.query(Drink.cardnumber, func.sum(Drink.consumption).label("sum")) \
            .filter(Drink.cardnumber == cardnumber, Drink.time > begin_time, Drink.time < end_time) \
            .group_by(Drink.cardnumber) \
            .first()
        if result is None or result.sum is None:
            return jsonify({"sum": "0"}), 200
        return jsonify({"sum": result.sum}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": "sqlalchemy error: " + str(e)}), 500
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "unexpected error: " + str(e)}), 500

# 查询饮水机状态
def query_state(id):
    try:
        machine = Machine.query.get(id)
        if machine is None:
            return -1
        return machine.state
    except SQLAlchemyError as e:
        db.session.rollback()
        return -2
    except Exception as e:
        db.session.rollback()
        return -3

# 增加饮水记录
def add_drink(cardnumber, machineid, localtime, consumption):
    try:
        new_drink = Drink(
            cardnumber=cardnumber,
            machineid=machineid,
            time=localtime,
            consumption=consumption
        )
        db.session.add(new_drink)
        db.session.commit()
        return jsonify({"msg": "add drink success"}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": "sqlalchemy error: " + str(e)}), 500
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "unexpected error: " + str(e)}), 500