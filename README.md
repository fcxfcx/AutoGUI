# AutoGUI
自动追踪并记录鼠标和键盘的轨迹，储存在json文件中，然后可以读取并复现同样的操作

需要python环境运行

## 记录

运行：

```shell
python track_trace.py
```

5秒后听到蜂鸣声代表开始记录，此时可以执行需要的操作，按键盘上的ECS键结束记录

同一路径下会产生`commands.json`文件，其中记录了刚才的操作

## 复现

运行：

```sh
python repeat.py commands.json 5
```

此处`commands.json`对应刚刚产生的记录文件，可以更改，但是要保证路径正确（可以使用绝对或相对路径）

后面需要输入一个数字代表需要重复的次数（根据需求更替）

## 注意事项

电脑显示屏需要将显示设置里的缩放调整为100%，否则鼠标移动会不准确





参考：[记录你的操作——pynput模拟和监听键盘鼠标操作 - 简书 (jianshu.com)](https://www.jianshu.com/p/11a8e75f5170)
