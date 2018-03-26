# -*- coding: utf-8 -*-
from common.utils import printEx

SECRETDIALPADs = {
"SM-N900S_samsung_1080x1920_480dpi":
            {'1': (100, 800), '2': (500, 800), '3': (900, 800),
           '4': (100, 950), '5': (500, 950), '6': (900, 950),
           '7': (100, 1100), '8': (500, 1100), '9': (900, 1100),
           '*': (100, 1250), '0': (500, 1250), '#': (900, 1250),
           'keypad': (650, 1550),
           },

"SM-A500S_samsung_720x1280_320dpi":#추측
            {'1': (100, 550), '2': (350, 550), '3': (600, 550),
           '4': (100, 650), '5': (350, 650), '6': (600, 650),
           '7': (100, 750), '8': (350, 750), '9': (600, 750),
           '*': (100, 850), '0': (350, 850), '#': (600, 850),
           'keypad': (450, 1020),
           },

"SM-J530S_samsung_720x1280_320dpi":
            {'1': (100, 550), '2': (350, 550), '3': (600, 550),
           '4': (100, 650), '5': (350, 650), '6': (600, 650),
           '7': (100, 750), '8': (350, 750), '9': (600, 750),
           '*': (100, 850), '0': (350, 850), '#': (600, 850),
           'keypad': (450, 1020),
           },

"SM-G611S_samsung_1080x1920_420dpi":
        {'1': (150, 950), '2': (500, 950), '3': (900, 950),
         '4': (150, 1100), '5': (500, 1100), '6': (900, 1100),
         '7': (150, 1220), '8': (500, 1220), '9': (900, 1220),
         '*': (150, 1350), '0': (500, 1350), '#': (900, 1350),
         'keypad': (650, 1600),
         },

"SM-A720S_samsung_1080x1920_420dpi":
        {'1': (150, 950), '2': (500, 950), '3': (900, 950),
         '4': (150, 1100), '5': (500, 1100), '6': (900, 1100),
         '7': (150, 1220), '8': (500, 1220), '9': (900, 1220),
         '*': (150, 1350), '0': (500, 1350), '#': (900, 1350),
         'keypad': (650, 1600),
         },

"SM-A800S_samsung_1080x1920_480dpi":
            {'1': (100, 800), '2': (500, 800), '3': (900, 800),
           '4': (100, 950), '5': (500, 950), '6': (900, 950),
           '7': (100, 1100), '8': (500, 1100), '9': (900, 1100),
           '*': (100, 1250), '0': (500, 1250), '#': (900, 1250),
           'keypad': (650, 1550),
           },

"SM-G930S_samsung_720x1280_320dpi":
            {'1': (100, 550), '2': (350, 550), '3': (600, 550),
           '4': (100, 650), '5': (350, 650), '6': (600, 650),
           '7': (100, 750), '8': (350, 750), '9': (600, 750),
           '*': (100, 850), '0': (350, 850), '#': (600, 850),
           'keypad': (450, 1000),
           },

"SM-G600S_samsung_720x1280_320dpi":
            {'1': (100, 550), '2': (350, 550), '3': (600, 550),
           '4': (100, 650), '5': (350, 650), '6': (600, 650),
           '7': (100, 750), '8': (350, 750), '9': (600, 750),
           '*': (100, 850), '0': (350, 850), '#': (600, 850),
           'keypad': (450, 1000),
           },

"SM-G930S_samsung_1080x1920_480dpi":
            {'1': (100, 800), '2': (500, 800), '3': (900, 800),
           '4': (100, 950), '5': (500, 950), '6': (900, 950),
           '7': (100, 1100), '8': (500, 1100), '9': (900, 1100),
           '*': (100, 1250), '0': (500, 1250), '#': (900, 1250),
           'keypad': (650, 1550),
           },

"SM-G930S_samsung_1440x2560_640dpi":
            {'1': (200, 1050), '2': (700, 1050), '3': (1200, 1050),
            '4': (200, 1300), '5': (700, 1300), '6': (1200, 1300),
            '7': (200, 1500), '8': (700, 1500), '9': (1200, 1500),
            '*': (200, 1700), '0': (700, 1700), '#': (1200, 1700),
            'keypad': (900, 2050),
            },

"SM-G955N_samsung_720x1480_320dpi":
            {'1': (100, 650), '2': (350, 650), '3': (600, 650),
           '4': (100, 750), '5': (350, 750), '6': (600, 750),
           '7': (100, 850), '8': (350, 850), '9': (600, 850),
           '*': (100, 950), '0': (350, 950), '#': (600, 950),
           'keypad': (450, 1120),
           },

"SM-G955N_samsung_1080x2220_480dpi":
            {'1': (120, 950), '2': (520, 950), '3': (900, 950),
           '4': (120, 1100), '5': (520, 1100), '6': (900, 1100),
           '7': (120, 1300), '8': (520, 1300), '9': (900, 1300),
           '*': (120, 1450), '0': (520, 1450), '#': (900, 1450),
           'keypad': (650, 1700),
           },

"SM-G955N_samsung_1440x2960_640dpi":
            {'1': (150, 1300), '2': (700, 1300), '3': (1200, 1300),
           '4': (150, 1500), '5': (700, 1500), '6': (1200, 1500),
           '7': (150, 1700), '8': (700, 1700), '9': (1200, 1700),
           '*': (150, 1900), '0': (700, 1900), '#': (1200, 1900),
           'keypad': (900, 2300),
           },

"SM-N950N_samsung_720x1480_280dpi":
            {'1': (100, 750), '2': (350, 750), '3': (600, 750),
           '4': (100, 850), '5': (350, 850), '6': (600, 850),
           '7': (100, 950), '8': (350, 950), '9': (600, 950),
           '*': (100, 1050), '0': (350, 1050), '#': (600, 1050),
           'keypad': (450, 1200),
           },

"SM-N950N_samsung_1080x2220_420dpi":
            {'1': (200, 1100), '2': (500, 1100), '3': (800, 1100),
           '4': (200, 1250), '5': (500, 1250), '6': (800, 1250),
           '7': (200, 1400), '8': (500, 1400), '9': (800, 1400),
           '*': (200, 1550), '0': (500, 1550), '#': (800, 1550),
           'keypad': (700, 1750),
           },
"SM-N950N_samsung_1440x2960_560dpi":
            {'1': (150, 1500), '2': (700, 1500), '3': (1200, 1500),
           '4': (150, 1700), '5': (700, 1700), '6': (1200, 1700),
           '7': (150, 1850), '8': (700, 1850), '9': (1200, 1850),
           '*': (150, 2050), '0': (700, 2050), '#': (1200, 2050),
           'keypad': (900, 2350),
           },

"LGM-X320S_LGE_720x1280_320dpi":
            {'1': (100, 450), '2': (350, 450), '3': (600, 450),
             '4': (100, 550), '5': (350, 550), '6': (600, 550),
             '7': (100, 650), '8': (350, 650), '9': (600, 650),
             '*': (100, 750), '0': (350, 750), '#': (600, 750),
             'keypad': (450, 950),
             },

"LG-F720S_LGE_720x1280_320dpi":
            {'1': (100, 450), '2': (350, 450), '3': (600, 450),
             '4': (100, 550), '5': (350, 550), '6': (600, 550),
             '7': (100, 650), '8': (350, 650), '9': (600, 650),
             '*': (100, 750), '0': (350, 750), '#': (600, 750),
             'keypad': (450, 950),
             },

"LG-F500S_LGE_1440x2560_640dpi":
            {'1': (200, 900), '2': (700, 900), '3': (1200, 900),
           '4': (200, 1150), '5': (700, 1150), '6': (1200, 1150),
           '7': (200, 1300), '8': (700, 1300), '9': (1200, 1300),
           '*': (200, 1500), '0': (700, 1500), '#': (1200, 1500),
           'keypad': (900, 1900),
           },

"LGM-X600S_LGE_1080x2160_480dpi":#추측
            {'1': (150, 900), '2': (550, 900), '3': (900, 900),
             '4': (150, 1050), '5': (550, 1050), '6': (900, 1050),
             '7': (150, 1200), '8': (550, 1200), '9': (900, 1200),
             '*': (150, 1400), '0': (550, 1400), '#': (900, 1400),
             'keypad': (680, 1650),
             },
"LG-F370S_LGE_480x800_240dpi":#추측
            {'1': (50, 350), '2': (240, 350), '3': (400, 350),
             '4': (50, 400), '5': (240, 400), '6': (400, 400),
             '7': (50, 450), '8': (240, 450), '9': (400, 450),
             '*': (50, 550), '0': (240, 550), '#': (400, 550),
             'keypad': (300, 600),
             },
"IM-100S_PANTECH_1080x1920_480dpi":
            {'1': (100, 650), '2': (500, 650), '3': (900, 650),
           '4': (100, 850), '5': (500, 850), '6': (900, 850),
           '7': (100, 1000), '8': (500, 1000), '9': (900, 1000),
           '*': (100, 1150), '0': (500, 1150), '#': (900, 1150),
           'keypad': (650, 1400),
           },

"T-1000_TCL_1440x2560_640dpi":
            {'1': (200, 900), '2': (700, 900), '3': (1200, 900),
           '4': (200, 1150), '5': (700, 1150), '6': (1200, 1150),
           '7': (200, 1300), '8': (700, 1300), '9': (1200, 1300),
           '*': (200, 1500), '0': (700, 1500), '#': (1200, 1500),
           'keypad': (900, 1900),
           },
"TG-L900S_Foxconn_1440x2560_560dpi":
            {'1': (150, 1100), '2': (700, 1100), '3': (1200, 1100),
           '4': (150, 1250), '5': (700, 1250), '6': (1200, 1250),
           '7': (150, 1450), '8': (700, 1450), '9': (1200, 1450),
           '*': (150, 1650), '0': (700, 1650), '#': (1200, 1650),
           'keypad': (900, 1950),
           },
"PixelXL_Google_1440x2560_560dpi":
            {'1': (150, 1100), '2': (700, 1100), '3': (1200, 1100),
             '4': (150, 1250), '5': (700, 1250), '6': (1200, 1250),
             '7': (150, 1450), '8': (700, 1450), '9': (1200, 1450),
             '*': (150, 1650), '0': (700, 1650), '#': (1200, 1650),
             'keypad': (900, 1950),
             },
}
def getLocationOnDialPad(selfVersion, appVersion, number, manufacture, model, width, height, density):
    """
        printEx( "%s:%s" % ("number", number) )
        printEx( "%s:%s" % ("manufacture", manufacture) )
        printEx( "%s:%s" % ("model", model) )
        printEx( "%s:%s" % ("width", width) )
        printEx( "%s:%s" % ("height", height) )
        printEx( "%s:%s" % ("density", density) )
        printEx( "%s:%s" % ("appVersion", appVersion) )
        :param selfVersion:
    """
    reVal = None
    requestKey = model + '_' + manufacture + '_' + str(width) + 'x' + str(height) + '_' + str(density) + 'dpi'
    correctKey = None
    while correctKey == None:
        for key in SECRETDIALPADs.keys():
            if requestKey in key:
                correctKey = key
                break

        if correctKey == None:
            if '_' not in requestKey:
                break

            requestKey = requestKey[requestKey.index('_')+1:]

    if correctKey != None:
        reVal = "%s %s" % (str(SECRETDIALPADs[correctKey][number][0]), str(SECRETDIALPADs[correctKey][number][1]))

    return reVal

