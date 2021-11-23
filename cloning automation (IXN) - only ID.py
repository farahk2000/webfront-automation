# -*- coding: utf-8 -*-
"""
Created on Tue Oct 12 14:48:15 2021

@author: farah
"""
import time
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

import pandas as pd 
import numpy as np


#import carrier data 
df = pd.read_csv('C:/Users/farah/Desktop/Finaeo - BA Intern/Automation test iA Products - Sheet1.csv')
#print (df)

PATH = r'C:\Users\farah\Desktop\chromedriver_win32\chromedriver.exe'
password = 'Farah533932'
email = 'farah.khan@finaeo.com'
opt = Options()
#added option to run tests on same window (otherwise it opens new test window every run)
# CMD steps: 
# 1. C:\Users\farah>cd C:\Program Files (x86)\Google\Chrome\Application
# 2. C:\Program Files (x86)\Google\Chrome\Application>chrome.exe --remote-debugging-port=9000 
    # --user-data-dir=C:\Users\farah\Documents\farahchromeprofile
opt.add_experimental_option('debuggerAddress', 'localhost:9000')

driver = webdriver.Chrome(executable_path=PATH, options= opt)
#maximizing window
driver.maximize_window()

def cloning_process():
    for n in range(len(df.index)):
        #print('product number ' , df.index[n] , ' is' , df['productname'][n])
        driver.get('https://admin.finaeo.ca/product/498/ia/37')
        #find the clone button after loading
        input = WebDriverWait(driver, 10).until(
             EC.element_to_be_clickable((By.XPATH, '//*[@id="root"]/div[2]/div[3]/div/div[1]/div/div[2]/div/div[2]/div'))
         )
        input.click()
        #driver.find_element_by_class_name('MuiButtonBase-root MuiIconButton-root MuiIconButton-colorPrimary')
        
        #for confirm clone pop-up --> click yes
        input = WebDriverWait(driver, 10).until(
             EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/div[3]/div/div[3]/button[2]'))
         )
        input.click()
        
        driver.implicitly_wait(30)
        #new input in name (Product name)
        WebDriverWait(driver, 10).until(
            EC.url_changes('https://admin.finaeo.ca/product/498/ia/37'))
        #new input in name (Product name)
        name = WebDriverWait(driver, 10).until(
             EC.element_to_be_clickable((By.XPATH, '//*[@id="nameEn"]'))
         )
        name.click()
        name.send_keys(Keys.CONTROL + 'a') 
        name.send_keys(df['productname'][n])
        
        #new input in quote (Quote Refrence)
        quote = driver.find_element_by_xpath('//*[@id="quoteRef"]')
        quote.send_keys(Keys.CONTROL + 'a') 
        quote.send_keys(str(df['productid'][n]))
        #click save button
        input = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="root"]/div[2]/div[3]/div/div[5]/div/div[1]/div/div[2]/div[20]/div/div/div/div/button'))
             )
        input.click()
        
        #click on features tab 
        driver.find_element_by_xpath('//*[@id="root"]/div[2]/div[3]/div/div[3]/div/div/div/div/button[7]').click()
        #new input into term value
        #non-unique ID's into list and then index to the one needed (may change with permanent and CI products)
         
        ids = driver.find_elements_by_xpath('//*[@id="value"]')
        term = ids[9]
        term.send_keys(Keys.CONTROL + 'a')
        term.send_keys(str(df['productterm'][n]))
         #new input into term text
        text_ids = driver.find_elements_by_xpath('//*[@id="text"]')
        term_text = text_ids[16]
        term_text.send_keys(Keys.CONTROL + 'a')
        term_text.send_keys('Term ' + str(df['productterm'][n]))
        try:
            #click save button 
            input = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="root"]/div[2]/div[3]/div/div[5]/div/div[17]/div/div[8]/div/div/div/div/button'))
                 )
            input.click()
        except: 
            pass
         #go back to the product info and flows tab
        driver.find_element_by_xpath('//*[@id="root"]/div[2]/div[3]/div/div[3]/div/div/div/div/button[1]').click()
         
        print("product", df.index[n], "created")
        #restart the program for rest of the products
        
cloning_process()