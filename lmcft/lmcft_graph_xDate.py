# -*- coding:utf8 -*-
import numpy as np
from numpy import asarray
import csv
import time
from drawnow import drawnow
import matplotlib.pyplot as plt
import sys
import datetime

Global_Path = ""
ROWS = []
DATES = {}
LIMITS = 20
ERROR = 'none'

def loadTargetFile(path):
    global ROWS
    global DATES
    ROWS = []
    DATES = {}
    try:
        with open(path, 'rb') as f:
            ROWS = f.readlines()
        count = 0
        for row in ROWS:
            row = row.split("\t")
            if DATES.get(row[7][4:10], False) == False:
                count = count + 1
                DATES[row[7][4:10]] = count

    except:
        print "Unexpected error: ", sys.exc_info()[0], sys.exc_info()[1]


def createXY(target, index_target, type, index_x, index_y, path):
    global ROWS
    global DATES
    global ERROR
    x = []
    y = []
    dates = []
    commits = []
    colors = []

    try:
        #for row in csv.reader(f, delimiter='\t'):
        for row in ROWS:
            row = row.split("\t")
            if index_target >= len(row) or index_x >= len(row) or index_y >= len(row):
                continue
#                if row[index_target] == "preProcessCheck" and row[11] != "none":
#                    continue
#                if row[index_target] == "fuzztest" and row[12] != "none":
#                    continue

            if row[index_target] == 'preProcessCheck' :
                ERROR = row[11]

            if row[index_target].lower() == target.lower() and row[index_x] != "" and row[index_y] != "":
                x.append(DATES.get(row[index_x][4:10]))
                dates.append(row[index_x][4:10])
                if type == "sum":
                    y.append(float(row[index_y])/float(row[9]))
                else:
                    y.append(row[index_y])
                commits.append(row[5])
                colors.append('gray')

        colors[-1] = 'red'
    except:
        print "Unexpected error: ", sys.exc_info()[0], sys.exc_info()[1]
        x.append(0)
        y.append(0)
        dates.append("000000")
        commits.append("0")
        colors.append('red')

    s_index = 0
    if (len(x) - LIMITS) > 0:
        s_index = len(x) - LIMITS

    return x[s_index:], y[s_index:], dates[s_index:], commits[s_index:], colors[s_index:]

def lmcft_graph_xDate():
    global Global_Path
    plt.suptitle("LMCFT(Low-Maintenance Continuousable Fuzz Test)", horizontalalignment ='right', verticalalignment='bottom', fontsize=12)

    #######################################################################################
    ax = plt.subplot(3, 3, 1)
    plt.title('Surfing Activities')
    x, y, dates, commits, colors = createXY("fuzzTest", 6, "num", 7, 13, Global_Path)
    plt.plot(x, y, 'g-', label='current')
    plt.scatter(x, y, c=colors)
    for i, commit in enumerate(commits):
        ax.annotate(y[i], (x[i], y[i]), fontsize=8, rotation='45')

    x, y, dates, commits, colors = createXY("fuzzTest", 6, "num", 7, 14, Global_Path)
    plt.plot(x, y, 'r--', label='max', linewidth=0.5)
    for i, commit in enumerate(commits):
        ax.annotate(y[i], (x[i], y[i]), fontsize=8, rotation='45')

    # ax.set_ylim([min(y), max(y)])
    #    plt.xticks(x, commits)
    plt.xticks(x, dates, rotation='vertical')
    plt.xlabel('date(MH)')
    plt.ylabel('num #')
    plt.grid(True)
    plt.legend(loc='upper left')

    #######################################################################################
    ax = plt.subplot(3, 3, 2)
    plt.title('Polling Count')
    x, y, dates, commits, colors = createXY("fuzzTest", 6, "num", 7, 11, Global_Path)
    plt.plot(x, y, '-', label='fuzz')
    plt.scatter(x, y, c=colors)
    for i, commit in enumerate(commits):
        ax.annotate(y[i], (x[i], y[i]), fontsize=8, rotation='45')

    x, y, dates, commits, colors = createXY("storageCheck", 6, "num", 7, 11, Global_Path)
    plt.plot(x, y, '-', label='storage')
    plt.scatter(x, y, c=colors)
    for i, commit in enumerate(commits):
        ax.annotate(y[i], (x[i], y[i]), fontsize=8, rotation='45')

    x, y, dates, commits, colors = createXY("memCheck", 6, "num", 7, 11, Global_Path)
    plt.plot(x, y, '-', label='mem')
    plt.scatter(x, y, c=colors)
    for i, commit in enumerate(commits):
        ax.annotate(y[i], (x[i], y[i]), fontsize=8, rotation='45')

    x, y, dates, commits, colors = createXY("cpuCheck", 6, "num", 7, 11, Global_Path)
    plt.plot(x, y, '-', label='cpu')
    plt.scatter(x, y, c=colors)
    for i, commit in enumerate(commits):
        ax.annotate(y[i], (x[i], y[i]), fontsize=8, rotation='45')

    x, y, dates, commits, colors = createXY("tcpNetworkCheck", 6, "num", 7, 11, Global_Path)
    plt.plot(x, y, '-', label='network')
    plt.scatter(x, y, c=colors)
    for i, commit in enumerate(commits):
        ax.annotate(y[i], (x[i], y[i]), fontsize=8, rotation='45')

    x, y, dates, commits, colors = createXY("logCheck", 6, "num", 7, 11, Global_Path)
    plt.plot(x, y, '-', label='log')
    plt.scatter(x, y, c=colors)
    for i, commit in enumerate(commits):
        ax.annotate(y[i], (x[i], y[i]), fontsize=8, rotation='45')

