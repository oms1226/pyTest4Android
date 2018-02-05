import re
import requests
from bs4 import BeautifulSoup
import sys
import urllib
import getInfoFromMedia
import random
import datetime
import shutil
import urllib2
import unicodedata

def openerDomain( url ) :
    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3)        AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36')]
    page_to_scrape = opener.open(url, timeout=1).read()
    return BeautifulSoup(page_to_scrape.decode('cp949', 'ignore'), 'html.parser')#'utf-8'

def getInitDomain() :
    f = open('initDomainList.txt')
    lines = f.readlines()
    select = random.randrange(0, len(lines))

    return lines[select]

MAX_COUNT = 100

previousDomainUrl = domainUrl = "http://bomool5074.blog.me/221007085840"#getInitDomain()
page = requests.get(domainUrl)
"""
#soup = BeautifulSoup(page.text, 'html.parser')
#soup = BeautifulSoup(page.text, "html5lib")
#soup = BeautifulSoup(page.text, "lxml")
"""
soup = openerDomain(domainUrl)


if __name__ == '__main__':
    stayCount = 0
    reVisitCount = 0
    Ing = True

    if False:
        initDomain = "http://blog.naver.com/onsili/PostView.nhn?blogId=onsili&logNo=221000292673&redirect=Dlog&widgetTypeCall=true"
        print initDomain
        try:
            number = int(filter(str.isdigit, initDomain))
        except:
            number = None
        print number
        print initDomain.replace(str(number), str(number+1))
        sys.exit()
        print getInitDomain()
        sys.exit()

        links = soup.find_all('a', href=True)
        print links
        print type(links)
        sys.exit()
        tagetImg = getInfoFromMedia.IMAGE("testImg.jpg")
        sys.exit()
        crawlingDesc, crawlingLatitude, crawlingLongitude = None, None, None
        url = "http://blog.naver.com/PostView.nhn?blogId=onsili&logNo=221000292673&redirect=Dlog&widgetTypeCall=true"
        soup = openerDomain(url)
        #for map in soup.find_all('a', attrs={'data-linkdata'}, href=True):
        for map in soup.select('a[data-linktype="map"]'):
            print map['data-linkdata']
            mapDict = eval(map['data-linkdata'])
            crawlingLatitude = float(mapDict['latitude'])
            crawlingLongitude = float(mapDict['longitude'])
            crawlingDesc = mapDict['title']

            #['latitude']
            #print dict(map['data-linkdata'])['longitude']
        sys.exit()
        url = "http://blog.naver.com/onsili/221000292673"
        soup = openerDomain(url)
        rootUrl = url[:url.index("/", url.index(url.split("/")[2]))]
        for img in soup.find_all('frame'):
            if img.has_key('src') == 1 and not "http" in img['src']:
                print rootUrl + img['src']

        # page = requests.get(domainUrl)
        # print page.content
        # print page.text
        sys.exit()

    while Ing:
        print 'url: "%s"' % domainUrl
        crawlingDesc, crawlingLatitude, crawlingLongitude, crawlingDate = None, None, None, None

        for map in soup.select('a[data-linktype="map"]'):
            """Naver Blog focus!"""
            print map['data-linkdata']
            mapDict = eval(map['data-linkdata'])
            crawlingLatitude = float(mapDict['latitude'])
            crawlingLongitude = float(mapDict['longitude'])
            crawlingDesc = mapDict['title']

        for img in soup.find_all('img'):
            if img.has_key('src') == 1 and "http" in img['src'] :
                try:
                    print 'imgLink: "%s"' % img['src']
                    urllib.urlretrieve(img['src'], "testImg.jpg")
                    tagetImg = getInfoFromMedia.IMAGE("testImg.jpg")
                    isJpg, ctime, latitude, longitude, description, filename = tagetImg.getLocation()
                    if isJpg :
                        if latitude == None or longitude == None:
                            crawlingDate = (datetime.datetime.utcnow() + datetime.timedelta(hours=9)).strftime("%Y:%m:%d %H:%M:%S")
                            tagetImg.set_gps_location(crawlingLatitude, crawlingLongitude, crawlingDesc, crawlingDate)
                        else:
                            tagetImg.set_gps_location(imageDescription = crawlingDesc)

                    isJpg, ctime, latitude, longitude, description, filename = tagetImg.getLocation()
                    print 'latitude: "%s"' % latitude + ' / longitude: "%s"' % longitude
                    if isJpg and latitude != None and longitude != None :
                        NEED_FILEWRITE = True
                        f = open("./jepgWithGPS/info.txt", 'a+')
                        for line in f:
                            if img['src'] in line:
                                NEED_FILEWRITE = False
                                reVisitCount = reVisitCount + 1
                                break
                        if NEED_FILEWRITE:
                            shutil.move("testImg.jpg", "./jepgWithGPS/" + filename + ".jpg")
                            shutil.move("testImg.jpg.kml", "./jepgWithGPS/" + filename + ".kml")
                            #f.writelines("%s\t%s\t%s\t%s\t%s\t%s\n" % str((datetime.datetime.utcnow() + datetime.timedelta(hours=9)).strftime("%Y%m%d%H%M%S")).replace(" ", "").strip(), filename, img['src'], ctime, latitude, longitude)
                            f.write(str((datetime.datetime.utcnow() + datetime.timedelta(hours=9)).strftime("%Y%m%d%H%M%S")).replace(" ", "").strip() + "\t" + domainUrl + "\t" + str(filename) + "\t" +
                                    str(img['src']) + "\t" + str(ctime) + "\t" + str(latitude) + "\t" + str(longitude) + "\n")
                            reVisitCount = 0
                        f.close()
                except KeyboardInterrupt:
                    break
                except UnicodeEncodeError:
                    """UnicodeEncodeError: 'cp949' codec can't encode character u'\xe9' in position 97: illegal multibyte sequence"""""
                    print "Unexpected error:", sys.exc_info()[0]
                    print "Unexpected error:", sys.exc_info()[1]
                    print "Unexpected error:", sys.exc_info()[2]
                    pass
                except:
                    print "Unexpected error:", sys.exc_info()[0]
                    print "Unexpected error:", sys.exc_info()[1]
                    print "Unexpected error:", sys.exc_info()[2]
                    pass

        isTry = True

        frameLinks = []
        try:
            rootUrl = domainUrl[:domainUrl.index("/", domainUrl.index(domainUrl.split("/")[2]))]
        except:
            rootUrl = None

        if rootUrl != None :
            for frame in soup.find_all('frame'):
                """Naver Blog Focus"""
                try:
                    if frame.has_key('src') == 1 and not "http" in frame['src']:
                        print type(frame['src'])
                        print frame['src']
                        frameUrl = unicodedata.normalize('NFKD', frame['src']).encode('ascii', 'ignore')
                        print rootUrl + frameUrl
                        frameUrl = rootUrl + frameUrl
                        if len(frameLinks) == 0 :
                            frameLinks = [frameUrl]
                        else :
                            frameLinks = frameLinks + [frameUrl]
                except:
                    print "Unexpected error:", sys.exc_info()[0]
                    print "Unexpected error:", sys.exc_info()[1]
                    print "Unexpected error:", sys.exc_info()[2]
                    pass

        if len(frameLinks) > 0:
            select = random.randrange(0, len(frameLinks))
            domainUrl = frameLinks[select]
            soup = openerDomain(domainUrl)
            isTry = False

        tryCount = 0
        if isTry:
            links = soup.find_all('a', href=True)

        while isTry:
            if tryCount > len(links) :
                domainUrl = getInitDomain()
            elif len(links) > 0 :
                select = random.randrange(0, len(links))
                if "http" in links[select]['href']:
                    domainUrl = links[select]['href']
                elif rootUrl != None:
                    domainUrl = rootUrl + links[select]['href']
            else:
                domainUrl = getInitDomain()

            if reVisitCount > MAX_COUNT :
                domainUrl = getInitDomain()

            if previousDomainUrl == domainUrl :
                stayCount = stayCount + 1
            else :
                stayCount = 0

            ratio = random.randrange(0, 100)
            if ratio > 50 :
                try:
                    number = int(filter(str.isdigit, domainUrl))
                    ratio = random.randrange(0, 2)
                    if ratio > 0 :
                        domainUrl = domainUrl.replace(str(number), str(number + 1))
                    else :
                        domainUrl = domainUrl.replace(str(number), str(number - 1))
                except:
                    number = None

            tryCount = tryCount + 1
            try:
                #page = requests.get(domainUrl)
                #soup = BeautifulSoup(page.text, 'html.parser')
                soup = openerDomain(domainUrl)
                isTry = False
            except KeyboardInterrupt:
                break
            except:
                print "Unexpected error:", sys.exc_info()[0]
                print "Unexpected error:", sys.exc_info()[1]
                print "Unexpected error:", sys.exc_info()[2]
                pass

            previousDomainUrl = domainUrl

            if stayCount > MAX_COUNT :
                stayCount = 0
                if domainUrl == getInitDomain() :
                    print "Occur Deadlock!"
                    Ing = False
                    break
                else :
                    domainUrl = getInitDomain()


    if False:
        #    opener = urllib2.build_opener()
        #    opener.addheaders = [('User-agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3)        AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36')]
        #    page_to_scrape = opener.open(domainUrl).read()
        #    soup = BeautifulSoup(page_to_scrape.decode('utf-8', 'ignore'))
        # for tag in soup.find_all(attrs={"data-linktype"}):
        print 'url: "%s"' % domainUrl
        #    print soup.get_text()
        for img in soup.find_all('img'):
            print img

        # page = requests.get(domainUrl)
        # print page.content
        # print page.text
        sys.exit()




    urllib.urlretrieve("http://nstatic.dcinside.com/dgn/gallery/images/new_banner_6.gif", "testImg.jpg")
    tagetImg = getInfoFromMedia.IMAGE("honeyview-gps.jpg")
    isJpg, ctime, latitude, longitude, description, filename = tagetImg.getLocation()
    print 'latitude: "%s"' % latitude + ' / longitude: "%s"' % longitude

    sys.exit()

