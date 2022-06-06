#-*- coding:utf-8 -*-
from pynput.mouse import Button, Controller


## ================================================
##              控制鼠标
## ================================================
# 读鼠标坐标
mouse = Controller()
print('The current pointer position is {0}'.format(mouse.position))
# 设置鼠标坐标
# mouse.position = (10, 20)
# print('Now we have moved it to {0}'.format(mouse.position))
# # 移动鼠标到相对位置
# mouse.move(5, -5)
# # 按住和放开鼠标
# mouse.press(Button.left)        # 按住鼠标左键
# mouse.release(Button.left)      # 放开鼠标左键
# # 点击鼠标
# mouse.click(Button.left, 2)     # 点击鼠标2下
# # 鼠标滚轮
# mouse.scroll(0, 2)              # 滚动鼠标

## 监听鼠标
from pynput.mouse import Listener

def on_move(x, y):
    # 监听鼠标移动
    a=1
    # print('Pointer moved to {0}'.format((x, y)))

def on_click(x, y, button, pressed):
    # 监听鼠标点击
    print('{0} at {1}'.format('click' if pressed else 'Released', (x, y)))
    if not pressed:
        # Stop listener
        return False

def on_scroll(x, y, dx, dy):
    # 监听鼠标滚轮
    a=2
    # print('Scrolled {0}'.format((x, y)))

# 连接事件以及释放
with Listener(on_move=on_move, on_click=on_click, on_scroll=on_scroll) as listener:
    listener.join()
# 一个鼠标监听器是一个线程。线程，所有的回调将从线程调用。从任何地方调用pynput.mouse.Listener.stop，或者调用pynput.mouse.Listener.StopException或从回调中返回False来停止监听器。


## ================================================
##              控制键盘
## ================================================
# from pynput.keyboard import Key, Controller
#
# keyboard = Controller()
# # 按键盘和释放键盘
# keyboard.press(Key.space)
# keyboard.release(Key.space)
#
# # 按小写的a
# keyboard.press('a')
# keyboard.release('a')
#
# # 按大写的A
# keyboard.press('A')
# keyboard.release('A')
#
# # 按住shift在按a
# with keyboard.pressed(Key.shift):
#     # Key.shift_l, Key.shift_r, Key.shift
#     keyboard.press('a')
#     keyboard.release('a')
#
# # 直接输入Hello World
# keyboard.type('Hello World')


## 监听键盘
# from pynput.keyboard import Key, Listener
#
# def on_press(key):
#     # 监听按键
#     print('{0} pressed'.format(key))
#
# def on_release(key):
#     # 监听释放
#     print('{0} release'.format(key))
#     if key == Key.esc:
#         # Stop listener
#         return False
#
# # 连接事件以及释放
# with Listener(on_press=on_press, on_release=on_release) as listener:
#     listener.join()

"""
一个鼠标监听器是一个线程。线程，所有的回调将从线程调用。从任何地方调用pynput.mouse.Listener.stop，或者调用
pynput.mouse.Listener.StopException或从回调中返回False来停止监听器。

对于鼠标来说，api就上面几个。但是对于键盘来说还要别的，详细的查看：http://pythonhosted.org/pynput/index.html
"""