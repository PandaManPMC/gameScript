import ctypes
import sys
import psutil

# 定义 Windows API 函数
kernel32 = ctypes.windll.kernel32

# DLL 路径
dll_path = r"D:\a\codes\game_script\pythonProject\dao2\demo\ket_f8_dl.dll"

# 获取目标进程 PID
process_name = "Snipaste.exe"

target_process = None
# 获取指定进程的 pid
for proc in psutil.process_iter(['pid', 'name']):
    if process_name in proc.info['name']:
        target_process = proc.info['pid']
        print(f"process_name={process_name} target_process={target_process}")
        break

if target_process is None:
    raise Exception("目标进程未找到")

# 打开目标进程
process_handle = kernel32.OpenProcess(0x1F0FFF, False, target_process)
if not process_handle:
    print("打开目标进程失败", ctypes.windll.kernel32.GetLastError())
    sys.exit(1)

# 分配内存
dll_len = len(dll_path) + 1  # 包含空字符
memory = kernel32.VirtualAllocEx(process_handle, 0, dll_len, 0x3000, 0x40)
if not memory:
    print("内存分配失败", ctypes.windll.kernel32.GetLastError())
    sys.exit(1)

# 写入 DLL 路径
written = ctypes.c_int(0)
result = kernel32.WriteProcessMemory(process_handle, memory, dll_path.encode('utf-8'), dll_len, ctypes.byref(written))
if not result:
    print("写入内存失败", ctypes.windll.kernel32.GetLastError())
    sys.exit(1)

# 获取 LoadLibraryW 地址
load_lib = kernel32.GetProcAddress(kernel32.GetModuleHandleA(b"kernel32.dll"), "LoadLibraryW")
if not load_lib:
    print("获取 LoadLibraryW 地址失败", ctypes.windll.kernel32.GetLastError())
    sys.exit(1)

# 创建远程线程来加载 DLL
thread = kernel32.CreateRemoteThread(process_handle, 0, 0, load_lib, memory, 0, 0)
if not thread:
    print("创建远程线程失败", ctypes.windll.kernel32.GetLastError())
    sys.exit(1)

# 等待线程完成
kernel32.WaitForSingleObject(thread, 0xFFFFFFFF)

# 关闭句柄
kernel32.CloseHandle(process_handle)
kernel32.CloseHandle(thread)

print("DLL 注入成功")
