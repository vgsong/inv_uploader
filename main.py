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


class WO:
    def __init__(self, cc, invnum, invamt, contract, contact, date):
        self.cc = cc
        self.invnum =invnum
        self.invamt = invamt
        self.contract = contract
        self.contact = contact
        self.date = date
        
        
class InvoiceUploader:
    def __init__(self):
        load_dotenv()
        
        self.mdir = os.getenv('MDIR')
        self.data_dir = os.path.join(self.mdir, 'data')
        self.wo_filename = 'wo.csv'
        
        self.webdriver_dir = os.getenv('GECKO_DIR')
        self.firefox_binary_location = os.getenv('FIREFOX_BDIR')
        
        self.portal_url = os.getenv('PORTAL_URL')
        self.portal_username = os.getenv('PORTAL_USERNAME')
        self.portal_password = os.getenv('PORTAL_PASSWORD')        

        self.wo = None
        self.driver = None
        self.time_stamp = datetime.now()
        
        self.main_menu = {1 : ['LAUNCH BOT', self.start_upload],
                          2 : ['OPEN DIR', self.open_mdir],
                          3 : ['REFRESH WO', self.load_wo],
                          0 : ['QUIT', exit],
                          }
        
        self.portal_mapping = {'username_textbox':'',
                               'loginnext_button':'',
                               'password_textbox':'',
                               'signin_button':'',
                               }
        
        self.load_wo()
        
    def start_upload(self):
        
        def start_webdriver():
            print('Launching uploader')
            o = Options()
            s = Service(os.path.join(self.webdriver_dir))
            o.binary_location = self.firefox_binary_location
            self.driver = webdriver.Firefox(service=s, options=o)
            time.sleep(3)
        
        def portal_login():
            self.driver.get(self.portal_url)
            print('logging into portal...')
            time.sleep(5)
            # get DOM element using xpath to get username textbox
            self.driver.find_element(By.XPATH,self.portal_mapping['username_textbox']).send_keys(self.portal_username)
            time.sleep(1.5)
            
            #initial login needs time to load the JScript as well since the username > next > password login screen update
            # self.driver.find_element(By.XPATH,self.ariba_xpath_mapping['loginnext_button']).send_keys(f'\n')
            self.driver.find_element(By.XPATH,self.portal_mapping['loginnext_button']).click()
            time.sleep(2)
            
            # get DOM element using xpath to get password textbox
            self.driver.find_element(By.XPATH, self.portal_mapping['password_textbox']).send_keys(self.portal_password)
            time.sleep(0.5)
            
            # get DOM element using xpath to click on login button
            self.driver.find_element(By.XPATH, self.portal_mapping['signin_button']).click()
            time.sleep(3)
            # ariba_logged.switch_to.window(ariba_logged.window_handles[2])
            return
                
        # start_webdriver()
        # portal_login()
        total_wo = len(self.wo)
        print('Uploading {} invoice(s)'.format(total_wo))
            
        for i, x in enumerate(self.wo):
            count = i + 1
            upload_step = i + 1
            wo = WO(x[0],x[1],x[2], x[3],x[4], x[5])
            
            try:
                print(x[2])
                print('Uploading {} out of  {}\n'.format(count, total_wo))
                print('{} for contract {}'.format(wo.invnum, wo.contract))
                time.sleep(2)
                
                
                
            except Exception as e:
                print(e)
                
                continue
        return

        

    
    def open_mdir(self):
        os.startfile(os.path.join(self.mdir))
        return
    
    def load_wo(self):
        result = []
        with open(os.path.join(self.data_dir, self.wo_filename), 'r', encoding='utf-8') as cf:
            data = csv.reader(cf)
            for x in list(data)[1:]:
                result.append(x)
        self.wo = result
        print('{} wo loaded!'.format(len(self.wo)))
        return

    def start_menu(self):
        while True:
            
            print('wo loaded: {}'.format(len(self.wo)))
            print('Hello! Today is {}'.format(self.time_stamp.strftime('%Y %m %d')))
            
            print('----- MAIN MENU ------')
            for k, v in self.main_menu.items():
                print('{}: {}'.format(k, v[0]))
            
            user_input = input('Please enter index to select:\n')
            try:
                self.main_menu[int(user_input)][1]()
            except Exception as e:
                print(e)
                



def main():
    iu = InvoiceUploader()
    iu.start_upload()

if __name__ == '__main__':
    main()
    
    