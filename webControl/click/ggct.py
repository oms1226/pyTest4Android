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
#elem = driver.find_element_by_link_text(u'설 승차권')
#elem = driver.find_element_by_class_name("menu_01")
#elem = driver.find_element_by_name('menu1')
try:
    target = u'랜덤 채팅 시작하기'
    # target = u'랜덤채팅'
    #<button type="button" onclick="window.rchat_start();">랜덤 채팅 시작하기</button>
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
input.send_keys(u'ㅇㅈ', Keys.ENTER)
time.sleep(2)
# elem = driver.find_element_by_class_name(u"v_area v_area_scroll")
# driver.switch_to_active_element();
# elems = driver.find_elements_by_class_name(u"msg msg_stranger")
# elems = driver.find_elements_by_xpath('//div[@class="msg msg_stranger"]')

story = [
    u'하고 싶어',
    u'33',
    u'넌 몇살?',
    u'뭐하는데?',
    u'원하는게 뭐?',
    u'안하고싶으면 나가',
    u'서울',
    u'넌 어디',
    u'저녁에 나오면 줄께',
    u'넌 혼자살아',
    u'뭐 딴놈이랑 하는 맛이 있어서 들어오긴 했쥐'
    u'번호찍어',
    u'안알려줄꺼면 나가',
    u'나도 딴넘 찾아야해'
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
				<div class="v_area_in"><div class="msg msg_notice"><span class="msg_in">&lt;가가라이브 랜덤 채팅&gt;</span></div>
		<div class="msg msg_notice"><span class="msg_in"><a href="http://www.gagalive.com/" target="_1">http://www.gagalive.com/</a> 랜덤 채팅 서버에 접속되었습니다.</span></div>
		<div class="msg msg_notice"><span class="msg_in">랜덤한 사람이 대화방에 입장했습니다. 편하게 대화하시길 바랍니다!~</span></div>
		<div class="msg msg_self"><span class="nick">당신</span><span class="date"> <span> (</span>오전 10:48<span>)</span></span><span class="i"> : </span><span class="msg_in">ㅇㅈ</span></div>
		<div class="msg msg_stranger"><span class="nick">낯선상대</span><span class="date"> <span> (</span>오전 10:48<span>)</span></span><span class="i"> : </span><span class="msg_in">ㄴㅈ</span></div>
		<div class="msg msg_stranger"><span class="nick">낯선상대</span><span class="date"> <span> (</span>오전 10:48<span>)</span></span><span class="i"> : </span><span class="msg_in">ㅎㅇ</span></div>
		<div class="msg msg_stranger"><span class="nick">낯선상대</span><span class="date"> <span> (</span>오전 10:48<span>)</span></span><span class="i"> : </span><span class="msg_in">35서울</span></div>
		<div class="msg msg_notice"><span class="msg_in">대화가 끝났습니다.</span></div></div>
				<div class="preview"></div>
			</div>
"""