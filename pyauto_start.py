# -*- coding: utf-8 -*-
import keyboard as keyb
from time import sleep
import pyautogui, pyperclip
import win32api
import os
import subprocess
import psutil

# import logging.config
# from settings import logger_config

# logging.config.dictConfig(logger_config)
# logger = logging.getLogger('app_logger')


def menu_pusk(name_prog):
    pyautogui.hotkey('Win')
    type(name_prog, 0.2)
    sleep(3)
    pyautogui.keyDown('Enter')

def koordinati():
    keyb.wait('space')
    print (win32api.GetCursorPos())

def paste(text: str):
    pyperclip.copy(text)
    keyb.press_and_release('ctrl + v')


def type(text: str, interval=0.0):
    buffer = pyperclip.paste()
    if not interval:
        paste(text)
    else:
        for char in text:
            paste(char)
            sleep(interval)
    pyperclip.copy(buffer)


def transfer_fanuc():
    pyautogui.leftClick(294, 461)#первая программа
    keyb.press('shift')
    sleep(2)
    pyautogui.leftClick(295, 531)#последняя программа
    keyb.release('shift')
    sleep(2)
    pyautogui.rightClick(295, 531)#контекстн меню
    sleep(2)
    pyautogui.leftClick(354, 550)#uploat
    sleep(2)
    pyautogui.leftClick(374, 654)#yes to all
    sleep(5)
    pyautogui.leftClick(936, 621)# complite
    sleep(6)
    pyautogui.leftClick(1051, 593)
    sleep(1)

def Program_Transfer_Tool():
    os.startfile(r'C:\Program Files (x86)\FANUC\Program Transfer Tool\Bin\PttMain.exe')
    sleep(3)
    keyb.press_and_release('win + up')#full screen

    pyautogui.leftClick(106, 464)#открываем next26
    pyautogui.leftClick(136, 588)#part1
    sleep(2)
    pyautogui.leftClick(1074, 447)#последняя модификация
    sleep(3)
    transfer_fanuc()
    pyautogui.leftClick(136,603) # part2
    sleep(3)
    transfer_fanuc()
    pyautogui.leftClick(28, 463)
    #--------------------------------------
    pyautogui.leftClick(106, 477) # hanhwa
    sleep(3)
    pyautogui.leftClick(92, 510) # part1
    sleep(2)
    transfer_fanuc()
    pyautogui.leftClick(92,528) # part2
    sleep(3)
    transfer_fanuc()
    pyautogui.leftClick(28, 479)
    #--------------------------------------
    pyautogui.leftClick(106, 495) # miano
    sleep(3)
    pyautogui.leftClick(92, 525) # part1
    sleep(2)
    transfer_fanuc()
    pyautogui.leftClick(92, 540) # part2
    sleep(3)
    transfer_fanuc()
    pyautogui.leftClick(28, 496)
    #--------------------------------------
    pyautogui.leftClick(106, 513) # colchester
    sleep(3)
    pyautogui.leftClick(92, 541) # part1
    sleep(2)
    transfer_fanuc()
    pyautogui.leftClick(28, 514)
    #--------------------------------------
    pyautogui.leftClick(106, 549) # nexturn12
    sleep(3)
    pyautogui.leftClick(92, 574) # part1
    sleep(2)
    transfer_fanuc()
    pyautogui.leftClick(92, 591) # part2
    sleep(3)
    transfer_fanuc()
    pyautogui.leftClick(28, 545)
    sleep(3)
    for process in (process for process in psutil.process_iter() if process.name() == "PttMain.exe"):
        process.kill()

def sitizen():
    os.startfile(r'C:\Program Files (x86)\FileControl\FileControl.exe')
    sleep(3)
    pyautogui.leftClick(1220, 340)
    sleep(2)
    pyautogui.leftClick(1102, 351)
    sleep(2)
    pyautogui.leftClick(925, 345)
    sleep(2)
    pyautogui.leftClick(1015, 591)
    sleep(2)
    pyautogui.leftClick(1002, 660)
    sleep(2)
    pyautogui.leftClick(717, 288)
    sleep(2)
    pyautogui.leftClick(767, 334)
    sleep(2)
    pyautogui.leftClick(999, 676)
    sleep(2)
    pyautogui.leftClick(1012, 572)
    sleep(2)
    pyautogui.leftClick(927, 615)
    sleep(40)

    pyautogui.leftClick(1220, 340)
    sleep(2)
    pyautogui.leftClick(1137, 366)
    sleep(2)
    pyautogui.leftClick(943, 338)
    sleep(2)
    pyautogui.leftClick(1096, 599)
    sleep(2)
    pyautogui.leftClick(1096, 599)
    sleep(2)
    pyautogui.leftClick(1023, 579)
    sleep(2)
    pyautogui.leftClick(717, 288)
    sleep(2)
    pyautogui.leftClick(767, 334)
    sleep(2)
    pyautogui.leftClick(999, 676)
    sleep(2)
    pyautogui.leftClick(1012, 572)
    sleep(2)
    pyautogui.leftClick(927, 615)
    sleep(40)
    for process in (process for process in psutil.process_iter() if process.name() == "FileControl.exe"):
        process.kill()

def nomura(x,y,path):
    pyautogui.leftClick(1914, 1067)
    pyautogui.doubleClick(719, 974,button='LEFT')
    keyb.press_and_release('win + up')  # full screen
    sleep(5)
    pyautogui.doubleClick(x, y, button='LEFT')#координаты папки
    for x in range(4):
        pyautogui.doubleClick(214, 126,button='LEFT')
        sleep(1)
    sleep(10)
    pyautogui.leftClick(214, 126)  # первая программа
    keyb.press('shift')
    sleep(1)
    pyautogui.leftClick(228, 356)  # последняя программа
    keyb.release('shift')
    sleep(1)
    keyb.press_and_release('ctrl + c')
    sleep(1)
    os.startfile(path)
    keyb.press_and_release('win + up')  # full screen
    sleep(1)
    keyb.press_and_release('ctrl + v')
    sleep(3)
    pyautogui.leftClick(760, 712)
    sleep(1)
    pyautogui.leftClick(860, 462)
    sleep(20)
    pyautogui.leftClick(1898, 5)
    pyautogui.leftClick(1898, 5)
    sleep(10)


# ***********************************************************************
# -----------------------------------------------------------------------
#
def main():
    # koordinati()
    nomura(214, 126,r'C:\Users\Programmer\Desktop\pro\STANKI\nomura20-1')
    nomura(221, 155, r'C:\Users\Programmer\Desktop\pro\STANKI\nomura20-2')
    nomura(234, 174, r'C:\Users\Programmer\Desktop\pro\STANKI\nomura20-3')
    nomura(231, 197, r'C:\Users\Programmer\Desktop\pro\STANKI\nomura10')
    Program_Transfer_Tool()
    sitizen()

# -----------------------------------------------------------------------
if __name__ == '__main__':
    main()
