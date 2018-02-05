import numpy as np
import cv2
import os
import sys
import time
from time import gmtime, strftime
import random
import subprocess
from pandas import Series, DataFrame
import datetime
from sys import platform as _platform
from instagram.client import InstagramAPI
import urllib2
import requests
import webbrowser

if __name__ == '__main__':
    """private info"""
    clientid = "c17deb7598514759962962684d1b8d65"
    clientsecret = "9d2557f63fe44ebfa14a48ed72b1b522"
    re_url = "http://localhost"
    authenticationType = "Server-Side" #"Client-Side" #"PASS"
    authenticationType = "PASS"

    if authenticationType == "Server-Side":
        service_url = "https://instagram.com/oauth/authorize/?client_id=" + clientid + "&redirect_uri=" + re_url + "&response_type=code"
        print service_url
        webbrowser.open(service_url)
        sys.exit()

        code = '0d15fb8d6b1849b8a2791f15faa6cc21'  # I open the browser and go on to the service url and get the code
        api = InstagramAPI(client_id=clientid, client_secret=clientsecret, redirect_uri=re_url)
        access_token = api.exchange_code_for_access_token(code)
        print 'access_token: "%s"' % str(access_token)
        sys.exit()

    if authenticationType == "Client-Side":
        service_url = "https://instagram.com/oauth/authorize/?client_id=" + clientid + "&redirect_uri=" + re_url + "&response_type=token"
        print service_url
        webbrowser.open(service_url)
        sys.exit()

        response = requests.get(service_url)
        if response.history:
            print "Request was redirected"
            for resp in response.history:
                print resp.status_code, resp.url
            print "Final destination:"
            print response.status_code, response.url
        else:
            print "Request was not redirected"

        #sys.exit()
        try:
            #response = urllib2.urlopen(service_url)
            req = urllib2.Request(service_url)
            response = urllib2.urlopen(req)
            print 'response headers: "%s"' % response.info()
            data = response.read()
            print 'response data: "%s"' % data
            print 'response url: "%s"' % response.geturl()
            #print 'response code: "%s"' % response.get['code']


        except IOError, e:
            if hasattr(e, 'code'):  # HTTPError
                print 'http error code: ', e.code
            elif hasattr(e, 'reason'):  # URLError
                print "can't connect, reason: ", e.reason
            else:
                raise

    access_token="5432922616.c17deb7.c07622c8f4af4d65861dbd0485847699"
    api = InstagramAPI(access_token=access_token, client_secret=clientsecret)
    #api = InstagramAPI(access_token=access_token)

    data = api.user(user_id='self')
    print data
    print "id: " + data.id
    print "username: " + data.username
    print "full_name: " + data.full_name
    print "profile_picture: " + data.profile_picture
    print "bio: " + data.bio
    print "website: " + data.website
    print "counts: " + str(data.counts)

    sys.exit()
    #recent_media, next_ = api.user_recent_media(user_id='self', count=10)
    recent_media, next_ = api.user_follows(user_id='self')
    #recent_media, next_ = api.user_search()
    for media in recent_media:
        print media.caption.text

    sys.exit()
    api = InstagramAPI(client_id=clientid, client_secret=clientsecret, access_token=access_token)
    popular_media = api.media_popular(count=20)
    for media in popular_media:
        print media.images['standard_resolution'].url