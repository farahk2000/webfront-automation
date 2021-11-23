# -*- coding: utf-8 -*-
"""
Created on Tue Sep  7 11:56:03 2021

@author: farah
"""

#raw script without the def functions - testing only
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
df['productnamenew']= df['productname'].str.replace('Insurance ','')
# create new column with term value 
df['productterm'] = df.productnamenew.str.split().apply(lambda x: x[1]).astype(int)

#rename the products to match the current uplaoded products
df['productname']= df['productname'].str.replace('Insurance','Insurance: Term')
df['productname']= df['productname'].str.replace('years','')
df['productname']= df['productname'].str.replace(',','-')
df['productname']= df['productname'].str.replace('decreasing 50%','50% Decreasing')
df['productname'][:22]= df['productname'][:22].str.replace('Pick-A-Term','Pick-A-Term: Term')
print(df['productname'])

#rounded the term to the nearst 5 value (makes the most sense when filtering)
df['productterm']=(np.around(df.productterm.values/5, decimals=0)*5).astype(int)
print(df['productterm'])
    
#cleaned and organized df

#text summarizer using ntlk (product description is too long)
import bs4 as bs
import re
import nltk
index = [0,22]
summary_list = []
for n in index:
    scraped_data = df['productDesc'][n]
    article = scraped_data
    
    parsed_article = bs.BeautifulSoup(article,'lxml')
    
    paragraphs = parsed_article.find_all('p')
    
    article_text = ""
    
    for p in paragraphs:
        article_text += p.text
    # Removing Square Brackets and Extra Spaces   
    article_text = re.sub(r'\[[0-9]*\]', ' ', article_text)
    article_text = re.sub(r'\s+', ' ', article_text)
    # Removing special characters and digits
    formatted_article_text = re.sub('[^a-zA-Z]', ' ', article_text )
    formatted_article_text = re.sub(r'\s+', ' ', formatted_article_text)
    
    sentence_list = nltk.sent_tokenize(article_text)
    
    stopwords = nltk.corpus.stopwords.words('english')
    
    word_frequencies = {}
    for word in nltk.word_tokenize(formatted_article_text):
        if word not in stopwords:
            if word not in word_frequencies.keys():
                word_frequencies[word] = 1
            else:
                word_frequencies[word] += 1
    maximum_frequncy = max(word_frequencies.values())
    
    for word in word_frequencies.keys():
        word_frequencies[word] = (word_frequencies[word]/maximum_frequncy)
        
    sentence_scores = {}
    for sent in sentence_list:
        for word in nltk.word_tokenize(sent.lower()):
            if word in word_frequencies.keys():
                if len(sent.split(' ')) < 30:
                    if sent not in sentence_scores.keys():
                        sentence_scores[sent] = word_frequencies[word]
                    else:
                        sentence_scores[sent] += word_frequencies[word]
    import heapq
    summary_sentences = heapq.nlargest(7, sentence_scores, key=sentence_scores.get)
    summary = ' '.join(summary_sentences)
    summary_list.append(summary)
    print(summary)
    
#replace current text in dataframe with the new summary creation (text and summary changes half-way into the df)
regular = str(summary_list[0])
decreasing = str(summary_list[1])
df.loc[0:22,'productDesc'] = regular
df.loc[22:45,'productDesc'] = decreasing
#check if dataframe is replaced (test)
print(df['productDesc'][1])
print(df['productDesc'][35])

#automated cloning of products - Finaeo
import time
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

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
 
# wait for the 2FA to be run on the phone manually, then the program should identify the 'carrier button' 
input = WebDriverWait(driver,30).until(
     EC.element_to_be_clickable((By.XPATH, '//*[@id="root"]/div[2]/div[3]/div/div/div[2]/div[11]/div/div/img'))
     )
input.click()
#click the 'product' button OR create a new link to the exact product family that you need to work on  
driver.find_element_by_xpath('//*[@id="root"]/div[2]/div[3]/div/div[4]/div/div/div/div/div[3]/a').click()

# uses the link 
driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + 't') 
driver.get('https://admin.finaeo.ca/product-family/37/ia')

# or this method can be used --> (uses the page element)
#driver.find_element_by_xpath('//*[@id="root"]/div[2]/div[3]/div/div/div[3]/div/div[3]/a').click()

#clicking under the products tab 
input = WebDriverWait(driver, 10).until(
     EC.element_to_be_clickable((By.XPATH, '//*[@id="root"]/div[2]/div[3]/div/div[2]/div/div/div/div/button[4]'))
 )
input.click()
# clicking on the product OR you can also use the link that it is redirecting to 
driver.find_element_by_xpath('//*[@id="root"]/div[2]/div[3]/div/div[4]/div/div[2]/div/div[1]/div/div[1]/a').click()
#driver.find_element_by_link_text('Product 1: Pick-A-Term Insurance: Term 10 - 50% Decreasing')

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
        
        #description tab 
        driver.find_element_by_xpath('//*[@id="root"]/div[2]/div[3]/div/div[3]/div/div/div/div/button[2]').click()
        
        summary = WebDriverWait(driver, 10).until(
             EC.element_to_be_clickable((By.XPATH, '//*[@id="summaryEn"]'))
         )
        summary.click()
        summary.send_keys(Keys.CONTROL + 'a')
        summary.send_keys(df['productDesc'][n])
        # click save 
        input = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="root"]/div[2]/div[3]/div/div[5]/div/div[7]/div/div/div/div/button'))
             )
        input.click()
        
        #eligiblity tab
        driver.find_element_by_xpath('//*[@id="root"]/div[2]/div[3]/div/div[3]/div/div/div/div/button[6]').click()
        #enter value from malelowage smoker and malehighagesmoker
        min_age = driver.find_element_by_id('min')
        min_age.send_keys(Keys.CONTROL + 'a')
        min_age.send_keys(str(df['maleLowAgeSmoker'][n]))
        
        max_age = driver.find_element_by_id('max')
        max_age.send_keys(Keys.CONTROL + 'a')
        max_age.send_keys(str(df['maleHighAgeSmoker'][n]))
        # enter value mentioned before but add the word "to" in between
        age_text = driver.find_element_by_id('textEn')
        age_text.send_keys(Keys.CONTROL + 'a')
        age_text.send_keys(str(df['maleLowAgeSmoker'][n]) + ' to ' + str(df['maleHighAgeSmoker'][n]))
         #click save button
        input = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="root"]/div[2]/div[3]/div/div[5]/div/div[2]/div/div[16]/div/div/div/div/button'))
             )
        input.click()
        
        input = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="root"]/div[2]/div[3]/div/div[5]/div/div[2]/div/div[16]/div/div/div/div/button'))
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