# -*- coding: utf-8 -*-
"""
Created on Sat Jan 13 10:23:38 2018

@author: Brad
"""
import pyautogui as ag
import ctypes

SendInput = ctypes.windll.user32.SendInput
import time


DEFAULT_ACTION_map = {
        'up': 0x16, # U
        'left': 0x23, # H
        'down': 0x24, # J
        'right': 0x25, #K
        'attack': 0x2D, # X
        'use': 0x2C, # Z
        'swap': 0x2E, # C
        'playpause': 0x39,
        'escape': 0x01,
        }

PUL = ctypes.POINTER(ctypes.c_ulong)
class KeyBdInput(ctypes.Structure):
    _fields_ = [("wVk", ctypes.c_ushort),
                ("wScan", ctypes.c_ushort),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]

class HardwareInput(ctypes.Structure):
    _fields_ = [("uMsg", ctypes.c_ulong),
                ("wParamL", ctypes.c_short),
                ("wParamH", ctypes.c_ushort)]

class MouseInput(ctypes.Structure):
    _fields_ = [("dx", ctypes.c_long),
                ("dy", ctypes.c_long),
                ("mouseData", ctypes.c_ulong),
                ("dwFlags", ctypes.c_ulong),
                ("time",ctypes.c_ulong),
                ("dwExtraInfo", PUL)]

class Input_I(ctypes.Union):
    _fields_ = [("ki", KeyBdInput),
                 ("mi", MouseInput),
                 ("hi", HardwareInput)]

class Input(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong),
                ("ii", Input_I)]

def PressKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput( 0, hexKeyCode, 0x0008, 0, ctypes.pointer(extra) )
    x = Input( ctypes.c_ulong(1), ii_ )
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

def ReleaseKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput( 0, hexKeyCode, 0x0008 | 0x0002, 0, ctypes.pointer(extra) )
    x = Input( ctypes.c_ulong(1), ii_ )
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))


class Mouse:
    def toCenter(self):
        w, h = ag.size()
        self.to(w/2, h/2)
    
    def to(self, x, y):
        ag.moveTo(x, y)
    
    def clickCenter(self):
        self.toCenter()
        ag.click()
    
    def clickAt(self, x, y):
        self.to(x, y)
        ag.click()

        
class ActionPad:
    am = None

    def __init__(self, action_map = DEFAULT_ACTION_map):
        self.am = action_map

    def actPress(self, act, interval=0.1, presses=1):
        for i in range(presses):
            PressKey(self.am[act])
            time.sleep(interval)
            ReleaseKey(self.am[act])
            time.sleep(interval)

    def actStart(self, act):
        PressKey(self.am[act])

    def actStop(self, act):
        PressKey(self.am[act])

