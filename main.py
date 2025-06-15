import csv
import os
import time

from datetime import datetime
from random import randint

from dotenv import load_dotenv

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait  # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC  # available since 2.26.0
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options


class InvoiceUploader:
    def __init__(self):
        load_dotenv()
        
        self.mdir = os.getenv('MDIR')
        
        
        self.main_menu = {1 : ['LAUNCH BOT', 'self.start_upload'],
                          2: ['OPEN DIR', self.open_mdir],
                          0: ['QUIT', exit],
                          }


    def start_menu(self):
        while True:
            print('----- MAIN MENU ------')
            for k, v in self.main_menu.items():
                print('{}: {}'.format(k, v[0]))
            user_input = input('Please enter index to select:\n')
            try:
                self.main_menu[int(user_input)][1]()
            except Exception as e:
                print(e)

    def open_mdir(self):
        os.startfile(os.path.join(self.mdir))
        return


def main():
    iu = InvoiceUploader()
    iu.start_menu()

if __name__ == '__main__':
    main()
    
    