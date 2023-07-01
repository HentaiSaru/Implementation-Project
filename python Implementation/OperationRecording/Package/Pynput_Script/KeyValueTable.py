from pynput import keyboard
import win32con

#Todo - 鍵值表 -

class PynputKey:
    Keytable = {
        "Ctrl" : keyboard.Key.ctrl_l,
        "Alt" : keyboard.Key.alt_l,
        "Shift" : keyboard.Key.shift_l,
        "F1" : keyboard.Key.f1,
        "F2" : keyboard.Key.f2,
        "F3" : keyboard.Key.f3,
        "F4" : keyboard.Key.f4,
        "F5" : keyboard.Key.f5,
        "F6" : keyboard.Key.f6,
        "F7" : keyboard.Key.f7,
        "F8" : keyboard.Key.f8,
        "F9" : keyboard.Key.f9,
        "F10" : keyboard.Key.f10,
        "F11" : keyboard.Key.f11,
        "F12" : keyboard.Key.f12,
    }

class Win32Key:
    MouseKT_D = {
        "left" : win32con.MOUSEEVENTF_LEFTDOWN,
        "right" : win32con.MOUSEEVENTF_RIGHTDOWN,
        "middle" : win32con.MOUSEEVENTF_MIDDLEDOWN,
        "1" : win32con.MOUSEEVENTF_WHEEL,
        "-1" : win32con.MOUSEEVENTF_WHEEL,
    }

    MouseKT_U = {
        "left" : win32con.MOUSEEVENTF_LEFTUP,
        "right" : win32con.MOUSEEVENTF_RIGHTUP,
        "middle" : win32con.MOUSEEVENTF_MIDDLEUP,
    }

    KeyboardKT = {
        "tab" : win32con.VK_TAB,
        "enter" : win32con.VK_RETURN,
        "space" : win32con.VK_SPACE,
        "backspace" : win32con.VK_BACK,
        "caps_lock": win32con.VK_CAPITAL,
        "ctrl_l" : win32con.VK_LCONTROL,
        "ctrl_r" : win32con.VK_RCONTROL,
        "alt_l" : win32con.VK_LMENU,
        "alt_r" : win32con.VK_RMENU,
        "shift" : win32con.VK_SHIFT,
        "shift_l" : win32con.VK_LSHIFT,
        "shift_r" : win32con.VK_RSHIFT,
        "up" : win32con.VK_UP,
        "left" : win32con.VK_LEFT,
        "right" : win32con.VK_RIGHT,
        "down" : win32con.VK_DOWN,
        "f1" : win32con.VK_F1,
        "f2" : win32con.VK_F2,
        "f3" : win32con.VK_F3,
        "f4" : win32con.VK_F4,
        "f5" : win32con.VK_F5,
        "f6" : win32con.VK_F6,
        "f7" : win32con.VK_F7,
        "f8" : win32con.VK_F8,
        "f9" : win32con.VK_F9,
        "f10" : win32con.VK_F10,
        "f11" : win32con.VK_F11,
        "f12" : win32con.VK_F12,
        "96" : win32con.VK_NUMPAD0,
        "97" : win32con.VK_NUMPAD1,
        "98" : win32con.VK_NUMPAD2,
        "99" : win32con.VK_NUMPAD3,
        "100" : win32con.VK_NUMPAD4,
        "101" : win32con.VK_NUMPAD5,
        "102" : win32con.VK_NUMPAD6,
        "103" : win32con.VK_NUMPAD7,
        "104" : win32con.VK_NUMPAD8,
        "105" : win32con.VK_NUMPAD9,
    }