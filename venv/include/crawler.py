# !/usr/bin/python3
# -- coding: UTF-8 --
# Author   :WindAsMe
# Date     :18-9-26 上午8:13
# File     :crawler.py
# Location:/Home/PycharmProjects/..
import re
import xlwt
import xlrd
import requests
import base64
import pandas as pd
from bs4 import BeautifulSoup
# selenium is time susceptible
# It's also the weakness of Python
from selenium import webdriver
from time import sleep
from queue import Queue
from selenium.webdriver.common.keys import Keys
from xlutils.copy import copy


'''
This code can be found in https://github.com/WindAsMe/PythonCrawler

Google Browser is needed
ChromeDriver is also needed
The correlative version can be found in
https://blog.csdn.net/weixin_42551465/article/details/80817552
'''

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


# trim the uncertain str to int
def trim(string):
    s = ''
    for c in string:
        if '0' <= c <= '9':
            s += c
    return int(s)


# Save data in form of Excel
# Global variance
row = 1
def save_data(list1, list2, list3, list4,
    list5, list6, list7, list8, list9,
    list10, list11, list12):
    # Read-only
    workbook = xlrd.open_workbook('data.xls')
    workbook_copy = copy(workbook)
    sheet = workbook_copy.get_sheet(0)

    try:
        global row
        i = 0
        while i < len(list1):
            sheet.write(row, 0, list1[i])
            sheet.write(row, 1, list2[i])
            sheet.write(row, 2, list3[i])
            sheet.write(row, 3, list4[i])
            sheet.write(row, 4, list5[i])
            sheet.write(row, 5, list6[i])
            sheet.write(row, 6, list7[i])
            sheet.write(row, 7, list8[i])
            sheet.write(row, 8, list9[i])
            sheet.write(row, 9, list10[i])
            sheet.write(row, 10, list11[i])
            sheet.write(row, 11, list12[i])
            i += 1
            row += 1
    except BaseException:
        print('save Error')
    workbook_copy.save("data.xls")


# Init the Excel
def init_excel():
    workbook = xlwt.Workbook()
    sheet = workbook.add_sheet(u'sheet1', cell_overwrite_ok=True)
    sheet.write(0, 0, '申请号')
    sheet.write(0, 1, '申请日')
    sheet.write(0, 2, '公开(公告)号')
    sheet.write(0, 3, '公开(公告)日')
    sheet.write(0, 4, 'IPC分类号')
    sheet.write(0, 5, '申请（专利权）人')
    sheet.write(0, 6, '发明人')
    sheet.write(0, 7, '优先权号')
    sheet.write(0, 8, '优先权日')
    sheet.write(0, 9, '申请人地址')
    sheet.write(0, 10, '申请人邮编')
    sheet.write(0, 11, 'CPC分类号')
    workbook.save("data.xls")