#    ax.set_xlim([min(x), max(x)])
    #    plt.xticks(x, commits)
#    locs, lables = plt.xticks()
    plt.xticks(x, dates, rotation='vertical')
    plt.xlabel('date(MH)')
    plt.ylabel('num #')
    plt.grid(True)
    plt.legend(loc='upper left')

    #######################################################################################
    ax = plt.subplot(3, 3, 3)
    plt.title('Generate Messages')
    x, y, dates, commits, colors = createXY("tmessageCheck", 6, "num", 7, 11, Global_Path)
    plt.plot(x, y, '-', linewidth=1.5, label='loopbackMsg')
    plt.scatter(x, y, c=colors)
    for i, commit in enumerate(commits):
        ax.annotate(y[i], (x[i], y[i]), fontsize=8, rotation='45')

    x, y, dates, commits, colors = createXY("tmessageCheck", 6, "num", 7, 13, Global_Path)
#    plt.plot(x, y, '-', label='suspiciousRecvMsg')
    plt.plot(x, y, '-', label='filteredRecvMsg')
    plt.scatter(x, y, c=colors)
    for i, commit in enumerate(commits):
        ax.annotate(y[i], (x[i], y[i]), fontsize=8, rotation='45')

    x, y, dates, commits, colors = createXY("tmessageCheck", 6, "num", 7, 12, Global_Path)
    plt.plot(x, y, '-', label='recvMsg')
    plt.scatter(x, y, c=colors)
    for i, commit in enumerate(commits):
        ax.annotate(y[i], (x[i], y[i]), fontsize=8, rotation='45')

    #ax.set_xlim([min(x), max(x)])
    #    plt.xticks(x, commits)
    plt.xticks(x, dates, rotation='vertical')
    plt.xlabel('date(MH)')
    plt.ylabel('num #')
    plt.grid(True)
    plt.legend(loc='upper left')

    #######################################################################################
    ax = plt.subplot(3, 3, 4)
    plt.title('Lint')

    x, y, dates, commits, colors = createXY("preProcessCheck", 6, "num", 7, 15, Global_Path)
    plt.plot(x, y, 'y-', linewidth=1.5, label='lint warning')
    plt.scatter(x, y, c=colors)
    for i, commit in enumerate(commits):
        ax.annotate("git#"+commit, (x[i], y[i]), fontsize=8, rotation='45')

    x, y, dates, commits, colors = createXY("preProcessCheck", 6, "num", 7, 14, Global_Path)
    plt.plot(x, y, 'r-', label='lint error')
    plt.scatter(x, y, c=colors)
    for i, commit in enumerate(commits):
        ax.annotate(y[i], (x[i], y[i]), fontsize=8, rotation='45')

    if ERROR != 'none' :
        ax.annotate(ERROR, (x[-1], y[-1]), fontsize=15, color='r')

    #ax.set_xlim([min(x), max(x)])
    #    plt.xticks(x, commits)
    plt.xticks(x, dates, rotation='vertical')
    plt.xlabel('date(MH)')
    plt.ylabel('num #')
    plt.grid(True)
    plt.legend(loc='upper left')

    #######################################################################################

    ax = plt.subplot(3, 3, 5)
    plt.title('Storage')

    x, y, dates, commits, colors =  createXY("storageCheck", 6, "avg", 7, 16, Global_Path)
    plt.plot(x, y, '--', label='cache_avg', linewidth=0.3)
    plt.scatter(x, y, c=colors)
    for i, commit in enumerate(commits):
        ax.annotate(int(float(y[i])), (x[i], y[i]), fontsize=8, rotation='45')

    x, y, dates, commits, colors =  createXY("storageCheck", 6, "avg", 7, 17, Global_Path)
    plt.plot(x, y, '--', label='cache_max', linewidth=0.3)
    plt.scatter(x, y, c=colors)
    for i, commit in enumerate(commits):
        ax.annotate(int(float(y[i])), (x[i], y[i]), fontsize=8, rotation='45')

    x, y, dates, commits, colors =  createXY("storageCheck", 6, "avg", 7, 18, Global_Path)
    plt.plot(x, y, '--', label='cache_min', linewidth=0.3)
    plt.scatter(x, y, c=colors)
    for i, commit in enumerate(commits):
        ax.annotate(int(float(y[i])), (x[i], y[i]), fontsize=8, rotation='45')

    x, y, dates, commits, colors =  createXY("storageCheck", 6, "avg", 7, 19, Global_Path)
    plt.plot(x, y, '--', label='cache_init', linewidth=0.3)
    plt.scatter(x, y, c=colors)
    for i, commit in enumerate(commits):
        ax.annotate(int(float(y[i])), (x[i], y[i]), fontsize=8, rotation='45')

    x, y, dates, commits, colors =  createXY("storageCheck", 6, "avg", 7, 12, Global_Path)
    plt.plot(x, y, 'g-', label='total_avg', linewidth=2.0)
    plt.scatter(x, y, c=colors)
    for i, commit in enumerate(commits):
        ax.annotate(int(float(y[i])), (x[i], y[i]), fontsize=8, rotation='45')

    x, y, dates, commits, colors =  createXY("storageCheck", 6, "avg", 7, 13, Global_Path)
    plt.plot(x, y, 'ro--', label='total_max', linewidth=0.5)
