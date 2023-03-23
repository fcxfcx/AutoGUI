
# 一个记录用户操作,并保存到json文件的程序

import time  # 用于记录每一项操作的时间
import json  # 用于保存导出我们记录的操作
import threading  # 由于键盘和鼠标事件的监听都是阻塞的,所以用两个线程实现
import pynput  # 用于记录用户事件
import winsound  # 用于播放提示音
command_list = []  # 用来存储用户的操作
isRunning = True  # 是否在运行,用于实现在按esc后退出的功能
startTime = 0  # 开始时间,会在之后main函数中进行初始化


def on_key_press(key):  # 当按键按下时记录
    if key == pynput.keyboard.Key.esc:  # 如果是esc
        global isRunning
        isRunning = False  # 通知监听鼠标的线程
        mouse = pynput.mouse.Controller()  # 获取鼠标的控制器
        mouse.click(pynput.mouse.Button.left)  # 通过模拟点击鼠标以执行鼠标的线程,然后退出监听.
        return False  # 监听函数return False表示退出监听
    command_list.append((
        "press",  # 操作模式
        # 具体按下的键,传进来的参数并不是一个字符串,而是一个对象,如果按下的是普通的键,会记录下键对应的字符,否则会使一个"Key.xx"的字符串
        (str(key).strip("'"),),
        time.time()-startTime  # 操作距离程序开始运行的秒数
    ))


def on_key_release(key):  # 但按键松开时记录
    command_list.append((
        "release",  # 操作模式
        (str(key).strip("'"),),  # 键信息,参见on_key_press中的相同部分
        time.time()-startTime  # 操作距离程序开始运行的秒数
    ))


def on_mouse_click(x, y, button, pressed):
    if not isRunning:  # 如果已经不在运行了
        return False  # 退出监听
    if not pressed:  # 如果是松开事件
        return True  # 不记录
    command_list.append((
        "click",  # 操作模式
        (x, y, str(button)),  # 分别是鼠标的坐标和按下的按键
        time.time()-startTime  # 操作距离程序开始运行的秒数
    ))


def start_key_listen():  # 用于开始按键的监听
    # 进行监听
    with pynput.keyboard.Listener(on_press=on_key_press, on_release=on_key_release) as listener:
        listener.join()


def start_mouse_listen():  # 用于开始鼠标的监听
    # 进行监听
    with pynput.mouse.Listener(on_click=on_mouse_click) as listener:
        listener.join()


def toFile(command_list, path):  # 保存为文件,参数分别为操作记录和保存位置
    with open(path, "w") as f:
        f.write(json.dumps(command_list))  # 使用json格式写入


def main():  # 主函数
    global startTime
    startTime = time.time()  # 初始化开始时间
    t1 = threading.Thread(target=start_key_listen)  # 创建用于监听按键的线程
    t2 = threading.Thread(target=start_mouse_listen)  # 创建用于监听鼠标的线程
    # 运行线程
    t1.start()
    t2.start()
    # 等待线程结束,也就是等待用户按下esc
    t1.join()
    t2.join()
    # 保存文件
    toFile(command_list, "./commands.json")


if __name__ == "__main__":
    time.sleep(5)  # 等待5秒,以便用户切换到需要记录的窗口
    duration = 1000  # millisecond
    freq = 440  # Hz
    winsound.Beep(freq, duration)  # 播放提示音
    main()
