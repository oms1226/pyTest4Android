# -*- coding: utf-8 -*-
#!/usr/bin/python
import datetime
import threading
import urllib
import urllib2
from os.path import basename
import wget

from bs4 import BeautifulSoup
import requests


from common.contant import *
from common.deviceInfo import *
from os import walk


setDEBUG(True)


def leopold_login(id, password):
    # 로그인 정보를 담을 수 있는 객체
    s = requests.Session()

    """ 로그인을 처리하는 페이지 URL """
    login_process_url = "http://www.raonkindergarten.com/members/login"
    params = {"url": "http://www.raonkindergarten.com/members/login",
              'mb_id': id,
              'mb_passwd': password,
              'x': 22,
              'y': 20} #login
    response = s.post(login_process_url, params)
    return s


def required_login_page(session):
    """ 로그인 후에 접근 가능한 페이지 URL """
    login_required_page_url = "http://www.raonkindergarten.com/sub03/sub03_3"
    response = session.get(login_required_page_url)
    soup = BeautifulSoup(response.text)
    #
    # links = soup.select('a[href^="./?doc=cart/orderinquiryview.php"]')
    # for link in links:
    #     print link.get('href'), link.find('u').string
    #     # print response.text.encode('utf-8')
    #
    #
def openerDomain( url ) :
    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3)        AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36')]
    page_to_scrape = opener.open(url, timeout=1).read()
    return BeautifulSoup(page_to_scrape.decode('cp949', 'ignore'), 'html.parser')#'utf-8'

# if __name__ == '__main__':
#     s = leopold_login('oms1226', '9177e6')
#     required_login_page(s)
"""
<a href="/sub03/sub03_3/?method=view&amp;no=12357&amp;page=1" title="2월 둘째주에 미소반에서..">2월 첫째주</a>
<a href="/sub03/sub03_3/?method=download&amp;no=12357&amp;fno=71510">					KakaoTalk_Moim_4JZ367HbKN45NqHAVnRBSTiWnpzkky.jpg</a>
"""


"""
references: https://beomi.github.io/2017/01/20/HowToMakeWebCrawler-With-Login/
"""
def loginIfNotCSRF(url, loginInfo):
    global COOKIE
    # Session 생성, with 구문 안에서 유지
    with requests.Session() as s:
        # HTTP POST request: 로그인을 위해 POST url와 함께 전송될 data를 넣어주자.
        login_response = s.post(url, data=loginInfo)
        printEx("%s:%s" % ('login_response.status_code', login_response.status_code))
        if login_response.status_code == 200:
            COOKIE = login_response.headers.get('Set-Cookie')
            return s
        else:
            return None

# 실제 HTML tagName에 맞추어 변수이름  및 로그인할 유저정보를 넣어주자 (모두 문자열)
LOGIN_INFO = {
    'user_id': 'oms1226',
    'user_password': '9177e6'
}

RAON_MAIN_PAGE = 'http://www.raonkindergarten.com'
RAON_LOGIN_PAGE = RAON_MAIN_PAGE + '/members/login'


def getRaonPage(pageUrl):
    fPass = False
    while fPass == False:
        session = loginIfNotCSRF(RAON_LOGIN_PAGE, LOGIN_INFO)
        try:
            response = session.get(pageUrl)
        except:
            session = loginIfNotCSRF(RAON_LOGIN_PAGE, LOGIN_INFO)
            printEx("%s:%s" % ("session", session))
            response.status_code = 400

        if response.status_code == 200:
            fPass = True
    return response


