# database operations
import pymongo
client = pymongo.MongoClient(host='wangqy.top', port=27017)
db = client.linux_commits_analysis
users = db.users
commits = db.commits
db.authenticate('share', 'shareshare')

# data analysis
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib
from pyecharts.charts import Bar
from pyecharts import options as opts
from datetime import timedelta

# 统计torvalds不同时间段的提交数
torvalds_commit_date = commits.find({'committer_login': 'torvalds'}, {'_id': 0, 'committer_date': 1})
torvalds_commit_hour_count = [0, 0, 0, 0, 0, 0,
                                0, 0, 0, 0, 0, 0,
                                0, 0, 0, 0, 0, 0,
                                0, 0, 0, 0, 0, 0]
for date in torvalds_commit_date:
    torvalds_commit_hour_count[date['committer_date'].hour] += 1

# 调整时区
# python复制list
torvalds_commit_hour_count_old = torvalds_commit_hour_count[:]
for i in range(24):
    torvalds_commit_hour_count[i-8] = torvalds_commit_hour_count_old[i]

#  # 下面是用matplotlib实现的, 后面换成了pyecharts
#  # 画柱状图
#  # 设置中文字体和负号正常显示
#  matplotlib.rcParams['font.sans-serif'] = ['WenQuanYi Micro Hei']
#  matplotlib.rcParams['axes.unicode_minus'] = False

#  plt.barh(range(24), torvalds_commit_hour_count)
#  plt.ylabel('时间点')
#  plt.xlabel('提交次数')
#  plt.title('Linus提交时间分布')
#  ax = plt.gca()# 获取到当前坐标轴信息
#  ax.xaxis.set_ticks_position('top')# 将X坐标轴移到上面
#  ax.invert_yaxis()# 反转Y坐标轴
#  plt.show()

# 使用pyecharts实现, 并保存为html
hours = list(range(24))
hours.reverse()
torvalds_commit_hour_count.reverse()
bar = (
    Bar()
    .add_xaxis(hours)
    .add_yaxis('提交次数', torvalds_commit_hour_count)
    .reversal_axis()
    .set_series_opts(label_opts=opts.LabelOpts(position="right"))
    .set_global_opts(title_opts=opts.TitleOpts(title='Linus提交小时分布'))
)
bar.render('Linus_hour_commit.html')

# 统计分析不同星期的提交情况
torvalds_commit_date = commits.find({'committer_login': 'torvalds'}, {'_id': 0, 'committer_date': 1})
# 从星期日开始
torvalds_commit_week_count = [0, 0, 0, 0,
                                0, 0, 0]
for date in torvalds_commit_date:
    real_date = date['committer_date'] - timedelta(hours=8)
    torvalds_commit_week_count[real_date.weekday()] += 1

# 使用pyecharts可视化
weeks = ['星期日', '星期一', '星期二', '星期三', '星期四', '星期五', '星期六']
bar = (
    Bar()
    .add_xaxis(weeks)
    .add_yaxis('提交次数', torvalds_commit_week_count)
    .set_global_opts(title_opts=opts.TitleOpts(title='Linus提交星期分布'))
)
bar.render('Linus_week_commit.html')
