# !/usr/bin/python3
# -- coding: UTF-8 --
# Author   :WindAsMe
# Date     :18-9-26 上午8:13
# File     :crawler.py
# Location:/Home/PycharmProjects/..
import requests
import base64
from bs4 import BeautifulSoup
from selenium import webdriver
from time import sleep


if __name__ == '__main__':

    # Google Browser is needed
    # ChromeDriver is also needed
    # The correlative version can be found in
    # https://blog.csdn.net/weixin_42551465/article/details/80817552

    browser = webdriver.Chrome()
    browser.get('http://www.pss-system.gov.cn/sipopublicsearch/portal/uiIndex.shtml')
    browser.find_element_by_id('j_username').send_keys('m451024822')
    browser.find_element_by_id('j_password_show').send_keys('m451024822')
    browser.find_element_by_id('j_validation_code').send_keys(input('valid code: '))
    try:
        log_in = browser.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[3]/div[2]/div[2]/div/a[1]')
        log_in.click()
        sleep(3)
        print('step1: Success')
    except e:
        print('step1: Failure')
    try:
        browser.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[2]/div[2]/div/div/div/div[3]/a/div').click()
        print('step2: Success')
        sleep(3)
    except e:
        print('step2: Failure')
    try:
        for i in range(1, 7, 2) :
            browser.find_element_by_xpath(
                '/html/body/div[3]/div[2]/div/div[1]/div/div[2]/div/div[1]/ul/li[' + str(i) + ']/a').click()
        print('step3: Success')
        sleep(2)
    except e:
        print('step3: Failure')


    # browser.quit()

