# -*- coding:utf8 -*-
import numpy as np
import csv
import time
from drawnow import drawnow
import matplotlib.pyplot as plt
import sys
import datetime

Global_Path = ""

def createXY(target, index_target, type, index_x, index_y, path):
    x = []
    y = []
    dates = []
    colors = []

    try:
        with open(path, 'rb') as f:
            for row in csv.reader(f, delimiter='\t'):
                print row
                if index_target >= len(row) or index_x >= len(row) or index_y >= len(row):
                    continue
                if row[index_target] == target and row[index_x] != "" and row[index_y] != "":
                    x.append(int(row[index_x]))
                    if type == "sum":
                        y.append(float(row[index_y])/float(row[9]))
                    else:
                        y.append(row[index_y])
                    dates.append(row[7])
                    colors.append('gray')

        colors[-1] = 'red'
    except:
        print "Unexpected error: ", sys.exc_info()[0], sys.exc_info()[1]
        x.append(0)
        y.append(0)
        dates.append("197701010000")
        colors.append('red')

    return x, y, dates, colors

def lmcft_graph():
    global Global_Path
    plt.suptitle("LMCFT(Low-Maintenance Continuousable Fuzz Test)", horizontalalignment ='right', verticalalignment='bottom', fontsize=12)

    #######################################################################################
    ax = plt.subplot(3, 3, 1)
    plt.title('Surfing Activities')
    x, y, dates, colors = createXY("fuzzTest", 6, "num", 5, 13, Global_Path)
    plt.plot(x, y, 'g-', label='current')
    plt.scatter(x, y, c=colors)
    for i, date in enumerate(dates):
        ax.annotate(date[4:10], (x[i], y[i]))

    x, y, dates, colors = createXY("fuzzTest", 6, "num", 5, 14, Global_Path)
    plt.plot(x, y, 'r--', label='max', linewidth=0.5)
    for i, date in enumerate(dates):
        ax.annotate(date[4:10], (x[i], y[i]))

    ax.set_xlim([min(x), max(x)])
    #    plt.xticks(x, dates)
    plt.xticks(x, x)
    plt.xlabel('git commit#')
    plt.ylabel('num #')
    plt.grid(True)
    plt.legend(loc='upper left')

    #######################################################################################
    ax = plt.subplot(3, 3, 2)
    plt.title('Polling Count')
    x, y, dates, colors = createXY("fuzzTest", 6, "num", 5, 11, Global_Path)
    plt.plot(x, y, '-', label='fuzz')
    plt.scatter(x, y, c=colors)
    for i, date in enumerate(dates):
        ax.annotate(date[4:10], (x[i], y[i]))

    x, y, dates, colors = createXY("storageCheck", 6, "num", 5, 11, Global_Path)
    plt.plot(x, y, '-', label='storage')
    plt.scatter(x, y, c=colors)
    for i, date in enumerate(dates):
        ax.annotate(date[4:10], (x[i], y[i]))

    x, y, dates, colors = createXY("memCheck", 6, "num", 5, 11, Global_Path)
    plt.plot(x, y, '-', label='mem')
    plt.scatter(x, y, c=colors)
    for i, date in enumerate(dates):
        ax.annotate(date[4:10], (x[i], y[i]))

    x, y, dates, colors = createXY("cpuCheck", 6, "num", 5, 11, Global_Path)
    plt.plot(x, y, '-', label='cpu')
    plt.scatter(x, y, c=colors)
    for i, date in enumerate(dates):
        ax.annotate(date[4:10], (x[i], y[i]))

    x, y, dates, colors = createXY("tcpNetworkCheck", 6, "num", 5, 11, Global_Path)
    plt.plot(x, y, '-', label='network')
    plt.scatter(x, y, c=colors)
    for i, date in enumerate(dates):
        ax.annotate(date[4:10], (x[i], y[i]))

    x, y, dates, colors = createXY("logCheck", 6, "num", 5, 11, Global_Path)
    plt.plot(x, y, '-', label='log')
    plt.scatter(x, y, c=colors)
    for i, date in enumerate(dates):
        ax.annotate(date[4:10], (x[i], y[i]))

    ax.set_xlim([min(x), max(x)])
    #    plt.xticks(x, dates)
    plt.xticks(x, x)
    plt.xlabel('git commit#')
    plt.ylabel('data(bytes,sum/hour)')
    plt.grid(True)
    plt.legend(loc='upper left')

    #######################################################################################
    ax = plt.subplot(3, 3, 3)
    plt.title('Generate Messages')
    x, y, dates, colors = createXY("tmessageCheck", 6, "num", 5, 11, Global_Path)
    plt.plot(x, y, '-', linewidth=1.5, label='loopbackMsg')
    plt.scatter(x, y, c=colors)
    for i, date in enumerate(dates):
        ax.annotate(date[4:10], (x[i], y[i]))

    x, y, dates, colors = createXY("tmessageCheck", 6, "num", 5, 13, Global_Path)
    plt.plot(x, y, '-', label='suspiciousRecvMsg')
    plt.scatter(x, y, c=colors)
    for i, date in enumerate(dates):
        ax.annotate(date[4:10], (x[i], y[i]))

    x, y, dates, colors = createXY("tmessageCheck", 6, "num", 5, 12, Global_Path)
    plt.plot(x, y, '-', label='recvMsg')
    plt.scatter(x, y, c=colors)
    for i, date in enumerate(dates):
        ax.annotate(date[4:10], (x[i], y[i]))

    ax.set_xlim([min(x), max(x)])
    #    plt.xticks(x, dates)
    plt.xticks(x, x)
    plt.xlabel('git commit#')
    plt.ylabel('num #')
    plt.grid(True)
    plt.legend(loc='upper left')

    #######################################################################################
    ax = plt.subplot(3, 3, 4)
    plt.title('Lint')
    x, y, dates, colors = createXY("preProcessCheck", 6, "num", 5, 15, Global_Path)
    plt.plot(x, y, 'y-', linewidth=1.5, label='warning')
    plt.scatter(x, y, c=colors)
    for i, date in enumerate(dates):
        ax.annotate(date[4:10], (x[i], y[i]))

    x, y, dates, colors = createXY("preProcessCheck", 6, "num", 5, 14, Global_Path)
    plt.plot(x, y, 'r-', label='error')
    plt.scatter(x, y, c=colors)
    for i, date in enumerate(dates):
        ax.annotate(date[4:10], (x[i], y[i]))

    ax.set_xlim([min(x), max(x)])
    #    plt.xticks(x, dates)
    plt.xticks(x, x)
    plt.xlabel('git commit#')
    plt.ylabel('num #')
    plt.grid(True)
    plt.legend(loc='upper left')

    #######################################################################################

    ax = plt.subplot(3, 3, 5)
    plt.title('Storage')
    x, y, dates, colors =  createXY("storageCheck", 6, "avg", 5, 12, Global_Path)
    plt.plot(x, y, 'g-', label='avg', linewidth=2.0)
    plt.scatter(x, y, c=colors)
    for i, date in enumerate(dates):
        ax.annotate(date[4:10], (x[i], y[i]))

    x, y, dates, colors =  createXY("storageCheck", 6, "avg", 5, 13, Global_Path)
    plt.plot(x, y, 'r--', label='max', linewidth=0.5)
