from flask import jsonify
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import create_engine, text
from config import DatabaseConfig

# 连接池
engine = create_engine(
    DatabaseConfig.SQLALCHEMY_DATABASE_URI,
    # 连接池中最多10个连接
    pool_size=10,
    # 连接池满后最多额外创建20个连接
    max_overflow=20,
    # 等待连接的超时时间为30秒
    pool_timeout=30,
    # 连接在池中超过多少秒后会被回收，设置为-1表示禁用连接回收
    pool_recycle=-1
)
session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)

# 修改饮水机状态
def change_state(id, state):
    session = Session()
    try:
        sql = f'update machine set state={state} where id={id}'
        result = session.execute(text(sql))
        if result.rowcount == 0:
            return jsonify({"msg": "item not found"}), 500
        session.commit()
        return jsonify({"msg": "change state success"}), 200
    except SQLAlchemyError as e:
        session.rollback()
        return jsonify({"error": "sqlalchemy error: " + str(e)}), 500
    except Exception as e:
        session.rollback()
        return jsonify({"error": "unexcepted error: " + str(e)}), 500
    finally:
        session.close()

# 查询饮水机位置、状态、水质
def query_info():
    session = Session()
    try:
        sql = 'select * from machine'
        rows = session.execute(text(sql)).fetchall()
        result = [dict(row._mapping) for row in rows]
        return jsonify(result), 200
    except SQLAlchemyError as e:
        session.rollback()
        return jsonify({"error": "sqlalchemy error: " + str(e)}), 500
    except Exception as e:
        session.rollback()
        return jsonify({"error": "unexcepted error: " + str(e)}), 500
    finally:
        session.close()

# 查询某饮水机某段时间内的饮水总量
def query_sum(id, begin_time, end_time):
    session = Session()
    try:
        sql = f"select machine.id as id, sum(drink.consumption) as sum from machine, drink \
            where machine.id={id} and drink.time>'{begin_time}' and drink.time<'{end_time}' group by machine.id"
        result = session.execute(text(sql)).fetchone()
        if result is None:
            return jsonify({"sum": "0"}), 200
        return jsonify({"sum": result.sum}), 200
    except SQLAlchemyError as e:
        session.rollback()
        return jsonify({"error": "sqlalchemy error: " + str(e)}), 500
    except Exception as e:
        session.rollback()
        return jsonify({"error": "unexcepted error: " + str(e)}), 500
    finally:
        session.close()

# 查询某学生某段时间在所有饮水机的饮水总量
def query_stu_sum(cardnumber, begin_time, end_time):
    session = Session()
    try:
        sql = f"select cardnumber, sum(drink.consumption) as sum from drink \
            where cardnumber={cardnumber} and time>'{begin_time}' and time<'{end_time}' group by cardnumber"
        result = session.execute(text(sql)).fetchone()
        if result is None:
            return jsonify({"sum": "0"}), 200
        return jsonify({"sum": result.sum}), 200
    except SQLAlchemyError as e:
        session.rollback()
        return jsonify({"error": "sqlalchemy error: " + str(e)}), 500
    except Exception as e:
        session.rollback()
        return jsonify({"error": "unexcepted error: " + str(e)}), 500
    finally:
        session.close()

# 查询饮水机状态
def query_state(id):
    session = Session()
    try:
        sql = f"select state from machine where id={id}"
        result = session.execute(text(sql)).fetchone()
        if result is None:
            return -1
        return result.state
    except SQLAlchemyError as e:
        session.rollback()
        return -2
    except Exception as e:
        session.rollback()
        return -3
    finally:
        session.close()

# 增加饮水记录
def add_drink(cardnumber, machineid, localtime, consumption):
    session = Session()
    try:
        sql = 'insert into drink (cardnumber, machineid, time, consumption)\
            values(:cardnumber, :machineid, :time, :consumption)'
        params = {
            'cardnumber': cardnumber,
            'machineid': machineid,
            'time': localtime,
            'consumption': consumption
        }
        result = session.execute(text(sql), params)
        session.commit()
        if result.rowcount == 0:
            jsonify({"msg": "add drink failed"}), 500
        return jsonify({"msg": "add drink success"}), 200
    except SQLAlchemyError as e:
        session.rollback()
        return jsonify({"error": "sqlalchemy error: " + str(e)}), 500
    except Exception as e:
        session.rollback()
        return jsonify({"error": "unexcepted error: " + str(e)}), 500
    finally:
        session.close()

# 其它模板
"""
def update(id, source, data, length):
    session = session_factory()
    try:
        result = session.query(test).filter(test.id==id).update({'source': source, 'data': data, 'length': length})
        if result==0:
            return jsonify({"error": "Item not found"}), 500
        session.commit()
        return jsonify({"msg": "Update success"}), 200

def delete_by_id(id):
    session = session_factory()
    try:
        result = session.query(test).filter(test.id==id).delete()
        if result==0:
            return jsonify({"error": "Item not found"}), 500
        session.commit()
        return jsonify({"msg": "Delete success"}), 200
"""