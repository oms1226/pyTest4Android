# -*- coding:utf8 -*-
import numpy as np
import csv
import time
from drawnow import drawnow
import matplotlib.pyplot as plt

def lint():
    print "lint"
    x = []
    y = []
    colors = []
    f = open("C:\\_1.pastrecord\\a.40y\\20170222_cywin_Monkey\\summary.txt")
    for row in csv.reader(f, delimiter='\t'):
        print row
        if row[6] == "preProcessCheck":
            x.append(row[5])
            y.append(row[14])
            colors.append('gray')
    colors[-1] = 'red'
    f.close()
    print y
    plt.plot(x, y, 'r.')
    #  plt.axis([-1, 30, -5,1 ])
    plt.ion()
    plt.show()
    time.sleep(10)
    plt.close()