import win32gui
import win32api
import win32ui
import win32con
import numpy as np
import time
import threading

class WindowInfo:
    x = 0
    y = 0
    cached_x = 0
    cached_y = 0
    width = 0
    height = 0
    content_width = 0
    content_height = 0
    border_size = 8
    titlebar_size = 31
    offset_x = border_size
    offset_y = titlebar_size
    hwnd = 0
    hidden = False
    wDc = None
    dcObj = None
    cDC = None

    def __init__(self) -> None:
        self.hwnd = win32gui.FindWindow(None, 'Chiaki | Stream')
        if self.hwnd == 0:
            return
        windows_rect = win32gui.GetWindowRect(self.hwnd)
        self.x = windows_rect[0]
        self.y = windows_rect[1]
        self.width = windows_rect[2] - windows_rect[0]
        self.height = windows_rect[3] - windows_rect[1]
        self.border_size = int((self.width - 1280) * 0.5)
        self.titlebar_size = int(self.height - 720 - self.border_size)
        self.content_width = self.width - (self.border_size * 2)
        self.content_height = self.height - self.titlebar_size - self.border_size

        self.wDC = win32gui.GetWindowDC(self.hwnd)
        self.dcObj = win32ui.CreateDCFromHandle(self.wDC)
        self.cDC = self.dcObj.CreateCompatibleDC()
        self.lock = threading.Lock()
    
    def is_active(self) -> int:
        return self.hwnd > 0

    def __del__(self) -> None:
        if self.hwnd > 0:
            self.dcObj.DeleteDC()
            self.cDC.DeleteDC()
            win32gui.ReleaseDC(self.hwnd, self.wDC)     

    def grab(self, rect) -> np.ndarray:
        self.lock.acquire()
        try:
            dataBitMap = win32ui.CreateBitmap()
            dataBitMap.CreateCompatibleBitmap(self.dcObj, rect['width'], rect['height'])
            self.cDC.SelectObject(dataBitMap)
            self.cDC.BitBlt((0,0),(rect['width'], rect['height']) , self.dcObj, (self.offset_x + rect['left'], self.offset_y + rect['top']), win32con.SRCCOPY)
            signedIntsArray = dataBitMap.GetBitmapBits(True)
            img = np.fromstring(signedIntsArray, dtype='uint8')
            img.shape = (rect['height'], rect['width'], 4)

            win32gui.DeleteObject(dataBitMap.GetHandle())
        finally:
            self.lock.release()
            return img

    def save(self, rect, name):
        dataBitMap = win32ui.CreateBitmap()
        dataBitMap.CreateCompatibleBitmap(self.dcObj, rect['width'], rect['height'])
        self.cDC.SelectObject(dataBitMap)
        self.cDC.BitBlt((0,0),(rect['width'], rect['height']) , self.dcObj, (self.offset_x + rect['left'], self.offset_y + rect['top']), win32con.SRCCOPY)
        dataBitMap.SaveBitmapFile(self.cDC, name)
        win32gui.DeleteObject(dataBitMap.GetHandle())
    
    def key_click(self, key, sleep):
        win32api.SendMessage(self.hwnd, win32con.WM_KEYDOWN, key, 0)
        time.sleep(0.1)
        win32api.SendMessage(self.hwnd, win32con.WM_KEYUP, key, 0)
        time.sleep(sleep)
    
    def key_press(self, key, duration):
        win32api.SendMessage(self.hwnd, win32con.WM_KEYDOWN, key, 0)
        time.sleep(duration)
        win32api.SendMessage(self.hwnd, win32con.WM_KEYUP, key, 0)

    def key_down(self, key):
        win32api.SendMessage(self.hwnd, win32con.WM_KEYDOWN, key, 0)

    def key_up(self, key):
        win32api.SendMessage(self.hwnd, win32con.WM_KEYUP, key, 0)