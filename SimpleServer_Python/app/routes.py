from flask import request, send_file
from app import app
from app.crud import *
from werkzeug.utils import secure_filename

# 全局变量，用于实时传递前端->硬件的信息
TH = {2001:'', 2002:''}
th_id = ''
th_flag = False
state_flag = False
machine_id = ''
machine_state = ''

def get_th():
    global TH, th_id
    return TH[th_id]

def get_th_id():
    global th_id
    return th_id

def get_th_flag():
    global th_flag
    return th_flag

def set_th_flag(tf):
    global th_flag
    th_flag = tf

def get_state_flag():
    global state_flag
    return state_flag

def set_state_flag(sf):
    global state_flag
    state_flag = sf

def get_machine_id():
    global machine_id
    return machine_id

def get_machine_state():
    global machine_state
    return machine_state

#修改饮水机状态
@app.route('/change_state', methods=['POST'])
def change_state_method():
    global state_flag, machine_id, machine_state
    data = request.get_json()
    id = data.get('id')
    state = data.get('state')
    result, state_code = change_state(id, state)
    if state_code==200:
        state_flag = True
        machine_id = id
        machine_state = state
    print('/change_state ', state_code)
    if state_code==500:
        print(result.data)
    return result, state_code

#修改TH值
@app.route('/change_th', methods=['POST'])
def change_th_method():
    global TH, th_flag, th_id
    data = request.get_json()
    th_id = data.get('id')
    th = data.get('th')
    th = float(th)
    TH[th_id] = th
    th_flag = not th_flag
    result = jsonify({"msg": "change th success"})
    print(f'/change_th success: {th_id} {TH[th_id]}')
    return result, 200

#查询饮水机位置、状态、水质
@app.route('/query_info', methods=['GET'])
def query_info_method():
    result, state_code = query_info()
    print('/query_info ', state_code)
    if state_code==500:
        print(result.data)
    return result, state_code

#查询某饮水机某段时间内的饮水总量
@app.route('/query_sum', methods=['POST'])
def query_sum_method():
    data = request.get_json()
    id = data.get('id')
    begin_time = data.get('begintime')
    end_time = data.get('endtime')
    result, state_code = query_sum(id, begin_time, end_time)
    print('/query_sum ', state_code)
    if state_code==500:
        print(result.data)
    return result, state_code

#查询某学生某段时间在所有饮水机的饮水总量
@app.route('/query_stu_sum', methods=['POST'])
def query_stu_sum_method():
    data = request.get_json()
    cardnumber = data.get('cardnumber')
    begin_time = data.get('begintime')
    end_time = data.get('endtime')
    result, state_code = query_stu_sum(cardnumber, begin_time, end_time)
    print('/query_stu_sum ', state_code)
    if state_code==500:
        print(result.data)
    return result, state_code

# 文件上传
@app.route('/upload_file', methods=['POST'])
def upload_file_method():
    try:
        # 请求中是否包含文件
        if 'file' not in request.files:
            print("no file")
            return jsonify({"msg": "no file"}), 500
        file = request.files['file']
        if file:
            file_name = secure_filename(file.filename)
            file.save(file_name)
            print("upload success")
            return jsonify({"msg": "upload success"}), 200
    except Exception as e:
        print(f"upload failed: {e}")
        return jsonify({"msg": "upload failed"}), 500

# 文件下载
@app.route('/download_file', methods=['POST'])
def download():
    data = request.get_json()
    filename = data.get('filename')
    return send_file(filename, as_attachment=True)