#    plt.scatter(x, y, c=colors)
    for i, date in enumerate(dates):
        ax.annotate(date[4:10], (x[i], y[i]))

    x, y, dates, colors = createXY("storageCheck", 6, "avg", 5, 14, Global_Path)
    plt.plot(x, y, 'b--', label='min', linewidth=0.5)
    #    plt.scatter(x, y, c=colors)
    for i, date in enumerate(dates):
        ax.annotate(date[4:10], (x[i], y[i]))

    ax.set_xlim([min(x), max(x)])
    #    plt.xticks(x, dates)
    plt.xticks(x, x)
    plt.xlabel('git commit#')
    plt.ylabel('size(kb,avg)')
    plt.grid(True)
    plt.legend(loc='upper left')

    #######################################################################################

    ax = plt.subplot(3, 3, 6)
    plt.title('Memory')
    x, y, dates, colors =  createXY("memCheck", 6, "avg", 5, 12, Global_Path)
    plt.plot(x, y, 'g-', label='avg', linewidth=2.0)
    plt.scatter(x, y, c=colors)
    for i, date in enumerate(dates):
        ax.annotate(date[4:10], (x[i], y[i]))

    x, y, dates, colors = createXY("memCheck", 6, "avg", 5, 13, Global_Path)
    plt.plot(x, y, 'r--', label='max', linewidth=0.5)
    #    plt.scatter(x, y, c=colors)
    for i, date in enumerate(dates):
        ax.annotate(date[4:10], (x[i], y[i]))

    x, y, dates, colors = createXY("memCheck", 6, "avg", 5, 14, Global_Path)
    plt.plot(x, y, 'b--', label='min', linewidth=0.5)
    #    plt.scatter(x, y, c=colors)
    for i, date in enumerate(dates):
        ax.annotate(date[4:10], (x[i], y[i]))

    ax.set_xlim([min(x), max(x)])
    #    plt.xticks(x, dates)
    plt.xticks(x, x)
    plt.xlabel('git commit#')
    plt.ylabel('heap mem(kb,avg)')
    plt.grid(True)
    plt.legend(loc='upper left')

    #######################################################################################

    ax = plt.subplot(3, 3, 7)
    plt.title('CPU')
    x, y, dates, colors =  createXY("cpuCheck", 6, "sum", 5, 15, Global_Path)
    plt.plot(x, y, '.-')
    plt.scatter(x, y, c=colors)
    for i, date in enumerate(dates):
        ax.annotate(date[4:10], (x[i], y[i]))

    ax.set_xlim([min(x), max(x)])
    #    plt.xticks(x, dates)
    plt.xticks(x, x)
    plt.xlabel('git commit#')
    plt.ylabel('cpu(%,sum/hour)')
    plt.grid(True)
    plt.legend(loc='upper left')