# Programme Interface
if __name__ == '__main__':

    queue = read_xlsx()
    init_excel()

    list1 = []
    list2 = []
    list3 = []
    list4 = []
    list5 = []
    list6 = []
    list7 = []
    list8 = []
    list9 = []
    list10 = []
    list11 = []
    list12 = []
    browser = webdriver.Chrome()
    # Input the username password and validation code
    browser.get('http://www.pss-system.gov.cn/sipopublicsearch/portal/uiIndex.shtml')
    browser.find_element_by_id('j_username').send_keys('m451024822')
    browser.find_element_by_id('j_password_show').send_keys('m451024822')
    browser.find_element_by_id('j_validation_code').send_keys(input('valid code: '))
    sleep(3)
    # All Exception can be delete
    try:
        # 1. Press the login button
        browser.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[3]/div[2]/div[2]/div/a[1]').click()
        sleep(3)
        print('step1: Success')
    except BaseException:
        print('step1: Failure')

    try:
        # 2. Press the "高级搜索"
        browser.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[2]/div[2]/div/div/div/div[3]/a/div').click()
        sleep(3)
        print('step2: Success')
    except BaseException:
        print('step2: Failure')

    try:
        # 3. Switch the certain tags
        for i in range(1, 7, 2) :
            browser.find_element_by_xpath(
                '/html/body/div[3]/div[2]/div/div[1]/div/div[2]/div/div[1]/ul/li[' + str(i) + ']/a').click()
            sleep(3)
        print('step3: Success')
        sleep(2)
    except BaseException:
        print('step3: Failure')

    try:
        # 4. Start to search
        # Structure is prefer to the function
        # Save the window handle
        while not queue.empty():
            try:
                IPC = queue.get()
                print("IPC: ", IPC)
                browser.find_element_by_id("tableSearchItemIdIVDB045").send_keys(IPC)
                browser.find_element_by_xpath('/html/body/div[3]/div[3]/div/div[2]/div[3]/a[3]').click()
                # Sleep is necessary
                # For the first loading
                sleep(5)
                # Starting outset crawler
                page_before = browser.find_element_by_xpath('//*[@id="resultMode"]/div/div[2]/div/div/div/div/p[1]').text
                # For certain IPC in different page
                page = trim(page_before)
                for current in range(1, page + 1):
                    item = 1
                    items = browser.find_elements_by_xpath('//*[@id="resultMode"]/div/div[1]/ul/li')
                    main_handle = browser.current_window_handle
                    # For certain page in different thesis
                    while item <= items.__len__():
                        # For some representative xpath:
                        # //*[@id="resultMode"]/div/div[1]/ul/li[1]/div/div[3]/div/a[1]
                        # //*[@id="resultMode"]/div/div[1]/ul/li[3]/div/div[3]/div/a[1]
                        # //*[@id="resultMode"]/div/div[1]/ul/li[9]/div/div[3]/div/a[1]
                        # //*[@id="resultMode"]/div/div[1]/ul/li[12]/div/div[3]/div/a[1]
                        button_path = '//*[@id="resultMode"]/div/div[1]/ul/li[' + str(item) + ']/div/div[3]/div/a[1]'
                        print(button_path)
                        browser.find_element_by_xpath(button_path).send_keys(Keys.ENTER)
                        sleep(5)
                        # Snatch the data
                        handles = browser.window_handles
                        for handle in handles:
                            if handle != main_handle:
                                browser.switch_to.window(handle)
                                content = browser.page_source
                                content.encode('utf-8')
                                # print(content)
                                pattern = re.compile('</div.*?second-td"><div>(.*?)</div.*?tr>', re.S)
                                items = re.findall(pattern, content)
                                sleep(5)
                                print('items:', items.__str__())
                                list1.append(items[0])
                                list2.append(items[1])
                                list3.append(items[2])
                                list4.append(items[3])
                                list5.append(items[4])
                                list6.append(items[5])
                                list7.append(items[6])
                                list8.append(items[7])
                                list9.append(items[8])
                                list10.append(items[9])
                                list11.append(items[10])
                                list12.append(items[11])

                                # Sleep is necessary
                                sleep(2)
                                browser.close()
                                browser.switch_to.window(main_handle)
                        item += 1
                    # Saving in the scale of page
                    print('save')
                    save_data(list1, list2, list3, list4, list5, list6, list7,
                              list8, list9, list10, list11, list12)

                    # init the list
                    list1 = []
                    list2 = []
                    list3 = []
                    list4 = []
                    list5 = []
                    list6 = []
                    list7 = []
                    list8 = []
                    list9 = []
                    list10 = []
                    list11 = []
                    list12 = []
                    current += 1
                    browser.find_element_by_xpath('//*[@id="resultMode"]/div/div[2]/div/div/div/div/a[6]').send_keys(Keys.ENTER)
                    sleep(3)
                    print('next Page')
            # Ignore this Exception
            except BaseException:
                print('read Error')
                # Do nothing
            browser.find_element_by_id("tableSearchItemIdIVDB045").clear()
            sleep(2)
        print('step4: Success')
    except BaseException:
        print('step4: Failure')

    browser.quit()