#    plt.scatter(x, y, c=colors)
    for i, commit in enumerate(commits):
        ax.annotate(int(float(y[i])), (x[i], y[i]), fontsize=8, rotation='45')

    x, y, dates, commits, colors = createXY("storageCheck", 6, "avg", 7, 15, Global_Path)
    if x[0] != 0:
        plt.plot(x, y, 'yo--', label='total_init', linewidth=1)
        #    plt.scatter(x, y, c=colors)
        for i, commit in enumerate(commits):
            ax.annotate(int(float(y[i])), (x[i], y[i]), fontsize=8, rotation='45')

    x, y, dates, commits, colors = createXY("storageCheck", 6, "avg", 7, 14, Global_Path)
    plt.plot(x, y, 'bo--', label='total_min', linewidth=0.5)
    #    plt.scatter(x, y, c=colors)
    for i, commit in enumerate(commits):
        ax.annotate(int(float(y[i])), (x[i], y[i]), fontsize=8, rotation='45')


    #ax.set_xlim([min(x), max(x)])
    #    plt.xticks(x, commits)
    ax.autoscale_view(scalex=True, scaley=False)
    plt.xticks(x, dates, rotation='vertical')
    plt.xlabel('date(MH)')
    plt.ylabel('size(kb,avg)')
    plt.grid(True)
    plt.legend(loc='upper left')

    #######################################################################################

    ax = plt.subplot(3, 3, 6)
    plt.title('Memory')
    x, y, dates, commits, colors =  createXY("memCheck", 6, "avg", 7, 12, Global_Path)
    plt.plot(x, y, 'g-', label='avg', linewidth=2.0)
    plt.scatter(x, y, c=colors)
    for i, commit in enumerate(commits):
        ax.annotate(int(float(y[i])), (x[i], y[i]), fontsize=8, rotation='45')

    x, y, dates, commits, colors = createXY("memCheck", 6, "avg", 7, 13, Global_Path)
    plt.plot(x, y, 'r--', label='max', linewidth=0.5)
    #    plt.scatter(x, y, c=colors)
    for i, commit in enumerate(commits):
        ax.annotate(int(float(y[i])), (x[i], y[i]), fontsize=8, rotation='45')

    x, y, dates, commits, colors = createXY("memCheck", 6, "avg", 7, 14, Global_Path)
    plt.plot(x, y, 'b--', label='min', linewidth=0.5)
    #    plt.scatter(x, y, c=colors)
    for i, commit in enumerate(commits):
        ax.annotate(int(float(y[i])), (x[i], y[i]), fontsize=8, rotation='45')

    #ax.set_xlim([min(x), max(x)])
    #    plt.xticks(x, commits)
    plt.xticks(x, dates, rotation='vertical')
    plt.xlabel('date(MH)')
    plt.ylabel('heap mem(kb,avg)')
    plt.grid(True)
    plt.legend(loc='upper left')

    #######################################################################################

    ax = plt.subplot(3, 3, 7)
    plt.title('CPU')
    x, y, dates, commits, colors =  createXY("cpuCheck", 6, "sum", 7, 15, Global_Path)
    plt.plot(x, y, '.-')
    plt.scatter(x, y, c=colors)
    for i, commit in enumerate(commits):
        ax.annotate(int(float(y[i])), (x[i], y[i]), fontsize=8, rotation='45')

    #ax.set_xlim([min(x), max(x)])
    #    plt.xticks(x, commits)
    plt.xticks(x, dates, rotation='vertical')
    plt.xlabel('date(MH)')
    plt.ylabel('cpu(%,sum/hour)')
    plt.grid(True)
    plt.legend(loc='upper left')

