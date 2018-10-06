#!/usr/bin/python  
# -*- coding: utf-8 -*-
import os, stat, glob, sys
from os import walk
import subprocess
import shutil
from dateutil import parser
import datetime
import codecs
from sys import platform as _platform

reload(sys)
sys.setdefaultencoding('utf-8')

def getTableLastTimeInDB(tablename):
    reVal = None
    fd_popen = subprocess.Popen("""mysql -uroot -p0000  -e "SELECT UPDATE_TIME FROM INFORMATION_SCHEMA.TABLES WHERE table_schema='%s';""" % tablename, stdout=subprocess.PIPE).stdout
    while 1:
       line = fd_popen.readline()
       if not line :
           break
       elif ('NULL' in line) or ('----' in line) or  ('UPDATE_TIME' in line) :
           pass
       else:
           printEx("%s:%s" % ("line", line))
           dt = parser.parse(line)
           reVal = dt.strftime("%Y%m%d%H%M%S")
           break
    fd_popen.close()

    return reVal

def execMysqlDump(filefullname):
    reVal = None

    if os.path.exists(filefullname):
        os.unlink(filefullname)
    printEx('start::mysqldump'),
    os.system("""mysqldump -uroot -p0000 my_wiki > %s""" % filefullname)
    printEx('end::mysqldump')

    if os.path.exists(filefullname):
        reVal = 'mysqldump success!'
    else:
        reVal = 'mysqldump fail!'

    return reVal

def execMysqlUpdate(filefullname):
    reVal = None

    p_lastTimeInDB = getTableLastTimeInDB(TABLE_NAME)
    printEx('start::mysql-update'),
    os.system("""mysql -uroot -p0000 my_wiki < %s""" % filefullname)
    printEx('end::mysql-update')
    lastTimeInDB = getTableLastTimeInDB(TABLE_NAME)

    if p_lastTimeInDB == lastTimeInDB:
        reVal = 'mysql-update fail!'
    else:
        reVal = 'mysql-update success!'

    return reVal


def readFileAboutTableLastTimeInDB(filefullname):
    reVal = None

    if os.path.exists(filefullname):
        with open(filefullname, 'r') as f:
            while True:
                line = f.readline().replace('\r', '').replace('\n', '')
                if not line: break
                reVal = line
            f.close()

    return reVal

def getDateFromDBFileNameInCloudBerry(filefullname):
    reVal = None
    if os.path.exists(filefullname):
        #reVal = filefullname.split('.')[-1]
        reVal = filefullname.split('.')[2]


    return reVal

def readFileAboutTableLastTimeInCloudBerry(dirname):
    reVal = None

    if os.path.exists(dirname):
        for (dirpath, dirnames, filenames) in walk(dirname):
            for filename in filenames:
                filefullname = os.path.join(dirpath, filename)
                if CLOUDBERRY_MYSQL_FULLFILENAME_PREFIX in filefullname and '.backup' not in filefullname and '.current' not in filefullname:
                    lastTimeInCloud = getDateFromDBFileNameInCloudBerry(filefullname)

                    if reVal == None:
                        reVal = lastTimeInCloud
                    elif int(lastTimeInCloud) > int(reVal):
                        reVal = lastTimeInCloud
    else:
        reVal = 'notFound'

    return reVal

def writeFileAboutTableLastTimeInDB(filefullname, content):
    reVal = None

    if os.path.exists(filefullname):
        os.unlink(filefullname)

    with open(filefullname, 'w') as f:
        f.write(content)
        f.close()

    reVal = readFileAboutTableLastTimeInDB(filefullname)
    if content != reVal:
        printEx("%s:%s" % ("content", content))
        printEx("%s:%s" % ("reVal", reVal))
        reVal = 'write fail!'

    return reVal

TABLE_NAME = 'my_wiki'
MIN_DB_SIZE =  250*1024*1024
HISTORY_UPDATEDATEinLOCAL_FILENAME = '%s.latest_updatetime.local' % TABLE_NAME
CLOUDBERRY_MYSQL_DIRECTORY = 'T:\\_wikibackup'
CLOUDBERRY_MYSQL_FULLFILENAME_PREFIX = '%s\\%s.%s' % (CLOUDBERRY_MYSQL_DIRECTORY, TABLE_NAME, 'sql')
CLOUDBERRY_HISTORY_LOG_FILENAME = '%s\\%s.%s' % (CLOUDBERRY_MYSQL_DIRECTORY, TABLE_NAME, 'log')
LOCAL______HISTORY_LOG_FILENAME = '%s\\%s.%s' % ('.', TABLE_NAME, 'log')
WHEREISSCRIPT = None
LOCALHOST_TARGETPATH = None

