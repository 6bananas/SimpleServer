import socket
import time
import threading
import json
from datetime import datetime
from app.database import query_state, add_drink
from app.routes import *
from app import sock

# 全局变量，用于实时传递硬件->前端的信息
ewn = False
ewn_id = None
ewn_state = None

# 获取系统时间
def get_time():
    now = datetime.now()
    format_time = now.strftime('%Y-%m-%d %H:%M:%S')
    return format_time

# 获取设定情况
def get_state(id):
    state = query_state(id)
    if state >= 0:
        return state
    return None

# 线程内函数，处理TH改变、饮水机状态改变error/warning/normal
def th_state(client_socket):
    while True:
        if get_th_flag() == True:
            # 连续发五次，防止硬件因与其它信息冲突而收不到
            for i in range(5):
                client_socket.send(json.dumps({"ID": get_th_id(), "TH": get_th()}).encode('utf-8'))
                set_th_flag(False)
                # 给硬件处理时间
                time.sleep(0.5)
        if get_state_flag() == True:
            # 连续发五次，防止硬件因与其它信息冲突而收不到
            for i in range(5):
                client_socket.send(json.dumps({"ID": get_machine_id(), "systemState": get_machine_state()}).encode('utf-8'))
                set_state_flag(False)
                # 给硬件处理时间
                time.sleep(0.5)


# TCP连接处理函数
def handle_client(client_socket):
    try:
        ts_thread = threading.Thread(target=th_state, args=(client_socket,))
        ts_thread.start()
        with app.app_context():
            while True:
                try:
                    raw_data = client_socket.recv(1024)
                    if raw_data:
                        print("tcp data: ", end='')
                        print(raw_data)
                        decode_data = raw_data.decode('utf-8')
                        if decode_data[0] == '[':
                            decode_data = decode_data[0:len(decode_data) - 2] + ']'
                        if decode_data[0] == '{':
                            index = decode_data.find('}')
                            decode_data = decode_data[:index+1]
                        data = json.loads(decode_data)
                        # 饮水记录
                        if isinstance(data, list):
                            print('receive drink data')
                            for d in data:
                                id = d['ID']
                                localtime = d['localTime']
                                cardnum = d['cardNum']
                                water = d['water']
                                result, state_code = add_drink(cardnum, id, localtime, water)
                                if state_code == 200:
                                    print('add drink success')
                                else:
                                    print(f'add drink failed: {result.data}')
                        else:
                            if 'ID' in data and 'localTime' in data and 'cardNum' in data and 'water' in data:
                                print('receive drink data')
                                id = data['ID']
                                localtime = data['localTime']
                                cardnum = data['cardNum']
                                water = data['water']
                                result, state_code = add_drink(cardnum, id, localtime, water)
                                if state_code == 200:
                                    print('add drink success')
                                else:
                                    print(f'add drink failed: {result.data}')
                            # 故障或警告
                            if 'ID' in data and 'localTime' in data and 'state' in data:
                                print('receive e/w/n')
                                id = data['ID']
                                state = data['state']
                                to_state = ''
                                if state == 'Error1':
                                    to_state = 3
                                elif state == 'Warning1':
                                    to_state = 4
                                elif state == 'Normal':
                                    to_state = 1
                                result, state_code = change_state(id, to_state)
                                if state_code == 200:
                                    global ewn, ewn_id, ewn_state
                                    ewn = True
                                    ewn_id = id
                                    ewn_state = to_state
                                    print('handle e/w/n success')
                                else:
                                    print(f'handle e/w/n failed: {result.data}')
                            # 复位
                            if 'ID' in data and 'state' in data:
                                id = data['ID']
                                status = data['state']
                                if status == 'reset':
                                    print('receive reset command')
                                    system_time = get_time()
                                    # state = get_state(id)
                                    client_socket.send(json.dumps({"ID": id, "clock": system_time}).encode('utf-8'))
                                    # client_socket.send(json.dumps({"ID":id,"systemState":state}).encode('utf-8'))
                                    result, state_code = change_state(id, 1)
                                    if state_code == 200:
                                        print('reset success')
                                    else:
                                        print(f'reset failed: {result.data}')
                except Exception as e:
                    print(f'TCP handle error: {e}')
                    break
    except Exception as e:
        print(f'TCP function error: {e}')
    finally:
        client_socket.close()
        print('tcp disconnected')


# 启动TCP服务器
def start_tcp():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 5000))
    server.listen(5)
    while True:
        # 接收连接
        client_socket, address = server.accept()
        print('tcp client connect success: ', address)
        # 创建新线程处理连接
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()

# websocket接口
@sock.route('/temperature')
def temperature(ws):
    while True:
        """
        ws.send("hello world")
        time.sleep(1)
        data = ws.receive()
        if data == 'exit':
            ws.close()
            break
        ws.send(f'回显：{data}')
        """
        global ewn, ewn_id, ewn_state
        if ewn is True:
            ws.send('{"id": ' + str(ewn_id) + ', "state": "' + str(ewn_state) + '"}')
            ewn = False
            print('send ewn success')
