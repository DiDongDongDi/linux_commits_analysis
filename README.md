# Github开源项目**torvalds/linux**历史提交信息分析统计

## 项目背景及意义



## 项目创新点



## 项目的设计

项目主要分为三个部分, 分别是: 获取数据, 数据分析和结果展示. 前期, 将**torvalds/linux**开源项目的历史提交信息抓取下来, 提取有用的信息到数据库; 中期, 对数据库中的信息进行统计分析, 探索其中的规律和特点, 并将其可视化; 后期, 将得到的规律和特点, 以网页的形式展现出来, 并优化可视化效果.

## 如何实现

### 数据获取

#### API调用

一开始准备直接爬取[commits界面](https://github.com/torvalds/linux/commits/master), 然后跑到github的[robots.txt](https://github.com/robots.txt)下去看, 很明显, 大部分数据都不让爬, 还有可能会被反爬虫, 但是恰好github很贴心地准备了[API接口](https://developer.github.com/), 这里我们使用的是[REST API v3](https://developer.github.com/v3/).

使用[List commits on a repository](https://developer.github.com/v3/repos/commits/#list-commits-on-a-repository)的接口来获取commits数据.

> 注意:
>
> 调用[api.github.com](api.github.com)的接口有次数限制:
>- 在不进行用户验证的情况下, 一小时内最多调用60次接口;
>- 在使用github用户验证后, 一小时内最多可调用5000次接口.
>
> 详情请见[接口调用限制](https://developer.github.com/v3/#rate-limiting), [OAuth Authorizations API](https://developer.github.com/v3/oauth_authorizations/), [其他验证方式](https://developer.github.com/v3/auth/).
>
> 这里我们使用了较为简单的[使用github用户名和密码进行验证](https://developer.github.com/v3/auth/#basic-authentication).

将用户名和密码放到`secret`目录下的`user_passwd.txt`文件中, 格式为`username:password`, 不要有其他字符.

```python
# 设置api_url
with open('../secret/user_passwd.txt', 'r') as f:
    user_passwd = f.read()
	# [:-1] 去掉换行符
    api_url = "https://" + user_passwd[:-1] + "@api.github.com/repos/torvalds/linux/commits"
```

`api_url`的参数, 使用`since`和`until`来限定时间范围. 但API每次返回的commit数目最多30条, 而且是返回靠近现在时间的结果, 所以每调用一次API都需要修改`until`的值.

> 注意:
>
> 在修改`until`的值时, 如果改为上一次返回结果的最后一条的时间, 再次返回结果时, 会将上一次的最后一条再次返回, 解决这个问题有两种方法:
>- 第一种, 直接将再次拿到的上一条抛弃;
>- 第二种, 把时间减一秒, 然后再调API.
>
> 这里我们采用的是第二种, 以免重复数据调用造成浪费.
>
> 同时由于Python的datetime库的ISO时间表示不同于mongodb和github, 所以需要进行一下简单的转换.
>
> 由于每次只能返回30条数据, 所以当返回数据小于30时, 可以认为这是最后一批数据了, 此时停止`GET`. 但测试过程中出现了最后一批数据为0条(这也太巧了), 造成列表索引溢出, 所以需要特别关照一下.

```python
# url参数
params = {"since": "2019-01-01T00:00:00Z" ,"until": "2020-01-01T00:00:00Z"}
```

```python
# 下一次until时间的确定
if len(r_json) == 0:
	break
next_until_time = datetime.isoformat(datetime.fromisoformat(r_json[-1]['commit']['committer']['date'][:-1]) - one_second)
params["until"] =  next_until_time + 'Z'
```

```python
# 最后一批数据
if len(r_json) < 30:
	break
```

然后就可以调用API了, 但由于一小时内最多调用5000次, 所以需要延时以确保不会过快调用, 每次调用后的延时为:

<img src="http://latex.codecogs.com/gif.latex?60 \times 60 \div 5000 = 0.72(s)"/>

> 注意:
>
> 这里并没有考虑网络传输延时和数据处理时间

同时由于网络原因, 有时会出现连接超时中断, 所以需要[捕获异常](https://stackoverflow.com/questions/24210792/checking-for-timeout-error-in-python)并重新发送请求. 最后将获取到的数据转为json格式.

```python
while True:
	try:
		r = re.get(api_url, params=params)
		break
	except re.Timeout:
		print('Retry GET ...')
	except re.RequestException:
		print('Retry GET ...')
	time.sleep(0.72)
	r_json = r.json()
```

#### 数据处理

我们使用list来暂存get到的commits和users, 由于commits不会有重复, 所以每调用一次API后就直接将这一批数据插入数据库, 但users可能会出现重复, 所以对其进行处理, 不重复放入list, 同时由于users并不多, 所以在所有API调用结束后, 再统一插入数据库.

```python
# 添加user到列表
def users_add(user_dict):
    if user_dict in users or user_dict['user'] == None:
        pass
    else:
        users.append(user_dict)
```

```python
# 添加commit到列表(需要对日期进行转换)
commits.append({'author_date': datetime.fromisoformat(author_date[:-1]), 'author_login': author_login, 'committer_date': datetime.fromisoformat(committer_date[:-1]), 'committer_login': committer_login, 'comment_count': comment_count, 'message': message})

# 添加user到列表
users_add({'user': author_login, 'avatar': author_avatar, 'html': author_html})
if author_login != committer_login:
	users_add({'user': committer_login, 'avatar': committer_avatar, 'html': committer_html})
```

在对json数据进行解析时, 发现`author`和`committer`的登录信息并不总是有, 所以需要对其捕获异常, 同时设成`None`.

```python
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
```

> 注意:
>
> 每一条commit中都存在`author`和`committer`的`name`, 但是并没有将这个作为区分的标准, 而是使用`login`, 即github的登录用户名.
>
> 原因是`name`有重复的可能, 但`login`必定是唯一的, 从而避免同名的重复统计, 但是也造成了会对没有`login`的漏统.

#### 数据库

在这里我们采用的是mongodb的数据库, 鉴于其以文档的形式存储, 字符串简直不要太好存.

数据库的地址为: `mongodb://share:shareshare@wangqy.top:27017/linux_commits_analysis`, 用户只有读的权限.

数据库共有两个表:

1. commits表, 用来记录每一条comimt的相关信息

author_date | author_login | committer_date | committer_login | comment_count | message
:---------: | :----------: | :------------: | :-------------: | :-----------: | :-----:
(作者完成的日期) | (作者的用户名) | (提交日期) | (提交者的用户名) | (该提交下的评论数) | (提交的说明信息)

2. users表, 用来记录commits中所有author和committer的信息

user | avatar | html
:--: | :----: | :--:
(用户名) | (用户github头像链接) | (用户github主页链接)

最后commits一共有`74010`条, users一共有`2530`条.

> 注意:
>
> 抓取数据的时间是`2019年12月27日`, 最近的一条数据的时间是`2019年12月23日`, 所以并不算是2019年全年, 数据结果仅供参考.

### 数据分析



### 结果展示



## 测试



## 项目分析



## 不足及可改进之处



## 总结



## 感想

> 
> Wrote By 王庆宇

>
> Wrote By 刘恺伊

> 
> Wrote By 李泉泱
