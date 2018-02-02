
selfVersion = '1.0.0'
LMCFT_FOLDER_FAIL = 'D:\\lmcft_log\\fail\\'
LMCFT_FOLDER_TRACKING = 'D:\\lmcft_log\\tracking\\'
LMCFT_FOLDER_RESULT = 'D:\\lmcft_log\\result\\'
LMCFT_EXEC_HISTORY = 'D:\\lmcft_log\\history.log'

class setting:
    DEBUG = False

def setDEBUG(value):
    setting.DEBUG = value

def DEBUG():
    return  setting.DEBUG

if __name__ == "__main__":
    print("%s:%s" % ("DEBUG", setting.DEBUG))
    setDEBUG(True)
    print("%s:%s" % ("DEBUG", setting.DEBUG))
