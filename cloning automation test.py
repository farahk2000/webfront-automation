# -*- coding: utf-8 -*-
"""
Created on Fri Aug 27 14:48:29 2021

@author: farah
"""

import pandas as pd 
import numpy as np

#import carrier data 
df = pd.read_csv('C:/Users/farah/Desktop/Finaeo - BA Intern/Automation test iA Products - Sheet1.csv')
#print (df)

#remove products that are already on the platform (yes under 'on platform')
df = df[df.onplatform == 'No']
df = df.reset_index(drop=True)
#display the entire dataframe lol idk why i like to see 
pd.set_option("display.max_rows", None, "display.max_columns", None)
#print(df)

#remove insurance from name to extract term value
df['productname']= df['productname'].str.replace('Insurance ','')
# create new column with term value 
df['productterm'] = df.productname.str.split().apply(lambda x: x[1]).astype(int)

print(df['productterm'])
#rounded the term to the nearst 5 value (makes the most sense when filtering)
df['productterm']=(np.around(df.productterm.values/5, decimals=0)*5).astype(int)
print(df['productterm'])

#cleaned and organized df

#automated cloning of products - Finaeo
import pyautogui
import pywinauto
from pywinauto.application import Application
from pywinauto.keyboard import send_keys
from pywinauto import keyboard as kb
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from chromedriver_py import binary_path # this will get you the path variable

# xpathsearch = '/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input'
# searchinput = driver.find_element_by_xpath(xpathsearch)

# searchinput.send_keys('https://admin.finaeo.ca/carrier-selection')
# searchinput.send_keys(Keys.ENTER)
PATH = r'C:\Users\farah\Desktop\chromedriver_win32\chromedriver.exe'

button= '//*[@id="root"]/div[2]/div[3]/div/div/div[2]/div/button'
//*[@id="identifierNext"]/div/button
//*[@id="passwordNext"]/div/button
//*[@id="root"]/div[2]/div[3]/div/div/div[2]/div/div[10]/div

from pyotp import *
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

opt = Options()
opt.add_experimental_option('debuggerAdress', 'localhost:9000')

driver = webdriver.Chrome(executable_path=PATH, chrome_options=opt)
driver.get("https://accounts.google.com/signin/v2/identifier?hl=en&passive=true&continue=https%3A%2F%2Fwww.google.com%2F&ec=GAZAmgQ&flowName=GlifWebSignIn&flowEntry=ServiceLogin")

gmail_sign_in('farah.khan@finaeo.com', 'Farah533932')

