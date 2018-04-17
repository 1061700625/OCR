# coding:utf-8

import pyperclip
import os
import time
from PIL import Image,ImageGrab
import subprocess
from aip import AipOcr
# import urllib
# import urllib3
# from bs4 import BeautifulSoup
# import requests
# import re
# import ssl
# import shutil
# import pyHook
# import sys
# import base64
# import pythoncom
# import threading
# import ctypes
# import inspect
# from win32api import GetSystemMetrics as gsm
# import pytesseract
# https不提示警告信息
# from requests.packages import urllib3
# urllib3.disable_warnings()
# from urllib import request
# ssl._create_default_https_context = ssl._create_unverified_context


# ################################强制关闭进程##################################################
# def _async_raise(tid, exctype):
#     """raises the exception, performs cleanup if needed"""
#     tid = ctypes.c_long(tid)
#     if not inspect.isclass(exctype):
#         exctype = type(exctype)
#     res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
#     if res == 0:
#         raise ValueError("invalid thread id")
#     elif res != 1:
#         # """if it returns a number greater than one, you're in trouble,
#         # and you should call it again with exc=NULL to revert the effect"""
#         ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
#         raise SystemError("PyThreadState_SetAsyncExc failed")
# def stop_thread(thread):
#     _async_raise(thread.ident, SystemExit)
# ###############################################################################################

#**********图片处理********************
def vcode2str(img_url):
    """ 你的 APPID AK SK """
    APP_ID = ''
    API_KEY = ''
    SECRET_KEY = ''
    client = AipOcr(APP_ID, API_KEY, SECRET_KEY)
    # """ 读取图片 """
    def get_file_content(filePath):
        with open(filePath, 'rb') as fp:
            return fp.read()
    # image = get_file_content('YZM.jpg')
    image = get_file_content(img_url)
    """ 调用通用文字识别, 图片参数为本地图片 """
    client.basicGeneral(image);
    """ 如果有可选参数 """
    options = {}
    options["language_type"] = "CHN_ENG"
    options["detect_direction"] = "false"
    options["detect_language"] = "false"
    options["probability"] = "false"
    """ 带参数调用通用文字识别, 图片参数为本地图片 """
    a=client.basicGeneral(image, options)
    length = len(a['words_result'])
    b = ""
    for i in range(length):
        b = b + a['words_result'][i]["words"]
    print("图片文本: " + b)
    with open("original.txt",'w+') as fp:
        fp.write(b)
        print("文字识别部分已保存到本地")
        fp.close()
    return b

    # url = "http://218.64.56.18/jsxsd/verifycode.servlet?t=0.5995165859560846"
    # """ 调用通用文字识别, 图片参数为远程url图片 """
    # client.basicGeneralUrl(url);
    # """ 如果有可选参数 """
    # options = {}
    # options["language_type"] = "CHN_ENG"
    # options["detect_direction"] = "true"
    # options["detect_language"] = "true"
    # options["probability"] = "true"
    # """ 带参数调用通用文字识别, 图片参数为远程url图片 """
    # a=client.basicGeneralUrl(url, options)
    # print(a)

#**********翻译部分********************
def fanyi(query):
    import http.client
    import hashlib
    import urllib
    import random
    import json
    appid = ''
    secretKey = ''
    httpClient = None
    myurl = '/api/trans/vip/translate'
    q = query
    fromLang = 'auto'
    toLang = 'zh'
    salt = random.randint(32768, 65536)

    sign = appid + q + str(salt) + secretKey
    m1 = hashlib.md5()
    m1.update(sign.encode())
    sign = m1.hexdigest()
    myurl = myurl + '?appid=' + appid + '&q=' + urllib.parse.quote(
        q) + '&from=' + fromLang + '&to=' + toLang + '&salt=' + str(salt) + '&sign=' + sign
    # print(urllib.parse.quote(q))
    try:
        httpClient = http.client.HTTPConnection('api.fanyi.baidu.com')
        httpClient.request('GET', myurl)
        # response是HTTPResponse对象
        response = httpClient.getresponse()
        html = response.read()  # bytes
        # print("html:  ",type(html),html)
        html_str = html.decode()  # bytes to str
        # print("html_str:  ",type(html_str),html_str)
        html_dict = json.loads(html_str)  # str to dict
        # print("html_dist:  ",type(html_dict),html_str)
        result_ori = html_dict["trans_result"][0]["src"]
        result_tar = html_dict["trans_result"][0]["dst"]
        # print(result_ori, " --> ", result_tar)
        print("*"*100)
        print("翻译文本: " + result_tar)
        with open("original.txt", 'a+') as fp:
            fp.write("\r\n"+"*" * 100+"\r\n")
            fp.write(result_tar)
            print("翻译部分已保存到本地")
            fp.close()
            try:
                fnull = open(os.devnull, 'w')
                return1 = subprocess.call('taskkill /f /t /im notepad.exe', shell=True, stdout=fnull, stderr=fnull)
            except:
                pass
            os.startfile(os.path.join(os.getcwd(), r'original.txt'))
    except Exception as e:
        print(e)
    finally:
        if httpClient:
            httpClient.close()