def getLocationOnDialPad(number, key):
    reVal = None

    if key != None:
        reVal = "%s %s" % (str(SECRETDIALPADs[key][number][0]), str(SECRETDIALPADs[key][number][1]))

    return reVal

def getLocationOnMainDialPad(number, key):
    reVal = None

    if key != None:
        reVal = "%s %s" % (str(SECRETDIALPADs[key][number][0]), str(int(SECRETDIALPADs[key][number][1]) + 200))
        # reVal = "%s %s" % (str(SECRETDIALPADs[key][number][0]), str(int(SECRETDIALPADs[key][number][1])))

    return reVal

def getLocationXYOnMainDialPad(number, key, index):
    reVal = None

    if key != None:
        reVal = SECRETDIALPADs[key][number][index]

    return reVal

def getKey4LocationOnDialPad(selfVersion, appVersion, manufacture, model, width, height, density):
    printEx( "%s:%s" % ("manufacture", manufacture) )
    printEx( "%s:%s" % ("model", model) )
    printEx( "%s:%s" % ("width", width) )
    printEx( "%s:%s" % ("height", height) )
    printEx( "%s:%s" % ("density", density) )
    printEx( "%s:%s" % ("appVersion", appVersion) )

    reVal = None
    requestKey = model + '_' + manufacture + '_' + str(width) + 'x' + str(height) + '_' + str(density) + 'dpi'
    while reVal == None:
        for key in SECRETDIALPADs.keys():
            if requestKey in key:
                print ("%s:%s" % (requestKey, key))
                reVal = key
                break

        if reVal == None:
            if '_' not in requestKey:
                break

            requestKey = requestKey[requestKey.index('_')+1:]

    return reVal