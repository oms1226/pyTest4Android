# -*- coding:utf8 -*-
from openpyxl import load_workbook
import random
import unicodedata

import sys
reload(sys)
sys.setdefaultencoding('utf8')

SHEETS = [
['yorum_sample_V5.0.xlsx', 'card1', 'C', 'D', 6, 307],
['yorum_sample_V5.0.xlsx', 'card2', 'C', 'D', 6, 230],
['yorum_sample_V5.0.xlsx', 'card3', 'C', 'D', 6, 20],
['yorum_sample_V5.0.xlsx', 'card4', 'C', 'D', 6, 56],
['yorum_sample_V5.0.xlsx', 'card5', 'C', 'D', 7, 145],
['yorum_sample_V5.0.xlsx', 'delivery', 'C', 'D', 6, 408],
['yorum_sample_V5.0.xlsx', 'auth', 'C', 'D', 6, 86],
['yorum_sample_V5.0.xlsx', 'shopping', 'C', 'D', 6, 65],
['yorum_sample_commercial.xlsx', '홍보성 문자', 'C', 'E', 3, 3979],
]


#sheet_ranges = wb['range names']
SHEET = SHEETS[random.randrange(0, len(SHEETS))]
#SHEET = SHEETS[8]
wb = load_workbook(filename = SHEET[0])


ADDRESS = None
MESSAGE = None

while ADDRESS == None and MESSAGE == None :
    try:
        sheet_ranges = wb[SHEET[1]]
        column_index = random.randrange(SHEET[4], SHEET[5]+1)
        ADDRESS = sheet_ranges[SHEET[2]+str(column_index)].value
        MESSAGE = sheet_ranges[SHEET[3]+str(column_index)].value
    except:
        print "Unexpected error: ", sys.exc_info()[0], sys.exc_info()[1]

#print MESSAGE
#MESSAGE = MESSAGE.replace("[Web발신]", "").replace("_", "").replace("\r", "").replace("\n", "")
MESSAGE = MESSAGE.replace("_", "").replace("\r", "").replace("\n", "")
print "ADDRESS:" + str(ADDRESS) + "_MESSAGE:" + MESSAGE
