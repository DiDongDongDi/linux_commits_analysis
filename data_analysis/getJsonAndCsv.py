import json
import pandas as pd
from datetime import datetime
import codecs
import csv
import pymongo

# 连接数据库
client = pymongo.MongoClient("mongodb://share:shareshare@wangqy.top:27017/linux_commits_analysis")
db = client["linux_commits_analysis"]
users = db["users"]
commits = db["commits"]

# 生成usersfile.csv
usersCursor = users.find()
with codecs.open('csvfolder/usersfile.csv', 'w', 'utf-8') as csvfile:
    writer = csv.writer(csvfile)
    # 先写入columns_name
    writer.writerow(["_id", "user", "avatar", "html"])
    # 写入多行用writerows
    for data in usersCursor:
        writer.writerows([[data["_id"], data["user"], data["avatar"], data["html"]]])

# 生成datefile.csv
commitsCursor = commits.find()
with codecs.open('csvfolder/datefile.csv', 'w', 'utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["author_date", "committer_date"])
    for data in commitsCursor:
        data["author_date"] = data["author_date"].strftime('%Y-%m-%d %H:%M:%S')
        data["committer_date"] = datetime.strftime(data["committer_date"], '%Y-%m-%d %H:%M:%S')
        writer.writerows([[data["author_date"], data["committer_date"]]])

# 生成authorcommitfile.csv
commitsCursor = commits.find()
with codecs.open('csvfolder/authorcommitfile.csv', 'w', 'utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["author_login", "committer_login"])
    for data in commitsCursor:
        if data["author_login"] == None:
            data["author_login"] = str(data["author_login"])
        if data["committer_login"] == None:
            data["committer_login"] = str(data["author_login"])
        writer.writerows([[data["author_login"], data["committer_login"]]])

# 生成temp.csv
author_commit = pd.read_csv("csvfolder/authorcommitfile.csv")
author_commit_df = pd.DataFrame(author_commit)


def getAuthorCount(str):
    return list(author_commit_df["author_login"]).count(str)


def getCommitCount(str):
    return list(author_commit_df["committer_login"]).count(str)


with codecs.open('csvfolder/temp.csv', 'w', 'utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["user", "author_login", "committer_login"])
    for data, row in author_commit_df.iterrows():
        authorCount = getAuthorCount(row["author_login"])
        commitCount = getCommitCount(row["committer_login"])
        writer.writerows([[row["author_login"], authorCount, commitCount]])

# 生成user.json
newUser = pd.read_csv('csvfolder/temp.csv')
users = pd.read_csv('csvfolder/usersfile.csv')
newUserdf = pd.DataFrame(newUser)
usersdf = pd.DataFrame(users)
newUser = pd.merge(newUser, users, on='user')
newUser = newUser.drop_duplicates(subset='user', keep='last')

userjson = newUser.to_json(orient='records')
with open('json/users.json', 'w', encoding="UTF-8") as jf:
    jf.write(json.dumps(userjson, indent=2))
