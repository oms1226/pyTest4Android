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
#���̹� �ð躸�� 1�� �� �����ٰ� �Ǵ��ؼ� �����ϴ� 2019.08.20�� �߼� ���� ���� �׷��� 2�� ������ �����ص�
while int(myTime) < 70002:#7�� 00�� 02��
    myTime = time.strftime('%H%M%S')


#elem = driver.find_elements_by_xpath("//*[@type='submit']")#put here the content you have put in Notepad, ie the XPath
#elem = driver.find_element_by_link_text(u'�� ������')
#elem = driver.find_element_by_class_name("menu_01")
#elem = driver.find_element_by_name('menu1')
try:
    target = u'�߼� ������ ����'
    elem = driver.find_element_by_partial_link_text(target)
except:
    print 'not found -> (target:%s)' % (target)
    target = u'�� ������ ����'
    elem = driver.find_element_by_partial_link_text(target)

#elem = driver.find_element_by_partial_link_text('06:00~15:00')
#elem = driver.ffind_element_by_css_selector('a.menu1')
elem.click()
print 'click -> (target:%s)' % (target)
inputStr = input("please enter?")
print inputStr
driver.close()