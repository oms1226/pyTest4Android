# -*- coding:utf8 -*-
from openpyxl import load_workbook
import unicodedata

wb = load_workbook(filename = '여름1.2_분류함샘플_V5.0.xlsx')
#sheet_ranges = wb['range names']
sheet_ranges = wb['card']
print(sheet_ranges['D121'].value)
