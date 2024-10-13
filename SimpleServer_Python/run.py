from app import app
from app.server import start_tcp
import threading
import sys
import inspect
import signal

# 优雅地关闭服务器
def sigint_handler(signal, frame):
    print('server has terminated')
    cleanup(0)

def _cleanup(attr, method, args):
    code = 0
    if hasattr(attr, method):
        try:
            getattr(attr, method)(*args)
        except Exception as exc:
            sys.stderr.write(f'error cleaning up attribute {repr(attr)}: {exc}')
            code = 1
    return code

def cleanup(code=0):
    for attr in globals().values():
        if not (inspect.isclass(attr) or inspect.isfunction(attr)):
            if not code:
                code |= _cleanup(attr, '__del__', ())
                code |= _cleanup(attr, '__exit__', (None, None, None))

    exit(code)

signal.signal(signal.SIGINT, sigint_handler)

# main
def main():
    try:
        # 启动TCP服务器
        tcp_thread = threading.Thread(target=start_tcp, args=())
        tcp_thread.daemon = True # 设置为守护线程
        tcp_thread.start()
        # 启动flask
        app.run(host='0.0.0.0', port=5001)
    except KeyboardInterrupt:
        # Ctrl+C终止时
        cleanup(0)

if __name__ == '__main__':
    main()