# #**********调用微信dll截图********************
# def capture():
#     import ctypes
#     try:
#         dll = ctypes.cdll.LoadLibrary('PrScrn.dll')
#     except Exception as e:
#         print("Dll load error: ")
#         print(e)
#         return
#     else:
#         try:
#             dll.PrScrn(0)
#         except:
#             print("Sth wrong in capture!")
#             return

# old_x, old_y = 0, 0
# new_x, new_y = 0, 0
# def onMouseEvent(event):
#     global old_x, old_y, new_x, new_y, hm2
#     if event.MessageName == "mouse left down":
#         old_x, old_y = event.Position
#     if event.MessageName == "mouse left up":
#         new_x, new_y = event.Position
#         # 解除事件绑定
#         hm2.UnhookMouse()
#         hm2 = None
#         image = ImageGrab.grab((old_x, old_y, new_x, new_y))
#         image.save('ocr.png')
#     return True

# #**********监听键盘事件************
# input_time_last = 0
# down_num = 0
# def onKeyboardEvent(event):
#     global down_num
#     global input_time_last
#     input_data = str(event.Key)
#     print(input_data)
#     if input_data == 'Lcontrol':
#         down_num = down_num + 1
#         print('down_num: ', down_num)
#         if down_num == 1:  #第一次按下时的时间
#             input_time_last = int(round(time.time() * 1000))
#         if down_num >= 2:  #第二、三次按下的情况
#             input_time_cur = int(round(time.time() * 1000))
#             input_time_det = input_time_cur - input_time_last
#             input_time_last = input_time_cur
#             print('Det time: ', input_time_det)
#             if input_time_det > 500:  #间隔大于500ms，则为无效
#                 down_num = 1
#                 return True
#             elif input_time_det <= 500 and down_num >= 3:  #两次间隔均小于500ms，则截图
#                 down_num = 0
#                 # capture()
#                 mousehook_thread.start()
#                 while main_thread.isAlive():
#                     try:
#                         stop_thread(main_thread)
#                         time.sleep(1)
#                         print("stop_thread(main_thread)")
#                     except Exception as e:
#                         print(e)
#                     print("start_thread.isAlive?  ", main_thread.isAlive())
#                 main_thread.start()
#     return True
#     # 返回 True 表示响应此事件，False表示拦截

# def keyhook():
#     hm = pyHook.HookManager()
#     hm.KeyDown = onKeyboardEvent
#     hm.HookKeyboard()
#     pythoncom.PumpMessages()
# def mousehook():
#     global hm2
#     hm2 = pyHook.HookManager()
#     hm2.MouseAllButtons = onMouseEvent
#     hm2.HookMouse()
#     pythoncom.PumpMessages()

def main():
    im = ImageGrab.grabclipboard()
    if 'image' in str(im):
        print(im)
        pyperclip.copy(None)
        im.save("ocr.png")
        img_path = os.path.join(os.getcwd(), "ocr.png")
        content = vcode2str(img_path)
        fanyi(content)
        os.remove(img_path)
        time.sleep(2)
    else:
        print("请检查是否正确截图后重试!")

import win32con,win32gui
import win32clipboard as cb
class MyWindow():         #剪切板监听
    def __init__(self):
        #注册一个窗口类
        wc = win32gui.WNDCLASS()
        wc.lpszClassName = 'MyWindow'
        wc.hbrBackground = win32con.COLOR_BTNFACE+1
        wc.lpfnWndProc = self.wndProc
        class_atom=win32gui.RegisterClass(wc)
        #创建窗口
        self.hwnd = win32gui.CreateWindow( class_atom, u'OCR',
                                           win32con.WS_OVERLAPPEDWINDOW,
                                           win32con.CW_USEDEFAULT,
                                           win32con.CW_USEDEFAULT,
                                           win32con.CW_USEDEFAULT,
                                           win32con.CW_USEDEFAULT, 0,0, 0, None)
        # 显示窗口
        # win32gui.ShowWindow(self.hwnd, win32con.SW_SHOWNORMAL)
    #消息处理
    def wndProc(self, hwnd, msg, wParam, lParam):
        if msg == win32con.WM_DESTROY:
            win32gui.PostQuitMessage(0)
        if msg == win32con.WM_DRAWCLIPBOARD: #当剪切板更新的时候收到这个消息
            main()
            return win32gui.DefWindowProc(hwnd, msg, wParam, lParam)

if __name__ == '__main__':
    print('      *** 使用前请先保存并关闭记事本! ***')
    print('使用说明：\r\n\t1、登陆QQ，任意界面按下Ctrl+Alt+F，则触发截图；\r\n\t2、选择区域后按‘√’。')
    print('*'*50)
    # keyhook_thread = threading.Thread(target=keyhook)
    # mousehook_thread = threading.Thread(target=mousehook)
    # main_thread = threading.Thread(target=main)
    # main_thread.start()
    # main_thread.join()
    # keyhook_thread.start()
    # keyhook_thread.join()
    mw = MyWindow()
    cb.SetClipboardViewer(mw.hwnd) #注册为剪切板监听窗口
    win32gui.PumpMessages()