def gmail_sign_in(email, password):
    driver = webdriver.Chrome(executable_path=PATH, chrome_options= opt)
    #maximizing window
    driver.maximize_window()
    #opeining the link in the test environment
    driver.get('https://admin.finaeo.ca/carrier-selection')
    #click the login by google button
    driver.find_element_by_xpath('//*[@id="root"]/div[2]/div[3]/div/div/div[2]/div/div/button').click()
    #insert email
    driver.find_element_by_xpath('//*[@id="identifierId"]').send_keys(email)
    #next
    input = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="identifierNext"]/div/button'))
    )
    input.click()

    driver.implicitly_wait(1)
    #input password
    driver.find_element_by_xpath('//*[@id="password"]/div[1]/div/div[1]/input').send_keys(password)
    #next
    input = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="passwordNext"]/div/button'))
    )
    input.click()
    driver.implicitly_wait(10)
    driver.get('https://admin.finaeo.ca/carrier-selection')
    
    # wait for the 2FA to be run on the phone manually, then the program should identify the 'carrier button' 
    try:
        input = WebDriverWait(driver,30).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="root"]/div[2]/div[3]/div/div/div[2]/div/div[10]/div'))
        )
        input.click()
    except: 
        driver.find_element_by_partial_link_text('Industrial Alliance')
    else: 
        driver.close()
        print ('closed when trying to click the industiral alliance carrier')
    #click the 'product' button OR create a new link to the exact product family that you need to work on 
    try: 
        driver.find_element_by_xpath('//*[@id="root"]/div[2]/div[3]/div/div[4]/div/div/div/div/div[3]/a').click()
    except: 
        driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + 't') 
        driver.get('https://admin.finaeo.ca/product-family/37/ia')
    else: 
        driver.close()
        print('closed when trying to get to the product family link')
    
    #driver.find_element_by_link_text('Pick-A-Term')
    
    #clicking under the products tab 
    input = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="root"]/div[2]/div[3]/div/div[2]/div/div/div/div/button[4]'))
    )
    input.click()
    # clicking on the product OR you can also use the link that it is redirecting to 
    driver.find_element_by_xpath('//*[@id="root"]/div[2]/div[3]/div/div[4]/div/div[2]/div/div[1]/div/div[1]/a').click()
    #driver.find_element_by_link_text('Product 1: Pick-A-Term Insurance: Term 10 - 50% Decreasing')
    
    for n in range(len(df.index)):
        #print('product number ' , df.index[n] , ' is' , df['productname'][n])
    #find the clone button after loading
        input = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="root"]/div[2]/div[3]/div/div[1]/div/div[2]/div/div[2]/div'))
        )
        input.click()
    
    #driver.find_element_by_class_name('MuiButtonBase-root MuiIconButton-root MuiIconButton-colorPrimary')
    
    #for confirm clone pop-up --> click yes
        input = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="root"]/html/body/div[2]/div[3]/div/div[3]/button[2]'))
        )
        input.click()
    
    #new input in name (Product name)
        name = driver.find_element_by_xpath('//*[@id="nameEn"]')
        name.clear()
        name.send_keys(df['productname'][n])
    #new input in quote (Quote Refrence)
        quote = driver.find_element_by_xpath('//*[@id="quoteRef"]')
        quote.clear()
        quote.send_keys(df['productid'][n])
    #click save button
        input = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="root"]/div[2]/div[3]/div/div[5]/div/div[1]/div/div[2]/div[20]/div/div/div/div/button'))
            )
        input.click()
    #eligiblity tab
        driver.find_element_by_xpath('//*[@id="root"]/div[2]/div[3]/div/div[3]/div/div/div/div/button[6]').click()
    #enter value from malelowage smoker and malehighagesmoker
        min_age = driver.find_element_by_id('min')
        min_age.clear()
        min_age.send_keys(df['maleLowAgeSmoker'][n])
        
        max_age = driver.find_element_by_id('max')
        max_age.clear()
        max_age.send_keys(df['maleHighAgeSmoker'][n])
    # enter value mentioned before but add the word "to" in between
        age_text = driver.find_element_by_id('textEn')
        age_text.clear()
        age_text.send_keys(str(df['maleLowAgeSmoker'][n]) + ' to ' + str(df['maleHighAgeSmoker'][n]))
    #click save button
        input = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="root"]/div[2]/div[3]/div/div[5]/div/div[2]/div/div[16]/div/div/div/div/button'))
            )
        input.click()
    
    #click on features tab 
        driver.find_element_by_xpath('//*[@id="root"]/div[2]/div[3]/div/div[3]/div/div/div/div/button[7]').click()
    #new input into term value
        term = driver.find_element_by_xpath('//*[@id=value')[5]
        term.clear()
        term.send_keys(str(df['productterm'][n]))
    #new input into term text
        term_text = driver.find_element_by_xpath('//*[@id=text')[17]
        term_text.clear()
        term_text.send_keys('Term ' + str(df['productterm'][n]))
    #click save button 
        input = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="root"]/div[2]/div[3]/div/div[5]/div/div[17]/div/div[8]/div/div/div/div/button'))
            )
        input.click()
    
    #go back to the product info and flows tab
        driver.find_element_by_xpath('//*[@id="root"]/div[2]/div[3]/div/div[3]/div/div/div/div/button[1]')
    
        print("product", df.index[n], "created")
   #restart the program for rest of the products 
   
# define the variables, login can be used by anyone who changes the 'email' and 'password' values  
gmail_sign_in('farah.khan@finaeo.com', 'Farah533932')


#click on features tab 
driver.find_element_by_xpath('//*[@id="root"]/div[2]/div[3]/div/div[3]/div/div/div/div/button[7]').click()
#new input into term value
#non-unique ID's into list and then index to the one needed (may change with permanent and CI products)

ids = driver.find_elements_by_xpath('//*[@id="value"]')
term = ids[9]
term.send_keys(Keys.CONTROL + 'a')
term.send_keys(str(df['productterm'][25]))
 #new input into term text
text_ids = driver.find_elements_by_xpath('//*[@id="text"]')
term_text = text_ids[16]
term_text.send_keys(Keys.CONTROL + 'a')
term_text.send_keys('Term ' + str(df['productterm'][25]))
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