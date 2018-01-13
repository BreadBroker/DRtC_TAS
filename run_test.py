# -*- coding: utf-8 -*-
"""
Created on Sat Jan 13 10:44:26 2018

@author: Brad
"""

from DRtC_TAS import DRtC_TAS
from time import sleep

def main():
    bot = DRtC_TAS()
    bot.open_game()
    bot.pad.actPress('attack', presses=3)
    bot.pad.actPress('right', presses=1)
    bot.pad.actPress('attack', presses=1)
    bot.pad.actPress('attack', presses=200, interval=0.25)


if __name__ == '__main__':
    main()