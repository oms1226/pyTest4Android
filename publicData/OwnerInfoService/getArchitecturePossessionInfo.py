#!/usr/bin/python
# -*- coding: utf-8 -*-
# Python 샘플 코드 #

"""
curl --include --request GET 'http://apis.data.go.kr/1611000/OwnerInfoService/getArchitecturePossessionInfo?ServiceKey=tWjeFvBdTvGiC0YrsTw1UTnUGWEHcKgb42d12WMvVFrJOx5WaNzFqczAcLhWWq8MG8OyaJT214hvao1TQ4wY7g%3D%3D&pageNo=1&numOfRows=10&sigungu_cd=11680&bjdong_cd=10100&plat_gb_cd=0&bun=0601&ji=0001&dong_nm=&ho_nm='
"""
import csv
import os
import sys
from urllib import urlencode, quote_plus
from urllib2 import Request, urlopen
import datetime
import xmltodict

reload(sys)
sys.setdefaultencoding('utf8')

ServiceKey = 'tWjeFvBdTvGiC0YrsTw1UTnUGWEHcKgb42d12WMvVFrJOx5WaNzFqczAcLhWWq8MG8OyaJT214hvao1TQ4wY7g%3D%3D'
url = 'http://apis.data.go.kr/1611000/OwnerInfoService/getArchitecturePossessionInfo'
index_filename = 'index.log'

def getArchitecturePossessionInfo():
    # queryParams = '?' + urlencode({ quote_plus('ServiceKey') : '서비스키', quote_plus('ServiceKey') : '-', quote_plus('pageNo') : '1', quote_plus('numOfRows') : '10', quote_plus('sigungu_cd') : '11680', quote_plus('bjdong_cd') : '10100', quote_plus('plat_gb_cd') : '0', quote_plus('bun') : '0601', quote_plus('ji') : '0001', quote_plus('dong_nm') : '', quote_plus('ho_nm') : '' })
    queryParams = urlencode({
                                   quote_plus('pageNo'): '1', quote_plus('numOfRows'): '10',
                                   quote_plus('sigungu_cd'): '11680', quote_plus('bjdong_cd'): '10100',
                                   quote_plus('plat_gb_cd'): '0', quote_plus('bun'): '0601', quote_plus('ji'): '0001',
                                   quote_plus('dong_nm'): '', quote_plus('ho_nm'): ''
    })

    # request = Request(url + queryParams)
    request = Request(url + '?ServiceKey=' + ServiceKey + '&' + queryParams)
    request.get_method = lambda: 'GET'
    response_body = urlopen(request).read()
    print response_body

def getArchitecturePossessionInfo(sigungu_cd, bjdong_cd, plat_gb_cd, bun, ji):

    queryParams = urlencode({
                                   quote_plus('pageNo'): '1', quote_plus('numOfRows'): '10',
                                   quote_plus('sigungu_cd'): sigungu_cd, quote_plus('bjdong_cd'): bjdong_cd,
                                   quote_plus('plat_gb_cd'): plat_gb_cd, quote_plus('bun'): bun, quote_plus('ji'): ji,
                                   quote_plus('dong_nm'): '', quote_plus('ho_nm'): ''
    })

    # request = Request(url + queryParams)
    request = Request(url + '?ServiceKey=' + ServiceKey + '&' + queryParams)
    request.get_method = lambda: 'GET'
    response_body = urlopen(request).read()
    return response_body


if __name__ == "__main__":
    #getArchitecturePossessionInfo()
    #exit(0);
    START______TIME = (datetime.datetime.utcnow() + datetime.timedelta(hours=9)).strftime("%Y%m%d%H%M")
    help_print = False
    result_filename = 'response4houseAddressInSeoul.csv'
    if os.path.exists(result_filename):
        help_print = True

    previousIndex = 0
    if os.path.exists(index_filename):
        with open(index_filename, 'rb') as f:
            try:
                previousIndex = int(f.read())
            except:
                print "Unexpected error: ", sys.exc_info()[0], sys.exc_info()[1]

    with open('houseAddressInSeoul.csv') as f:
        csv_reader = csv.reader(f)
        for index, row in enumerate(csv_reader):
            print "%s:%s" % ("START______TIME", START______TIME)
            print index, row
            if index == 0:
                continue
            if index <= previousIndex:
                continue
            pk, regstr_gb_cd, regstr_gb_nm, regstr_kind_cd, regstr_kind_nm, sigungu_cd, bjdong_cd, plat_gb_cd, bun, ji = row
            print 'request:', sigungu_cd, bjdong_cd, plat_gb_cd, bun, ji
            response_body = getArchitecturePossessionInfo(sigungu_cd, bjdong_cd, plat_gb_cd, bun, ji)
            #print response_body
            xpars = xmltodict.parse(response_body)
            try:
                with open(result_filename, 'a') as csv_file:
                    writer = csv.writer(csv_file)
                    for item in xpars['response']['body']['items']['item']:
                        if not isinstance(item, dict):#type(item) != dict --> is not working
                            continue
                        if help_print == False:
                            writer.writerow(item.keys())
                            help_print = True

                        writer.writerow(item.values())
                        #writer.write(item.values())
                #break
            except:
                print "Unexpected error: ", sys.exc_info()[0], sys.exc_info()[1]

            with open(index_filename, 'w') as f:
                try:
                    f.write(str(index))
                finally:
                    f.close()

    END________TIME = (datetime.datetime.utcnow() + datetime.timedelta(hours=9)).strftime("%Y%m%d%H%M")
    print "%s:%s" % ("START______TIME", START______TIME)
    print "%s:%s" % ("END________TIME", END________TIME)
    exit(0)

columns = list()
for key in item.keys():
    if type(item[key]) is str:
        columns.append(unicode(item[key], 'utf-8'))
    else:
        columns.append(item[key])
