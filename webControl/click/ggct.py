#!/usr/bin/python
# -*- coding: cp949 -*-
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0
import time
import sys
reload(sys)
sys.setdefaultencoding('utf8')


#sys.exit(0)

#driver = webdriver.Ie()
"""
https://sites.google.com/a/chromium.org/chromedriver/downloads
"""
driver = webdriver.Firefox(executable_path='/usr/local/bin/geckodriver')
driver.get("http://gagalive.kr/randomchat/")#put here the adress of your page


myTime = time.strftime('%H%M%S')
print type(myTime)
print myTime
print int(myTime)

#elem = driver.find_elements_by_xpath("//*[@type='submit']")#put here the content you have put in Notepad, ie the XPath
#elem = driver.find_element_by_link_text(u'�� ������')
#elem = driver.find_element_by_class_name("menu_01")
#elem = driver.find_element_by_name('menu1')
try:
    target = u'���� ä�� �����ϱ�'
    # target = u'����ä��'
    #<button type="button" onclick="window.rchat_start();">���� ä�� �����ϱ�</button>
    # elem = driver.find_element_by_partial_link_text(target)
    elem = driver.find_element_by_class_name(u'start')
    # elem = driver.find_element_by_id(u"c_area")
    # elem = driver.find_element_by_class_name('body')
except:
    print 'not found -> (target:%s)' % (target)

#elem = driver.find_element_by_partial_link_text('06:00~15:00')
#elem = driver.ffind_element_by_css_selector('a.menu1')
elem.click()
# driver.switch_to_active_element();
print 'click -> (target:%s)' % (target)
time.sleep(3)
#<input type="text" name="" value="">
input = driver.find_element_by_xpath("//input[@name='']")
# elem = driver.find_element_by_class_name(u'input')
input.send_keys(u'����', Keys.ENTER)
time.sleep(2)
# elem = driver.find_element_by_class_name(u"v_area v_area_scroll")
# driver.switch_to_active_element();
# elems = driver.find_elements_by_class_name(u"msg msg_stranger")
# elems = driver.find_elements_by_xpath('//div[@class="msg msg_stranger"]')

story = [
    u'�ϰ� �;�',
    u'33',
    u'�� ���?',
    u'���ϴµ�?',
    u'���ϴ°� ��?',
    u'���ϰ������ ����',
    u'����',
    u'�� ���',
    u'���ῡ ������ �ٲ�',
    u'�� ȥ�ڻ��',
    u'�� �����̶� �ϴ� ���� �־ ������ ����'
    u'��ȣ���',
    u'�Ⱦ˷��ٲ��� ����',
    u'���� ���� ã�ƾ���'
]
for text in story:
    for elem in driver.find_elements_by_xpath('//div[@class="msg msg_stranger"]'):
        try:
            print elem.text
        except:
            pass
    time.sleep(10)
    input.send_keys(text, Keys.ENTER)


inputStr = input("please enter?")
print inputStr
driver.close()
"""
<div class="v_area v_area_scroll">
				<div class="v_area_in"><div class="msg msg_notice"><span class="msg_in">&lt;�������̺� ���� ä��&gt;</span></div>
		<div class="msg msg_notice"><span class="msg_in"><a href="http://www.gagalive.com/" target="_1">http://www.gagalive.com/</a> ���� ä�� ������ ���ӵǾ����ϴ�.</span></div>
		<div class="msg msg_notice"><span class="msg_in">������ ����� ��ȭ�濡 �����߽��ϴ�. ���ϰ� ��ȭ�Ͻñ� �ٶ��ϴ�!~</span></div>
		<div class="msg msg_self"><span class="nick">���</span><span class="date"> <span> (</span>���� 10:48<span>)</span></span><span class="i"> : </span><span class="msg_in">����</span></div>
		<div class="msg msg_stranger"><span class="nick">�������</span><span class="date"> <span> (</span>���� 10:48<span>)</span></span><span class="i"> : </span><span class="msg_in">����</span></div>
		<div class="msg msg_stranger"><span class="nick">�������</span><span class="date"> <span> (</span>���� 10:48<span>)</span></span><span class="i"> : </span><span class="msg_in">����</span></div>
		<div class="msg msg_stranger"><span class="nick">�������</span><span class="date"> <span> (</span>���� 10:48<span>)</span></span><span class="i"> : </span><span class="msg_in">35����</span></div>
		<div class="msg msg_notice"><span class="msg_in">��ȭ�� �������ϴ�.</span></div></div>
				<div class="preview"></div>
			</div>
"""