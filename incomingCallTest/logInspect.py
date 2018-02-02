# -*- coding: utf-8 -*-
import os, sys, time, csv, pprint, sqlite3

orders = (
    "date",
    "time",
    "pid",
    "tid",
    "LogLV",
    "Tag",
    "Message"
)

def uniq(filename):
    dataSet = dict()
    with open(filename) as f:
        linenum = 0
        for line in f:
            row = dict()
            elements = line.split(' ')
            index = 0
            if len(elements) >= len(orders) :
                linenum = linenum + 1
                for i, order in enumerate(orders):
                    while len(elements) > index and elements[index] == '' :
                        index = index + 1
                    if i == (len(orders) - 1) :
                        row[order] = ' '.join(elements[index:])
                    else :
                        row[order] = elements[index]
                    index = index + 1

                #print line
                    #print elements
                # print type(line)
                    #print row
                dataSet[linenum] = row

    for target in range(1, linenum) :
        if dataSet.has_key(target) :
            message = dataSet[target]["Message"]
            duplicate_count = 0
            for l in range(target+1, linenum) :
                if dataSet.has_key(l):
                    if dataSet[l]["Message"] == message :
                        dataSet.pop(l)
                        duplicate_count = duplicate_count + 1
            dataSet[target]["duplicate"] = duplicate_count

    for target in range(1, linenum):
        if dataSet.has_key(target):
            print target, dataSet[target]
            with open("uniq_" + filename, 'a') as f:
                output = ""
                for order in orders:
                    output = output + " " + str(dataSet[target][order])
                try:
                    f.write(str(dataSet[target]["duplicate"]) + "\t" + output)
                except:
                    f.write("None" + "\t" + output)

