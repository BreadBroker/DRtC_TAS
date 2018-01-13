# -*- coding: utf-8 -*-
"""
Created on Sat Jan 13 10:27:12 2018

@author: BreadBroker
"""

import logging
import os
import win32com.client
from WindowMgr import WindowMgr
from time import sleep
from DRtC_Inputs import Mouse, ActionPad

DEFAULT_LOG_appname = 'DRtC_TAS'
DEFAULT_LOG_dbname = 'DRtC_TAS.dbg'
DEFAULT_LOG_infname = 'DRtC_TAS.log'
DEFAULT_LOG_formatter = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

DEFAULT_APP_loc = 'E:\\Program Files (x86)\\Steam\\steamapps\\common\\DeathRoadToCanada\\'
DEFAULT_APP_name = 'prog.exe'
class DRtC_TAS():
    
    logger = None
    app = None
    logger_handlers = []
    CWD = ''
    wmgr = None
    mouse = None
    pad = None
    
    def __init__(self):
        self.logger = self.init_logs()
        self.logger.info("DRtC-bot STARTED")
        self.logger.debug("DRtC-bot DEBUG STARTED")
        self.CWD = os.getcwd()
        self.wmgr = WindowMgr()
        self.mouse = Mouse()
        self.pad = ActionPad()

    def init_logs(self, appname=DEFAULT_LOG_appname, dbname=DEFAULT_LOG_dbname,
                  infname=DEFAULT_LOG_infname,
                  formatter=DEFAULT_LOG_formatter):
        """initialize logfiles"""
        logger = logging.getLogger(appname)
        logger.setLevel(logging.DEBUG)
        db_logger = logging.FileHandler(dbname)
        db_logger.setLevel(logging.DEBUG)
        info_logger = logging.FileHandler(infname)
        info_logger.setLevel(logging.INFO)
        str_logger = logging.StreamHandler()
        str_logger.setLevel(logging.INFO)
        formatter = logging.Formatter(formatter)
        db_logger.setFormatter(formatter)
        info_logger.setFormatter(formatter)
        str_logger.setFormatter(formatter)
        logger.addHandler(db_logger)
        logger.addHandler(info_logger)    
        logger.addHandler(str_logger)
        self.logger_handlers.append(db_logger)
        self.logger_handlers.append(info_logger)
        self.logger_handlers.append(str_logger)
        return logger
    
    def close_logs(self):
        for handler in self.logger_handlers:
            handler.close()
        self.logger_handlers = []
        self.logger.handlers = []
        self.logger=None
    
    def open_game(self, loc=DEFAULT_APP_loc, name=DEFAULT_APP_name):
        self.logger.debug('OPENING APP %s IN LOCATION %s' % (name, loc))
        os.chdir(loc)
        self.app = win32com.client.Dispatch('WScript.Shell')
        self.app.Run(name)
        sleep(2) 
        self.app.AppActivate(name)
        self.mouse.clickCenter()
        os.chdir(self.CWD)
        return self.app

    def close_game(self, app=None):
        self.logger.debug("TRYING TO KILL PROCESS IN APPFIELD")
        self.pad.actPress("escape")
        sleep(1)
        self.pad.actPress("attack")
        sleep(1)
        self.pad.actPress("right")
        sleep(1)
        self.logger.info("APP CLOSED")

    def stop(self):
        self.close_game()
        self.close_logs()