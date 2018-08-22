# -*- coding: utf-8 -*-
#!/usr/bin/python
import datetime
import threading

from common.contant import *
from common.deviceInfo import *
from os import walk
import shutil

def inspectAndRefactoring(path):
    for (dirpath, dirnames, filenames) in walk(path):
        print("%s:%s" % ("dirpath", dirpath))
        print("%s:%s" % ("dirnames", dirnames))
        print("%s:%s" % ("filenames", filenames))
        for filename in filenames:
            filefullname = os.path.join(dirpath, filename)

            if filefullname.endswith('.backup'):
                os.unlink(filefullname)
                continue
            with codecs.open(filefullname, 'r') as f:
                while 1:
                    line = f.readline()
                    if not line: break

                    line = line.replace('geo_point', 'location')

                    if 'goog' in line:
                        words = line.split(' ')
                        index = 0
                        for word in words:
                            if (index > 0) and (type(words[index-1]) is str) and ('goog' in words[index-1]) and word.endswith(','):
                                newWord = None
                                try:
                                    newWord = int(word.replace('"', '').replace(',', ''))
                                except ValueError as verr:
                                    try:
                                        newWord = float(word.replace('"', '').replace(',', ''))
                                    except ValueError as verr:
                                        if word.replace('"', '').replace(',', '') == 'true' or word.replace('"', '').replace(',', '') == 'false':
                                            newWord = word.replace('"', '').replace(',', '')

                                if newWord != None:
                                    words[index] = str(newWord) + ','
                            index = index + 1
                        line = ' '.join(words)

                    with codecs.open(filefullname + '.backup', 'a') as fw:
                        fw.write(line)
                        fw.close()
                f.close()
            if os.path.exists(filefullname + '.backup'):
                os.unlink(filefullname)
                shutil.move(filefullname + '.backup', filefullname)



if __name__ == "__main__":
    inspectAndRefactoring('.\\data')
    pass