# !/usr/bin/python3
# -- coding: UTF-8 --
# Author   :WindAsMe
# Date     :18-9-26 上午8:13
# File     :crawler.py
# Location:/Home/PycharmProjects/..
import xlrd
import requests
import base64
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from time import sleep
from queue import Queue

# Save IPC.xlsx to stack
# Facilitate the searching
def read_xlsx():
    ipc = Queue()
    workbook = xlrd.open_workbook('IPC.xlsx')
    booksheet = workbook.sheet_by_index(0)
    row = 1
    try:
        while True:
            ipc.put(booksheet.cell_value(row, 0))
            row += 1
    except IndexError:
        # Do nothing
        print('Data loading Success')
    return ipc


if __name__ == '__main__':

    # Google Browser is needed
    # ChromeDriver is also needed
    # The correlative version can be found in
    # https://blog.csdn.net/weixin_42551465/article/details/80817552

    queue = read_xlsx()

    browser = webdriver.Chrome()
    # Input the username password and validation code
    browser.get('http://www.pss-system.gov.cn/sipopublicsearch/portal/uiIndex.shtml')
    browser.find_element_by_id('j_username').send_keys('m451024822')
    browser.find_element_by_id('j_password_show').send_keys('m451024822')
    browser.find_element_by_id('j_validation_code').send_keys(input('valid code: '))

    # All Exception can be delete
    try:
        # 1. Press the login button
        log_in = browser.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[3]/div[2]/div[2]/div/a[1]')
        log_in.click()
        sleep(3)
        print('step1: Success')
    except IOError:
        print('step1: Failure')

    try:
        # 2. Press the "高级搜索"
        browser.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[2]/div[2]/div/div/div/div[3]/a/div').click()
        print('step2: Success')
        sleep(3)
    except IOError:
        print('step2: Failure')

    try:
        # 3. Switch the certain tags
        for i in range(1, 7, 2) :
            browser.find_element_by_xpath(
                '/html/body/div[3]/div[2]/div/div[1]/div/div[2]/div/div[1]/ul/li[' + str(i) + ']/a').click()
        print('step3: Success')
        sleep(2)
    except IOError:
        print('step3: Failure')

    try:
        # 4. Start to search
        while not queue.empty():
            browser.find_element_by_id("tableSearchItemIdIVDB045").send_keys(queue.get())
            browser.find_element_by_xpath('/html/body/div[3]/div[3]/div/div[2]/div[3]/a[3]').click()

        print('step4: Success')
    except IOError:
        print('step4: Failure')

    final_data = pd.DataFrame(
        columns=['APP_ID', 'APP_DATE', 'PUB_ID', 'PUB_DATE', 'IPC', 'APPLICANT', 'INVENTOR', 'PRI_ID', 'PRI_DATE',
                 'APP_ADDRESS', 'APP_ZIPCODE', 'CPC_ID'])

    fianl_data.to_csv('final_data.txt', index=True, encoding='utf-8')
    # browser.quit()

