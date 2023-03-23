
# 一个运行使用"记录宏.py"记录的json的程序

import os  # 用于文件操作
import json  # 用于记录下来的操作
import time  # 用于按照记录下来的时间间隔操作
import sys  # 用于获取命令行传入的参数
import pynput  # 用于模拟鼠标键盘操作
import winsound  # 用于播放提示音
import threading  # 用于多线程


global command_list  # 用于存储记录下来的操作


def repeat_once(command_list, mouse, keyboard, buttons):

    # 开始后已经经过的时间
    sTime = 0

    # 执行每一条记录
    for command in command_list:
        # 如果是点击记录
        if command[0] == "click":
            # 将鼠标移动到记录中的位置
            mouse.position = (command[1][0], command[1][1])
            print("move to", command[1][0], command[1][1])
            # 等待一下
            time.sleep(0.1)
            # 点击
            mouse.click(buttons[command[1][2]])
            print("click", command[1][2])

        # 如果是按键按下
        elif command[0] == "press":
            # 如果是特殊按键,会记录成Key.xxx,这里判断是不是特殊按键
            if command[1][0][:3] == "Key":
                # 按下按键
                keyboard.press(eval(command[1][0], {}, {
                    "Key": pynput.keyboard.Key
                }))
            else:
                # 如果是普通按键,直接按下
                keyboard.press(command[1][0])
        # 如果是按键释放
        elif command[0] == "release":
            # 如果是特殊按键
            if command[1][0][:3] == "Key":
                # 按下按键
                keyboard.press(eval(command[1][0], {}, {
                    "Key": pynput.keyboard.Key
                }))
            else:
                # 普通按键直接按下
                keyboard.release(command[1][0])
        # command[2]代表此操作距离开始操作所经过的时间,用它减去已经经过的时间就是距离下一次操作的时间
        time.sleep(command[2]-sTime)
        # 更新时间
        sTime = command[2]


if __name__ == "__main__":
    path = (sys.argv[1] if len(sys.argv) !=
            1 else input("请输入操作记录文件路径(相对路径从本文件位置开始)和循环次数"))

    # 第二个不是:,也就代表路径是相对路径
    if path[2] != ":":
        # 将其解析为从本文件开始的路径
        path = os.path.join(os.path.dirname(__file__), path)

    loop_times = sys.argv[2]
    print("循环次数:{}".format(loop_times))

    # 打开文件
    with open(path) as f:
        # 将记录的命令写入命令列表
        command_list = json.loads(f.read())

        # 创建鼠标和键盘的执行器,用于模拟键盘和鼠标的操作
    mouse = pynput.mouse.Controller()
    keyboard = pynput.keyboard.Controller()

    # 鼠标的两个按钮
    buttons = {
        "Button.left": pynput.mouse.Button.left,
        "Button.right": pynput.mouse.Button.right
    }

    time.sleep(3)
    duration = 1000  # millisecond
    freq = 440  # Hz
    winsound.Beep(freq, duration)  # 播放提示音,提示用户程序已经开始

    for i in range(int(loop_times)):
        print("Running for {} times".format(i+1))  # 打印一下当前是第几次循环
        repeat_once(command_list, mouse, keyboard, buttons)  # 执行main函数
        time.sleep(0.1)  # 等待一下

    # 播放提示音,提示用户程序已经结束
    winsound.Beep(freq, duration)
    print("Done")
