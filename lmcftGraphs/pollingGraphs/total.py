# -*- coding:utf8 -*-
import numpy as np
import csv
import time
from drawnow import drawnow
import matplotlib.pyplot as plt



def createXY(x, y, dates, colors, index_target, index_x, index_y):
    f = open("C:\\_1.pastrecord\\a.40y\\20170222_cywin_Monkey\\summary.txt")
    for row in csv.reader(f, delimiter='\t'):
        print row
        if row[index_target] == "memCheck" and row[index_x] != "" and row[index_y] != "":
            x.append(row[index_x])
            y.append(row[index_y])
            dates.append(row[7])
            colors.append('gray')
    f.close()
    colors[-1] = 'red'

def total():
    x = []
    y = []
    dates = []
    colors = []

    fig = plt.figure(1)

    createXY(x, y, dates, colors, 6, 5, 12)
#    plt.plot(x, y, 'r.')
    plt.scatter(x, y, c=colors)
    ax = fig.add_subplot(111)
    for i, date in enumerate(dates):
        ax.annotate(date[4:8], (x[i], y[i]))

    x=[]
    y=[]
    colors=[]
    fig = plt.figure(2)
    createXY(x, y, dates, colors, 6, 5, 14)
#    plt.plot(x, y, 'r.')
    plt.scatter(x, y, c=colors)
    plt.show()


total()