#######################################################################################
    ax = plt.subplot(3, 3, 8)
    plt.title('tcp network')
    x, y, dates, commits, colors = createXY("tcpNetworkCheck", 6, "sum", 7, 15, Global_Path)
    plt.plot(x, y, '-', linewidth=1.5, label='recv')
    plt.scatter(x, y, c=colors)
    for i, commit in enumerate(commits):
        ax.annotate(int(float(y[i])), (x[i], y[i]), fontsize=8, rotation='45')

    x, y, dates, commits, colors = createXY("tcpNetworkCheck", 6, "sum", 7, 19, Global_Path)
    plt.plot(x, y, '-', label='send')
    plt.scatter(x, y, c=colors)
    for i, commit in enumerate(commits):
        ax.annotate(int(float(y[i])), (x[i], y[i]), fontsize=8, rotation='45')

    #ax.set_xlim([min(x), max(x)])
    #    plt.xticks(x, commits)
    plt.xticks(x, dates, rotation='vertical')
    plt.xlabel('date(MH)')
    plt.ylabel('date(bytes,sum/hour)')
    plt.grid(True)
    plt.legend(loc='upper left')

#######################################################################################
    ax = plt.subplot(3, 3, 9)
    plt.title('log')

    x, y, dates, commits, colors = createXY("logCheck", 6, "num", 7, 14, Global_Path)
    plt.plot(x, y, 'b-', label='errorUniqWords')
    plt.scatter(x, y, c=colors)
    for i, commit in enumerate(commits):
        ax.annotate(int(float(y[i])), (x[i], y[i]), fontsize=8, rotation='45')

    x, y, dates, commits, colors = createXY("logCheck", 6, "num", 7, 15, Global_Path)
    #plt.plot(x, y, 'g-', label='pid')
    #plt.scatter(x, y, c=colors)
    for i, commit in enumerate(commits):
        #pid#
        pid = str('p#') + str(int(float(y[i])))
        y_1 = int(y[i]) + 40000
        ax.annotate(pid, (x[i], y_1), fontsize=7, rotation='45')

    x, y, dates, commits, colors = createXY("logCheck", 6, "num", 7, 12, Global_Path)
    plt.plot(x, y, 'r-', linewidth=1.5, label='crash')
    plt.scatter(x, y, c=colors)
    for i, commit in enumerate(commits):
        ax.annotate(int(float(y[i])), (x[i], y[i]), fontsize=8, rotation='45')

    x, y, dates, commits, colors = createXY("logCheck", 6, "num", 7, 13, Global_Path)
    plt.plot(x, y, 'y-', label='error')
    plt.scatter(x, y, c=colors)
    for i, commit in enumerate(commits):
        ax.annotate(int(float(y[i])), (x[i], y[i]), fontsize=8, rotation='45')

    #ax.set_xlim([min(x), max(x)])
    #    plt.xticks(x, commits)
    plt.xticks(x, dates, rotation='vertical')
    plt.xlabel('date(MH)')
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
    loadTargetFile(Global_Path)
    drawnow(lmcft_graph_xDate)

    while True:
        loadTargetFile(Global_Path)
        drawnow(lmcft_graph_xDate)
        print ("draw complete!")
        print (datetime.datetime.now())
        print (pause_seconds)
        plt.pause(int(pause_seconds))
    #    time.sleep(1)
