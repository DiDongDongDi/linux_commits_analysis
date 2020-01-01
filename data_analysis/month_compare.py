import pandas as pd
import csv
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from pyecharts import Pie
from pyecharts import Geo, Bar, Page, Bar3D
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

month=["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug",
       "Sept","Oct","Nov","Dec"]
colors=['y','m','y','m','y','m','y','m','y','m','y','m','y','m']
explode=[0,0.1,0,0.1,0,0.1,0,0.1,0,0.1,0,0.1]
'''#旋转角度
plt.title("commits of month_counts",fontsize=25)
#标题
plt.pie(month_counts,labels= month,explode=explode,colors=colors,
        startangle = 180,
        shadow=True)
plt.axis('equal')
plt.show()'''


pie = Pie('Github每月提交commits对比饼图',

          title_pos='center',

          width=900,

)

pie.add('',

        month,

        month_counts,

        is_label_show=True,

        legend_pos='left',

        legend_orient="vertical",

        radius=[20, 60],

)

 

pie.render('月份统计饼图.html')





   # 柱状统计

bar = Bar(

              "每月提交数量统计",

              "数据来源：guthub",

              # title_color="#fff",

              title_pos="center",

              width=1200,

              height=600,

    )


bar.add('',

           month,

           month_counts,

            is_label_show=True,

            is_visualmap=True,

    )

bar.render('每月提交量统计—柱状图.html')




    