def printEx (*strs):
    if os.path.exists(CLOUDBERRY_HISTORY_LOG_FILENAME):
        shutil.move(CLOUDBERRY_HISTORY_LOG_FILENAME, LOCAL______HISTORY_LOG_FILENAME)

    tot = ""
    for string in strs:
        if type(string) is str:
            tot += string
        else:
            tot += str(string)
    print tot

    #with open(CLOUDBERRY_HISTORY_LOG_FILENAME, 'a') as f:
    with codecs.open(LOCAL______HISTORY_LOG_FILENAME, 'a', 'utf-8') as f:
        f.write("%s> %s" % (WHEREISSCRIPT, tot) + "\r\n")
        f.close()

    if os.path.exists(LOCAL______HISTORY_LOG_FILENAME):
        shutil.move(LOCAL______HISTORY_LOG_FILENAME, CLOUDBERRY_HISTORY_LOG_FILENAME)

if __name__ == "__main__":
    while len(sys.argv) > 1:
        if len(sys.argv) > 1 and '--where' in sys.argv[1]:
            argfullname = sys.argv[1].split('=')
            if len(argfullname) == 2:
                if argfullname[0] == '--where':
                    WHEREISSCRIPT = argfullname[1]
            sys.argv.pop(1)
        #python DBUpdateAndBackupAfterCheck.py --localhost=/Users/oms1226/Downloads
        elif len(sys.argv) > 1 and '--localhost' in sys.argv[1]:
            argfullname = sys.argv[1].split('=')
            if len(argfullname) == 2:
                if argfullname[0] == '--localhost':
                    LOCALHOST_TARGETPATH = argfullname[1]
            sys.argv.pop(1)
        else:
            sys.argv.pop(1)

    print("%s:%s" % ("WHEREISSCRIPT", WHEREISSCRIPT))
    print("%s:%s" % ("LOCALHOST_TARGETPATH", LOCALHOST_TARGETPATH))
    if LOCALHOST_TARGETPATH != None:
        lastTimeInDB = getTableLastTimeInDB(TABLE_NAME)
        if 'my_wiki.sql' in LOCALHOST_TARGETPATH:
            fileTime = getDateFromDBFileNameInCloudBerry(LOCALHOST_TARGETPATH)
            if lastTimeInDB == None or fileTime == None:
                print("%s:%s" % ("lastTimeInDB", lastTimeInDB))
                print("%s:%s" % ("fileTime", fileTime))
                print("%s:%s" % ("LOCALHOST_ONLY", 'ERROR_DUE_TO_NONE'))
            elif int(lastTimeInDB) >= int(fileTime):
                print("%s:%s" % ("LOCALHOST_ONLY", 'ERROR_DUE_TO_DBisMoreRecent'))
            else:
                print("%s:%s" % ("LOCALHOST_ONLY", 'MY_WIKI_UPDATE'))
                printEx(execMysqlUpdate(LOCALHOST_TARGETPATH))
        else:
            print("%s:%s" % ("LOCALHOST_ONLY", 'MY_WIKI_DUMP'))
            if _platform == "linux" or _platform == "linux2" or _platform == "darwin":
                print(execMysqlDump('%s.%s' % ('%s/%s.%s' % (LOCALHOST_TARGETPATH, TABLE_NAME, 'sql'), lastTimeInDB)))
            elif _platform == "win32" or _platform == "win64":
                print(execMysqlDump('%s.%s' % ('%s\\%s.%s' % (LOCALHOST_TARGETPATH, TABLE_NAME, 'sql'), lastTimeInDB)))


        print("%s:%s" % ("LOCALHOST_ONLY", 'END'))
        exit(0)

    START______TIME = (datetime.datetime.utcnow() + datetime.timedelta(hours=9)).strftime("%Y%m%d%H%M")
    printEx("%s:%s" % ("START______TIME", START______TIME))
    lastTimeInDB = getTableLastTimeInDB(TABLE_NAME)
    printEx("%s:%s" % ("lastTimeInDB", lastTimeInDB))
    lastTimeInCloud = readFileAboutTableLastTimeInCloudBerry(CLOUDBERRY_MYSQL_DIRECTORY)
    printEx("%s:%s" % ("lastTimeInCloud", lastTimeInCloud))
    lastTimeInFile = readFileAboutTableLastTimeInDB(HISTORY_UPDATEDATEinLOCAL_FILENAME)
    printEx("%s:%s" % ("lastTimeInFile", lastTimeInFile))

    if lastTimeInDB == None:
        printEx("Error; %s is not found in local-pc!" % TABLE_NAME)
        ArithmeticError("lastTimeInDB is " + lastTimeInDB)

    if lastTimeInCloud == None:
        printEx(execMysqlDump('%s.%s' % (CLOUDBERRY_MYSQL_FULLFILENAME_PREFIX, lastTimeInDB)))
    elif 'notFound' in lastTimeInCloud:
        printEx("Error; %s is not found!" % CLOUDBERRY_MYSQL_DIRECTORY)
        ArithmeticError("lastTimeInCloud is " + lastTimeInCloud)		
    elif int(lastTimeInCloud) == int(lastTimeInDB):
        printEx("Nothing; lastTimeInCloud is equal to lastTimeInDB!")
        pass
    elif int(lastTimeInCloud) < int(lastTimeInDB):
        is_realLower = False
        if lastTimeInFile == None:
            is_realLower = True
        elif int(lastTimeInFile) < int(lastTimeInDB):
            is_realLower = True
            if os.path.exists(HISTORY_UPDATEDATEinLOCAL_FILENAME):
                os.unlink(HISTORY_UPDATEDATEinLOCAL_FILENAME)
        else:
            printEx("NoneAfterUpdate; lastTimeInDB is not upper to lastTimeInFile!")

        if is_realLower:
            printEx("Update-Cloud; lastTimeInCloud is lower to lastTimeInDB!")
            previous_filefullnameInCloud = '%s.%s' % (CLOUDBERRY_MYSQL_FULLFILENAME_PREFIX, lastTimeInCloud)
            createFilefullname = '%s.%s' % (CLOUDBERRY_MYSQL_FULLFILENAME_PREFIX, lastTimeInDB)
            printEx(execMysqlDump(createFilefullname))
            previous_fileSizeInCloud = os.path.getsize(previous_filefullnameInCloud)
            previous_createFileSize = os.path.getsize(createFilefullname)
            if previous_createFileSize > previous_fileSizeInCloud:
                printEx("correct; %s(%s) is bigger than %s(%s)!" % (createFilefullname, previous_createFileSize, previous_filefullnameInCloud, previous_fileSizeInCloud))
                if os.path.exists(previous_filefullnameInCloud):
                    os.unlink(previous_filefullnameInCloud)
            else:
                printEx("Error; %s is not bigger than %s!" % (createFilefullname, previous_filefullnameInCloud))
                shutil.move('%s' % previous_filefullnameInCloud,
                            '%s.%s' % (previous_filefullnameInCloud, 'backup'))

            if os.path.getsize(createFilefullname) <= MIN_DB_SIZE:
                printEx("Error; %s is not reach to MIN_DB_SIZE(%s)!" % (createFilefullname, MIN_DB_SIZE))
                shutil.move('%s' % createFilefullname,
                            '%s.%s' % (createFilefullname, 'current'))


    elif int(lastTimeInCloud) > int(lastTimeInDB):
        printEx("Update-Cloud; lastTimeInCloud is upper to lastTimeInDB!")
        printEx(execMysqlUpdate('%s.%s' % (CLOUDBERRY_MYSQL_FULLFILENAME_PREFIX, lastTimeInCloud)))
        lastTimeInDB = getTableLastTimeInDB(TABLE_NAME)
        #shutil.move('%s.%s' % (CLOUDBERRY_MYSQL_FULLFILENAME_PREFIX, lastTimeInCloud), '%s.%s' % (CLOUDBERRY_MYSQL_FULLFILENAME_PREFIX, lastTimeInDB))
        #printEx('%s.%s' % (CLOUDBERRY_MYSQL_FULLFILENAME_PREFIX, lastTimeInCloud) + ' to '  + '%s.%s' % (CLOUDBERRY_MYSQL_FULLFILENAME_PREFIX, lastTimeInDB))
        write_result = writeFileAboutTableLastTimeInDB(HISTORY_UPDATEDATEinLOCAL_FILENAME, lastTimeInDB)
        printEx("%s:%s" % ("write_result", write_result))
        pass

    END_________TIME = (datetime.datetime.utcnow() + datetime.timedelta(hours=9)).strftime("%Y%m%d%H%M")
    printEx("%s:%s" % ("END_________TIME", END_________TIME))

    printEx('--------------------------------------------------------------------')    

    exit(0)



    if lastTimeInFile == None:
        write_result = writeFileAboutTableLastTimeInDB(HISTORY_UPDATEDATEinLOCAL_FILENAME, getTableLastTimeInDB(TABLE_NAME))
        printEx("%s:%s" % ("write_result", write_result))
        lastTimeInFile = lastTimeInDB
    elif int(lastTimeInDB) == int(lastTimeInFile) :
        printEx("Nothing; lastTimeInDB is equal to lastTimeInFile!")
        pass
    elif int(lastTimeInDB) < int(lastTimeInFile) :
        ArithmeticError("RefreshFile; lastTimeInDB is lower to lastTimeInFile! --> but, Never occur this case!")
        pass
    elif int(lastTimeInDB) > int(lastTimeInFile) :
        ArithmeticError("CloudUpdate; lastTimeInDB is upper to lastTimeInFile! --> but, Never occur this case!")
        pass

exit(0)
