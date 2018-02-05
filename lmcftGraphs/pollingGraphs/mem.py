#https://sungyongchoi.wordpress.com/2016/02/02/csv-%ED%8C%8C%EC%9D%BC%EC%9D%84-%EC%9D%BD%EC%96%B4-%EC%B0%A8%ED%8A%B8-%EA%B7%B8%EB%A6%AC%EA%B8%B0/

import numpy as np
import csv
import time
from drawnow import drawnow
import matplotlib.pyplot as plt



def mem():
  def makeFig():
    plt.title("mem average(kb)", fontsize=18)
    plt.xlabel("date", fontsize=10)  # y=1.05
    plt.ylabel("average", fontsize=10)  # y=1.05
    plt.scatter(x, y, c=colors)  # I think you meant this

  while True:
    x=[]
    y=[]
    colors=[]
    f= open("C:\\_1.pastrecord\\a.40y\\20170222_cywin_Monkey\\summary.txt")
    for row in csv.reader(f, delimiter='\t'):
      print row
      if row[6] == "memCheck" and row[5] != "" and row[12] != "":
        x.append(row[5])
        y.append(row[12])
        colors.append('gray')
    colors[-1]='red'
    f.close()
    print y
    drawnow(makeFig)
    plt.pause(0.001)
    print "draw complete!"
    time.sleep(10)
  #  plt.plot(x, y, 'r.')
  #  plt.axis([-1, 30, -5,1 ])
  #  plt.show()


mem()