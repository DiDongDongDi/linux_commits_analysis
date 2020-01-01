# database operations
import pymongo
client = pymongo.MongoClient(host='wangqy.top', port=27017)
db = client.linux_commits_analysis
users = db.users
commits = db.commits
db.authenticate('share', 'shareshare')

# 提取所有的message
all_messages = commits.find({}, {'_id': 0, 'message': 1})
message_tag = ['Merge', 'Net', 'IO', 'Linux', 'ext4', 's390', 'GPIO', 'USB', 'KVM', 'drm', 'mm', 'PM', 'spi', 'i2c', 'CIFS', 'btrfs', 'block', 'Others']
message_tag_count = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
for message in all_messages:
    if message['message'][:5] == 'Merge':
        message_tag_count[0] += 1
    elif message['message'][:3] == 'net' or message['message'][:3] == 'tcp' or message['message'][:3] == 'udp' or message['message'][:3] == 'ipv':
        message_tag_count[1] += 1
    elif message['message'][:2] == 'io':
        message_tag_count[2] += 1
    elif message['message'][:5] == 'Linux':
        message_tag_count[3] += 1
    elif message['message'][:4] == 'ext4':
        message_tag_count[4] += 1
    elif message['message'][:4] == 's390':
        message_tag_count[5] += 1
    elif message['message'][:4] == 'gpio':
        message_tag_count[6] += 1
    elif message['message'][:3] == 'usb' or message['message'][:3] == 'USB':
        message_tag_count[7] += 1
    elif message['message'][:3] == 'KVM':
        message_tag_count[8] += 1
    elif message['message'][:3] == 'drm':
        message_tag_count[9] += 1
    elif message['message'][:2] == 'mm':
        message_tag_count[10] += 1
    elif message['message'][:2] == 'PM':
        message_tag_count[11] += 1
    elif message['message'][:3] == 'spi':
        message_tag_count[12] += 1
    elif message['message'][:3] == 'i2c':
        message_tag_count[13] += 1
    elif message['message'][:4] == 'cifs' or message['message'][:4] == 'CIFS':
        message_tag_count[14] += 1
    elif message['message'][:5] == 'btrfs' or message['message'][:5] == 'Btrfs':
        message_tag_count[15] += 1
    elif message['message'][:5] == 'block':
        message_tag_count[16] += 1
    else:
        message_tag_count[17] += 1

# 使用pyecahrts做饼状图
from pyecharts.faker import Faker
from pyecharts import options as opts
from pyecharts.charts import Pie

message_tag_count_tag = []
for i in range(len(message_tag)):
    message_tag_count_tag.append((message_tag[i], message_tag_count[i]))

pie = (
    Pie()
    .add("", message_tag_count_tag)
    .set_global_opts(title_opts=opts.TitleOpts(title='message类别比重', pos_top='bottom'))
    .set_series_opts(label_opts=opts.LabelOpts(formatter='{b}: {c} | {d}%'))
)

pie.render('message_analysis.html')
