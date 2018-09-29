# !/usr/bin/python3
# -- coding: UTF-8 --
# Author   :WindAsMe
# Date     :18-9-28 下午2:10
# File     :deprecated.py
# Location:/Home/PycharmProjects/..
import requests
import base64
from bs4 import BeautifulSoup
from selenium import webdriver
from time import sleep


# Deprecated function
if __name__ == '__main__':
    # Http header
    checkHeader = {
        "Host": "www.pss-system.gov.cn",
        "Proxy-Connection": "keep-alive",
        "Cache-Control": "max-age=0",
        "Origin": "http://www.pss-system.gov.cn",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36",
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Referer": "http://www.pss-system.gov.cn/sipopublicsearch/portal/uiIndex.shtml",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.8"
    }
    header = {
        "Accept": "text / html, * / *;q = 0.01",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.8",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36"
    }
    baseUrl = 'http://www.pss-system.gov.cn/sipopublicsearch/patentsearch/tableSearch-showTableSearchIndex.shtml'
    checkUrl = 'http://www.pss-system.gov.cn/sipopublicsearch/wee/platform/wee_security_check'
    timeUrl = 'http://www.pss-system.gov.cn/sipopublicsearch/portal/checkLoginTimes-check.shtml'
    debugUrl = 'http://www.pss-system.gov.cn/sipopublicsearch/portal/sessionDeBugAC.do'
    codeUrl = 'http://www.pss-system.gov.cn/sipopublicsearch/portal/login-showPic.shtml'

    strName = 'm451024822'
    strPass = 'm451024822'
    base64Name = str(base64.b64encode(bytes(strName,encoding='utf-8')), 'utf-8')
    base64Pass = str(base64.b64encode(bytes(strPass,encoding='utf-8')), 'utf-8')
    timeData = {
        'username': strName
    }
    data = {
        "j_loginsuccess_url": "",
        "j_validation_code": "",
        "j_username": base64Name,
        "j_password": base64Pass
    }
    debugData = {
        "sessionDebugMod.opttype":"login",
        "sessionDebugMod.position":"keepalive",
        "sessionDebugMod.broswer":"Netscape5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36",
        "sessionDebugMod.userName":strName,
        "sessionDebugMod.cur_wee_sid":"",
        "sessionDebugMod.wee_sid":""
    }
    valcode = requests.get(codeUrl,headers=header)
    f = open('valcode.png', 'wb')
    f.write(valcode.content)
    f.close()

    code = input('请输入验证码：')
    data["j_validation_code"] = str(code)
    resp = requests.post(
        checkUrl,
        headers=checkHeader,
        cookies=requests.utils.dict_from_cookiejar(valcode.cookies),
        data=data
    )
    soup = BeautifulSoup(resp.content, 'lxml')
    print(soup.prettify())