"""
http://www.raonkindergarten.com/sub03/sub03_3/?method=view&no=12231&page=1
"""
COOKIE = None
if __name__ == "__main__":

    response = getRaonPage('http://www.raonkindergarten.com/sub03/sub03_3')
    soup = BeautifulSoup(response.text, 'html.parser')

    """
    <a href="http://www.raonkindergarten.com/sub03/sub03_3/?page=1" title="Go to page 1" class="page current"><b class="list_page">1</b></a>
    """
    PAGE_LINKS = []
    for ahreflink in soup.find_all('a', href=True):
        if 'http://www.raonkindergarten.com/sub03/sub03_3/?page=' in ahreflink.attrs['href']:
            if ahreflink.attrs['href'] not in PAGE_LINKS:
                PAGE_LINKS.append(ahreflink.attrs['href'])

    CONTENT_LINKS = []
    for pageLink in PAGE_LINKS:
        printEx("%s:%s" % ('pageLink', pageLink))
        response = getRaonPage(pageLink)
        soup = BeautifulSoup(response.text, 'html.parser')
        """
        ex. <a href="/sub03/sub03_3/?method=view&no=12357&page=1" title="2월 둘째주에 미소반에서..">2월 첫째주</a>
       """
        for ahreflink in soup.find_all('a', href=True):
            if '/sub03/sub03_3/?method=view&no=' in ahreflink.attrs['href']:
                if RAON_MAIN_PAGE + ahreflink.attrs['href'] not in CONTENT_LINKS:
                    CONTENT_LINKS.append(RAON_MAIN_PAGE + ahreflink.attrs['href'])


    printEx("%s:%s" % ('len(CONTENT_LINKS)', len(CONTENT_LINKS)))
    for contentLink in CONTENT_LINKS:
        DOWNLOADLIST = {}
        printEx("%s:%s" % ('contentLink', contentLink))
        response = getRaonPage(contentLink)
        soup = BeautifulSoup(response.text, 'html.parser')

        # for a in soup.find_all('a', href=True):
        for ahreflink in soup.find_all('a', href=True):
            """
            <a href="/sub03/sub03_3/?method=download&amp;no=12231&amp;fno=70679">					IMG_6243.JPG</a>
          """
            if 'method=download' in ahreflink.attrs['href']:
                """
              reference: http://stackabuse.com/download-files-with-python/
              """
                #printEx("%s:%s" % ('ahreflink.attrs[href]', ahreflink.attrs['href']))
                fulllinkNmae = RAON_MAIN_PAGE + ahreflink.attrs['href']
                fileName = ""
                if len(ahreflink.contents) >= 1:
                    fileName = ahreflink.contents[0].replace(" ", "").replace('\r', '').replace('\n', '').replace('\t', '')
                if '.jpg' in fileName.lower() or '.png' in fileName.lower():
                    pass
                else:
                    excuteTime = (datetime.datetime.utcnow() + datetime.timedelta(hours=9)).strftime("%Y%m%d%H%M%S")
                    fileName = "ohjihun_raon_2017_" + excuteTime + ".jpg"
                    time.sleep(1)

                DOWNLOADLIST[fileName] = fulllinkNmae

        soup = BeautifulSoup(response.text, 'html.parser')
        for img in soup.find_all('img'):
            """
            <img name="target_resize_image[]" onclick="image_window(this)" src="/data/admin/board_upload/17/images/ffe4f58f314c980ad00778bd6c3a9a69.JPG" class="txc-image" style="clear:none;float:none;">
          """
        #for img in soup.find_all("img", {"onclick": "image_window(this)"}):
            if img.has_attr('src') == 1 and "http" not in img.attrs['src']\
                    and img.has_attr('onclick') == 1 and 'image_window(this)' in img.attrs['onclick']:
                fulllinkNmae = RAON_MAIN_PAGE + img['src']
                fileName = fulllinkNmae.split('/')[-1]

                if '.jpg' in fileName.lower() or '.png' in fileName.lower():
                    pass
                else:
                    excuteTime = (datetime.datetime.utcnow() + datetime.timedelta(hours=9)).strftime("%Y%m%d%H%M%S")
                    fileName = "ohjihun_raon_2017_" + excuteTime + ".jpg"
                    time.sleep(1)

                DOWNLOADLIST[fileName] = fulllinkNmae

        session = loginIfNotCSRF(RAON_LOGIN_PAGE, LOGIN_INFO)
        for fileN, linkU in DOWNLOADLIST.items():
            content = session.get(linkU).content
            if 'text/html' not in content:
                try:
                    with open("D:\\ohjihun_raon_2017\\" + fileN, "wb") as f:
                        status = f.write(content)
                        printEx("%s:%s" % ('createFile', "D:\\ohjihun_raon_2017\\" + fileN))
                except:
                    printEx("%s:%s" % ('linkU', linkU))
                    printEx("%s:%s" % ('fileN', fileN))
                    print "Unexpected error:", sys.exc_info()[0]
                    print "Unexpected error:", sys.exc_info()[1]
                    print "Unexpected error:", sys.exc_info()[2]

                    if os.path.isfile("D:\\ohjihun_raon_2017\\" + fileN):
                        os.remove("D:\\ohjihun_raon_2017\\" + fileN)

