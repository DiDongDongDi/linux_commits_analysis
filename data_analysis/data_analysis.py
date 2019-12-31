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

# 画柱状图
# 设置中文字体和负号正常显示
matplotlib.rcParams['font.sans-serif'] = ['WenQuanYi Micro Hei']
matplotlib.rcParams['axes.unicode_minus'] = False

plt.barh(range(24), torvalds_commit_hour_count)
plt.ylabel('时间点')
plt.xlabel('提交次数')
plt.title('Linus提交时间分布')
ax = plt.gca()# 获取到当前坐标轴信息
ax.xaxis.set_ticks_position('top')# 将X坐标轴移到上面
ax.invert_yaxis()# 反转Y坐标轴
plt.show()
