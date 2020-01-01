
import csv

import matplotlib

import matplotlib.pyplot as plt

import numpy as np

import pandas as pd



def hot_Time1():

    #根据数据使用折线图

    print('用折线图统计每月数量：')

pr= pd.read_csv(r'C:\Users\w\Desktop\datefile.csv',encoding='ISO-8859-1')
''' print(pr[pr['committer_date'].str.startswith("2019-12")])
    print(pr[pr['committer_date'].str.startswith("2019-11")])
    print(pr[pr['committer_date'].str.startswith("2019-10")])
    print(pr[pr['committer_date'].str.startswith("2019-09")])
    print(pr[pr['committer_date'].str.startswith("2019-08")])
    print(pr[pr['committer_date'].str.startswith("2019-07")])
    print(pr[pr['committer_date'].str.startswith("2019-06")])
    print(pr[pr['committer_date'].str.startswith("2019-05")])
    print(pr[pr['committer_date'].str.startswith("2019-04")])
    print(pr[pr['committer_date'].str.startswith("2019-03")])
    print(pr[pr['committer_date'].str.startswith("2019-02")])
    print(pr[pr['committer_date'].str.startswith("2019-01")])'''

Dec = pr[pr['committer_date'].str.startswith("2019-12")]
Nov = pr[pr['committer_date'].str.startswith("2019-11")]
Oct = pr[pr['committer_date'].str.startswith("2019-10")]
Sept = pr[pr['committer_date'].str.startswith("2019-09")]
Aug = pr[pr['committer_date'].str.startswith("2019-08")]
Jul = pr[pr['committer_date'].str.startswith("2019-07")]
Jun = pr[pr['committer_date'].str.startswith("2019-06")]
May = pr[pr['committer_date'].str.startswith("2019-05")]
Apr = pr[pr['committer_date'].str.startswith("2019-04")]
Mar = pr[pr['committer_date'].str.startswith("2019-03")]
Feb = pr[pr['committer_date'].str.startswith("2019-02")]
Jan = pr[pr['committer_date'].str.startswith("2019-01")]

#绘图显示的标签
month_counts = [ Jan.shape[0],Feb.shape[0], Mar.shape[0], Apr.shape[0], May.shape[0],Jun.shape[0],
              Jul.shape[0], Aug.shape[0],Sept.shape[0],Oct.shape[0],Nov.shape[0],Dec.shape[0]]

pr1= pd.read_csv(r'C:\Users\w\Desktop\datefile.csv',encoding='ISO-8859-1')
''' print(pr[pr['author_date'].str.startswith("2019-12")])
    print(pr[pr['author_datee'].str.startswith("2019-11")])
    print(pr[pr['author_date'].str.startswith("2019-10")])
    print(pr[pr['author_date'].str.startswith("2019-09")])
    print(pr[pr['author_date'].str.startswith("2019-08")])
    print(pr[pr['author_date'].str.startswith("2019-07")])
    print(pr[pr['author_date'].str.startswith("2019-06")])
    print(pr[pr['author_date'].str.startswith("2019-05")])
    print(pr[pr['author_date'].str.startswith("2019-04")])
    print(pr[pr['author_date'].str.startswith("2019-03")])
    print(pr[pr['author_date'].str.startswith("2019-02")])
    print(pr[pr['author_date'].str.startswith("2019-01")])'''

Dec1 = pr[pr['author_date'].str.startswith("2019-12")]
Nov1 = pr[pr['author_date'].str.startswith("2019-11")]
Oct1= pr[pr['author_date'].str.startswith("2019-10")]
Sept1= pr[pr['author_date'].str.startswith("2019-09")]
Aug1 = pr[pr['author_date'].str.startswith("2019-08")]
Jul1 = pr[pr['author_date'].str.startswith("2019-07")]
Jun1 = pr[pr['author_date'].str.startswith("2019-06")]
May1 = pr[pr['author_date'].str.startswith("2019-05")]
Apr1 = pr[pr['author_date'].str.startswith("2019-04")]
Mar1 = pr[pr['author_date'].str.startswith("2019-03")]
Feb1 = pr[pr['author_date'].str.startswith("2019-02")]
Jan1 = pr[pr['author_date'].str.startswith("2019-01")]

#绘图显示的标签
month_counts1 = [ Jan1.shape[0],Feb1.shape[0], Mar1.shape[0], Apr1.shape[0], May1.shape[0],Jun1.shape[0],
              Jul1.shape[0], Aug1.shape[0],Sept1.shape[0],Oct1.shape[0],Nov1.shape[0],Dec1.shape[0]]



    #plt.title('Peak Hours_1',fontsize=15)

plt.xlabel('Month',color='blue')

plt.ylabel('Numbers',color='blue')

    #plt.bar(index+bw, values1_on, bw, alpha=0.7)

x=["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug",
       "Sept","Oct","Nov","Dec"]

plt.plot(x,month_counts,label='committer_date',color='y',linewidth=3.0)

plt.plot(x,month_counts1,label='author_date',color='b',linewidth=2.0)

plt.plot(0,0)

plt.plot(0, 0)

plt.plot(0, 0)

plt.plot(0, 0)

plt.plot(0, 0)

plt.plot(0,0)

plt.plot(0, 0)

plt.plot(0, 0)

plt.plot(0, 0)





plt.grid(alpha=0.3,linestyle=':')

    #plt.xticks()

   # plt.legend(['0~6','6~8','8~10','10~12','12~14','14~16','16~18','18~20','20~24'],

    #           loc=2,edgecolor='b')

plt.legend(loc='best')

plt.show()

print()



if __name__=="__main__":

    hot_Time1()
