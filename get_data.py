import requests as re
import pymongo
from datetime import datetime, timedelta
import time

# 添加user到列表
def users_add(user_dict):
    if user_dict in users or user_dict['user'] == None:
        pass
    else:
        users.append(user_dict)

# 1 second
one_second = timedelta(seconds=1)

# database
client = pymongo.MongoClient(host='localhost', port=27017)
db = client.linux_commits_analysis
collection_commits = db.commits
collection_users = db.users

# api
# 用户名和密码
with open('user_passwd.txt', 'r') as f:
    user_passwd = f.read()
    api_url = "https://" + user_passwd[:-1] + "@api.github.com/repos/torvalds/linux/commits"
params = {"since": "2019-01-01T00:00:00Z" ,"until": "2020-01-01T00:00:00Z"}

# users数目不多, 先直接放内存
users = []

while True:
#  for x in range(3):
    # get data
    while True:
        try:
            r = re.get(api_url, params=params)
            break
        except re.Timeout:
            print('Retry GET ...')
        except re.RequestException:
            print('Retry GET ...')
    # 延时0.72秒, 防止get太快造成被封, 这里没有管传输和处理时间了
    time.sleep(0.72)
    r_json = r.json()
    commits = []

    for i in range(len(r_json)):
        # commit
        author_date = r_json[i]['commit']['author']['date']
        committer_date = r_json[i]['commit']['committer']['date']
        comment_count = r_json[i]['commit']['comment_count']
        message = r_json[i]['commit']['message']

        # user
        try:
            author_login = r_json[i]['author']['login']
            author_avatar = r_json[i]['author']['avatar_url']
            author_html = r_json[i]['author']['html_url']
        except TypeError:
            author_login = None
            author_avatar = None
            author_html = None

        try:
            committer_login = r_json[i]['committer']['login']
            committer_avatar = r_json[i]['committer']['avatar_url']
            committer_html = r_json[i]['committer']['html_url']
        except TypeError:
            committer_login = None
            committer_avatar = None
            committer_html = None

        # 添加commit到列表(需要对日期进行转换)
        commits.append({'author_date': datetime.fromisoformat(author_date[:-1]), 'author_login': author_login, 'committer_date': datetime.fromisoformat(committer_date[:-1]), 'committer_login': committer_login, 'comment_count': comment_count, 'message': message})

        # 添加user到列表
        users_add({'user': author_login, 'avatar': author_avatar, 'html': author_html})
        if author_login != committer_login:
            users_add({'user': committer_login, 'avatar': committer_avatar, 'html': committer_html})

    # 将每次get到的最后一条commit的时间作为下一次的until时间
    if len(r_json) == 0:
        break
    next_until_time = datetime.isoformat(datetime.fromisoformat(r_json[-1]['commit']['committer']['date'][:-1]) - one_second)
    params["until"] =  next_until_time + 'Z'

    # 显示进度
    print(next_until_time)

    # 先将每次get到的commits数据插入到数据库
    collection_commits.insert(commits)

    # 获取最后离2019-01-01T00:00:00Z最近的数据后, 退出
    if len(r_json) < 30:
        break

# 最后将users数据插入到数据库
collection_users.insert(users)