#######################################################################################
    ax = plt.subplot(3, 3, 8)
    plt.title('tcp network')
    x, y, dates, colors = createXY("tcpNetworkCheck", 6, "sum", 5, 14, Global_Path)
    plt.plot(x, y, '-', linewidth=1.5, label='recv')
    plt.scatter(x, y, c=colors)
    for i, date in enumerate(dates):
        ax.annotate(date[4:10], (x[i], y[i]))

    x, y, dates, colors = createXY("tcpNetworkCheck", 6, "sum", 5, 17, Global_Path)
    plt.plot(x, y, '-', label='send')
    plt.scatter(x, y, c=colors)
    for i, date in enumerate(dates):
        ax.annotate(date[4:10], (x[i], y[i]))

    ax.set_xlim([min(x), max(x)])
    #    plt.xticks(x, dates)
    plt.xticks(x, x)
    plt.xlabel('git commit#')
    plt.ylabel('date(bytes,sum/hour)')
    plt.grid(True)
    plt.legend(loc='upper left')

#######################################################################################
    ax = plt.subplot(3, 3, 9)
    plt.title('log')
    x, y, dates, colors = createXY("logCheck", 6, "num", 5, 12, Global_Path)
    plt.plot(x, y, 'r-', linewidth=1.5, label='error')
    plt.scatter(x, y, c=colors)
    for i, date in enumerate(dates):
        ax.annotate(date[4:10], (x[i], y[i]))

    x, y, dates, colors = createXY("logCheck", 6, "num", 5, 13, Global_Path)
    plt.plot(x, y, 'y-', label='crash')
    plt.scatter(x, y, c=colors)
    for i, date in enumerate(dates):
        ax.annotate(date[4:10], (x[i], y[i]))

    ax.set_xlim([min(x), max(x)])
    #    plt.xticks(x, dates)
    plt.xticks(x, x)
    plt.xlabel('git commit#')
    plt.ylabel('data(bytes,sum/hour)')
    plt.grid(True)
    plt.legend(loc='upper left')

    #######################################################################################

    plt.tight_layout()
#    plt.show()

if __name__ == '__main__':
    if len(sys.argv) > 1:
        Global_Path = sys.argv[1]
    else:
        Global_Path = "C:\\_1.pastrecord\\a.40y\\20170222_cywin_Monkey\\summary.txt"

    print (Global_Path)

    pause_seconds=10
    if len(sys.argv) > 2:
        pause_seconds = sys.argv[2]

    mng = plt.get_current_fig_manager()
    mng.full_screen_toggle()

    while True:
        drawnow(lmcft_graph)
        print ("draw complete!")
        print (datetime.datetime.now())
        print (pause_seconds)
        plt.pause(int(pause_seconds))
    #    time.sleep(1)
