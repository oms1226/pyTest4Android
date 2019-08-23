#!/usr/bin/python
# -*- coding: cp949 -*-
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import sys
reload(sys)
sys.setdefaultencoding('utf8')


#sys.exit(0)

#driver = webdriver.Ie()
"""
https://sites.google.com/a/chromium.org/chromedriver/downloads
"""
driver = webdriver.Chrome('chromedriver.exe')
driver.get("http://www.letskorail.com/")#put here the adress of your page


myTime = time.strftime('%H%M%S')
print type(myTime)
print myTime
print int(myTime)
#네이버 시계보다 1초 더 빠르다고 판단해서 설정하니 2019.08.20일 추석 예매 실패 그래서 2초 앞으로 세팅해둠
while int(myTime) < 70002:#7시 00분 02초
    myTime = time.strftime('%H%M%S')


#elem = driver.find_elements_by_xpath("//*[@type='submit']")#put here the content you have put in Notepad, ie the XPath
#elem = driver.find_element_by_link_text(u'설 승차권')
#elem = driver.find_element_by_class_name("menu_01")
#elem = driver.find_element_by_name('menu1')
try:
    target = u'추석 승차권 예약'
    elem = driver.find_element_by_partial_link_text(target)
except:
    print 'not found -> (target:%s)' % (target)
    target = u'설 승차권 예약'
    elem = driver.find_element_by_partial_link_text(target)

#elem = driver.find_element_by_partial_link_text('06:00~15:00')
#elem = driver.ffind_element_by_css_selector('a.menu1')
elem.click()
print 'click -> (target:%s)' % (target)
inputStr = input("please enter?")
print inputStr
driver.close()