# database operations
import pymongo
client = pymongo.MongoClient(host='wangqy.top', port=27017)
db = client.linux_commits_analysis
users = db.users
commits = db.commits
db.authenticate('share', 'shareshare')

# 统计一下2019年所有的评论数
total_comment_count = commits.aggregate([{
    '$group': {
        '_id': None,
        'total_comment_count': {
            '$sum': '$comment_count'
        }
    }
}])
for count in total_comment_count:
    print('Total comment count: ' + str(count['total_comment_count']))

# 评论数不是很多, 选取一下评论数前五的提交
# 需要使用可写的用户在commits表上创建comment_count字段的索引, 命令如下
# db.commits.createIndex({'comment_count': -1})
# 然后才可以排序
# 也可以采用解除内存限制的办法, 但那样性能会大大下降
max_comment_count_commit = commits.find().sort([('comment_count', pymongo.DESCENDING)]).limit(5)
for commit in max_comment_count_commit:
    print('\n*****-----*****-----*****-----*****-----*****-----*****-----*****-----*****\n')
    print('author_date: ' + commit['author_date'].isoformat())
    print('author_login: ' + commit['author_login'])
    print('committer_date: ' + commit['committer_date'].isoformat())
    print('committer_login: ' + commit['committer_login'])
    print('comment_count: ' + str(commit['comment_count']))
    print('message: ' + commit['message'])
