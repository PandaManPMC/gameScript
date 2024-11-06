import threading

# lock = threading.Lock()
lock = threading.RLock()

def func1():
    print("In func1, acquiring lock...")
    with lock:
        print("Lock acquired in func1")
        func2()

def func2():
    print("In func2, acquiring lock...")
    with lock:  # 这里应该会阻塞
        print("Lock acquired in func2")

# 创建并启动线程
t = threading.Thread(target=func1)
t.start()
t.join()
