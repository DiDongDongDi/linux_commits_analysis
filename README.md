目 录
=================

   * [<strong>开源软件基础</strong>课程报告](#开源软件基础课程报告)
      * [项目信息](#项目信息)
      * [项目背景及意义](#项目背景及意义)
      * [项目创新点](#项目创新点)
      * [项目的设计](#项目的设计)
      * [如何实现](#如何实现)
         * [数据获取](#数据获取)
            * [API调用](#api调用)
            * [数据处理](#数据处理)
            * [数据库存储](#数据库存储)
         * [数据分析](#数据分析)
            * [数据格式转换](#数据格式转换)
            * [各月提交次数分析](#各月提交次数分析)
            * [各月上传次数分析](#各月上传次数分析)
            * [上传与提交次数对比分析](#上传与提交次数对比分析)
            * [Coding时间分布分析](#coding时间分布分析)
            * [提交评论分析](#提交评论分析)
            * [提交message分析](#提交message分析)
            * [个人上传和提交次数对比分析](#个人上传和提交次数对比分析)
         * [结果展示](#结果展示)
      * [项目分析](#项目分析)
      * [不足及可改进之处](#不足及可改进之处)
      * [总结](#总结)
      * [感想](#感想)

# **开源软件基础**课程报告

## 项目信息

>- 项目名称: Github开源项目**torvalds/linux**历史提交信息分析统计
>- 完成时间: 2020.01.03
>- 指导老师: 任志磊
>- 小组自评(A/B/C): A

小组成员(姓名学号) | 成员分工(角色及任务)
------------------ | --------------------
王庆宇 201792222 | 组长, 负责数据抓取, 以及小时, 星期, comment和message的统计分析, 部分报告撰写
刘恺伊 201792407 | 组员, 负责对各月份的提交数和上传数进行统计分析和比较, 并可视化结果, 部分报告撰写
李泉泱 201792150 | 组员, 负责对各用户上传和提交次数进行统计分析, 以及结果展示网页设计编写, 部分报告撰写

## 项目背景及意义

1. Github

Github拥有超过900万开发者用户. 随着越来越多的应用程序转移到了云上, Github已经成为了管理软件开发以及发现已有代码的首选方法. 如前所述作为一个分布式的版本控制系统, 在Git中并不存在主库这样的概念, 每一份复制出的库都可以独立使用, 任何两个库之间的不一致之处都可以进行合并. GitHub可以托管各种git库, 并提供一个web界面, GitHub的独特卖点在于从另外一个项目进行分支的简易性. 

2. 开源

开放源代码也称为源代码公开, 指的是一种软件发布模式. 一般的软件仅可取得已经过编译的二进制可执行档, 通常只有软件的作者或著作权所有者等拥有程序的原始码. 

3. Git

Git是Linus Torvalds为了帮助管理Linux内核开发而开发的一个开放源码的版本控制软件. 

4. Linux

Linux继承了Unix以网络为核心的设计思想, 是一个性能稳定的多用户网络操作系统. 与其他操作系统相比, 具有开放源码, 没有版权, 技术社区用户多等特点, 开放源码使得用户可以自由裁剪, 灵活性高, 功能强大, 成本低. 尤其系统中内嵌网络协议栈, 经过适当的配置就可实现路由器的功能. 这些特点使得Linux成为开发路由交换设备的理想开发平台. 

5. 意义

通过python的pandas, matplotlib, pyecharts等库, 对数据进行统计分析, 将信息可视化, 绘制成条形图, 柱状图, 饼状图, 折线图等, 从而探究linux有关代码在2019年的用户提交上传次数, 提交上传时间等信息. 通过分析 linux 2019年的历史提交信息, 我们可以发现一些大型软件工程的开发规律和特点, 从中知道软件的演化过程, 从而为以后的软件开发过程规范化总结经验.

## 项目创新点

1. 数据分析方面

用python语言对爬取的`74010`条数据进行多维度的分析解读, 累计生成图表`10`个, 累计使用python及其他语言工具和库`10`余个. 

2. 数据可视化方面

实现了`2520`位用户信息的分页展示, 信息包括用户头像, 每年作为`author`和`committer`的提交次数,点击头像可以跳转到用户主页. 

实现了数据分析结果的集中展示, 包括柱形图, 饼图折线图等多种类型的分析图表. 

3. 编程技术与难点方面 

数据库: 用`mongodb `存储信息, 其他队员可以远程访问数据库.

python: 用`pandas`,`matplotlib`,`pychart` 等工具对大量数据进行分析, 比普通python编程代码量少, 且运行速度快. 

数据可视化: `art-template`模板动态加载数据, `Ajax`局部刷新.

4. 团队开发方面

利用git工具开发项目, 可以很容易的解决开发者之间的冲突, 且团队目标清晰, 分工明确, 工作积极. 

## 项目的设计

项目主要分为三个部分, 分别是: 获取数据, 数据分析和结果展示. 前期, 将**torvalds/linux**开源项目的历史提交信息抓取下来, 提取有用的信息到数据库; 中期, 对数据库中的信息进行统计分析, 探索其中的规律和特点, 并将其可视化; 后期, 将得到的规律和特点, 以网页的形式展现出来, 并优化可视化效果.

## 如何实现

### 数据获取

代码文件为`./get_date/get_date.py`.

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
> 这里并没有考虑网络传输延时和数据处理时间.

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

#### 数据库存储

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
> 抓取数据的时间是`2019年12月27日`, 最近的一条数据的时间是`2019年12月23日`, 所以并不算是2019年全年, 由于时间有限, 数据结果仅供参考.

### 数据分析

#### 数据格式转换

代码文件为`./data_analysis/get_json_csv.py`.

为方便后期的数据分析和可视化, 把需要的数据写入csv文件, 用pandas读取csv文件非常方便, 而且速度很快, 适合大量数据的处理. 或者转成json格式, 便于前端展示. 

```python 
# 例如生成usersfile.csv
with codecs.open('csvfolder/usersfile.csv', 'w', 'utf-8') as csvfile:
    writer = csv.writer(csvfile)
    # 先写入columns_name
    writer.writerow(["_id", "user", "avatar", "html"])
    # 写入多行用writerows
    for data in usersCursor:
        writer.writerows([[data["_id"], data["user"], data["avatar"], data["html"]]])
# 需要注意数据的类型, "author_date"是日期类型, "author_login"=None的情况, 这些都需要转换成字符串类型才能用上面的方法写入. 
# data["author_date"] = data["author_date"].strftime('%Y-%m-%d %H:%M:%S')
#data["committer_login"] = str(data["author_login"])

#生成JSON文件
userjson = newUser.to_json(orient='records')
with open('json/users.json', 'w', encoding="UTF-8") as jf:
    jf.write(json.dumps(userjson, indent=2))
```

#### 各月提交次数分析

代码文件为`./data_analysis/month_committer_date.py`.

首先将爬虫的数据存成`.csv`文件. 下面我们分析的数据均来自生成的`datefile.csv`文件:

```python
# 读取.csv文件, 这里引用了pandas包和csv包
import pandas as pd
import csv
pr= pd.read_csv(r'C:\Users\w\Desktop\datefile.csv',encoding='ISO-8859-1')
```

然后将每月提交量按月份取出:

```python
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
```

通过计算每一组DataFrame的行数, 来计算每月提交量. 最后, 设置要可视化的参数, 进行可视化. 

```python
month_counts = [ Jan.shape[0],Feb.shape[0], Mar.shape[0], Apr.shape[0], May.shape[0],Jun.shape[0],
              Jul.shape[0], Aug.shape[0],Sept.shape[0],Oct.shape[0],Nov.shape[0],Dec.shape[0]]
```

```python
month=["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug",
       "Sept","Oct","Nov","Dec"]
```

最终我们得到了每月提交量柱状图和每月提交量对比的饼状图:

![每月提交量饼状图](http://qiniu.wangqy.top/didong/images/linux_commits_analysis_liukaiyi_1.png)

![每月提交量饼状图](http://qiniu.wangqy.top/didong/images/linux_commits_analysis_liukaiyi_0.png)

可以看出:

1. 2019年6月与10月是Linux提交的高峰期, 看来大佬们喜欢把统一提交时间定在6月与10月;

2. 12月的提交量相对于别的月份来说, 尤其少, 看来管理者在一年的结尾都不是很想工作;

3. 总体说来, 6月提交量最多为8148次, 而12月的最少为1398次.

#### 各月上传次数分析

代码文件为`./data_analysis/month_author_date.py`.

同committer_date一样, 首先将爬虫的数据存成`.csv`文件. 下面我们分析的数据均来自生成的`datefile.csv`文件:

```python
# 读取.csv文件, 这里引用了pandas包和csv包
import pandas as pd
import csv
pr= pd.read_csv(r'C:\Users\w\Desktop\datefile.csv',encoding='ISO-8859-1')
```

然后将每月上传量按月份取出:

```python
Dec = pr[pr['author_date'].str.startswith("2019-12")]
Nov = pr[pr['author_date'].str.startswith("2019-11")]
Oct = pr[pr['author_date'].str.startswith("2019-10")]
Sept = pr[pr['author_date'].str.startswith("2019-09")]
Aug = pr[pr['author_date'].str.startswith("2019-08")]
Jul = pr[pr['author_date'].str.startswith("2019-07")]
Jun = pr[pr['author_date'].str.startswith("2019-06")]
May = pr[pr['author_date'].str.startswith("2019-05")]
Apr = pr[pr['author_date'].str.startswith("2019-04")]
Mar = pr[pr['author_date'].str.startswith("2019-03")]
Feb = pr[pr['author_date'].str.startswith("2019-02")]
Jan = pr[pr['author_date'].str.startswith("2019-01")]
```

通过计算每一组DataFrame的行数, 来计算每月上传量. 最后, 设置要可视化的参数, 进行可视化. 

```python
month_counts = [ Jan.shape[0],Feb.shape[0], Mar.shape[0], Apr.shape[0], May.shape[0],Jun.shape[0],
              Jul.shape[0], Aug.shape[0],Sept.shape[0],Oct.shape[0],Nov.shape[0],Dec.shape[0]]
```

```python
month=["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug",
       "Sept","Oct","Nov","Dec"]
```

最终我们得到了每月上传量柱状图和每月上传量对比的饼状图:

![每月上传量柱状图](http://qiniu.wangqy.top/didong/images/linux_commits_analysis_liukaiyi_3.png)

![每月上传量饼状图](http://qiniu.wangqy.top/didong/images/linux_commits_analysis_liukaiyi_4.png)

可以看出:

1. 2019年6月与8月是Linux上传的高峰期, 此时应该已经进入了工作的白热化阶段;

2. 12月的上传量相对于别的月份来说, 尤其少, 看来程序员在一年的结尾也同样不是很想工作;

3. 总体说来, 6月上传量最多为7435次, 而12月的最少为1183次.

#### 上传与提交次数对比分析

代码文件为`./data_analysis/month_author_committer_compare.py`.

我们还想探究一下上传与提交的关系, 所以在这里我们又生成了一个两者对比折线图. 

将两个数据放在一起进行比较:

```python
plt.plot(x,month_counts,label='committer_date',color='y',linewidth=3.0)
plt.plot(x,month_counts1,label='author_date',color='b',linewidth=2.0)
```

然后将折线图可视化出来, 效果如下:

![上传与提交次数对比折线图](http://qiniu.wangqy.top/didong/images/linux_commits_analysis_liukaiyi_2.png)

可以看出:

1. 提交量普遍高于上传量, 看来编码比审核复杂;

2. 总体说来, 提交与上传的整体走势还是一致的.

#### Coding时间分布分析

代码文件为`./data_analysis/Linus_hour_week_commit_analysis.py`.

之前有一篇Ivan的关于[At what time of day do famous programmers work?](https://ivan.bessarabov.com/blog/famous-programmers-work-time)的博客, 下面是Linus对[https://github.com/torvalds/linux](https://github.com/torvalds/linux)库的提交时间图表:

![Linus对linux库的提交时间分布](http://qiniu.wangqy.top/didong/images/linux_commits_analysis_0.jpg)

在这里我们借此机会, 对其做一个验证.

> 注意:
>- API所提供的时间是UTC时区的时间, 所以如果对所有author或committer进行统计是没有意义的, 因此这里只选择了Linus进行统计, 根据维基百科中对[Linus Torvalds](https://en.wikipedia.org/wiki/Linus_Torvalds)的说明, 其住所应该是在*Dunthorpe, Oregon, U.S.*, 所以根据时区, Linus提交时的真实时间应该是UTC时区时间再减去8小时;
>- git中有author和committer的区别, 其中, author是编写补丁的人, committer是应用补丁的人, 可参考[https://stackoverflow.com/questions/18750808/difference-between-author-and-committer-in-git](https://stackoverflow.com/questions/18750808/difference-between-author-and-committer-in-git). 在这里, 对于Linus来说, 我们采用committer来进行统计.

最后的结果如下图:

![Linus对linux库的提交小时分布(2019年)](http://qiniu.wangqy.top/didong/images/linux_commits_analysis_1.png)

其中, Linus在2019年共提交了3770次.

可以看出:

1. 2019年9点左右是Linus提交的高峰期, 与Ivan的10点比较靠近, 18点又到达另一个提交的高峰期;

2. 作息依旧比较正常, 白天提交次数多, 晚上提交次数少, 6点开始提交次数慢慢变多, 8点(应该是正式开始工作)爆发, 22点开始提交次数就很少了;

3. 2点的提交还是挺多的, 看来大佬也熬夜;

4. 总体说来与Ivan的结果还是比较接近的, 但由于数据量较少的原因, 不是特别接近.

除此之外, 对Linus不同星期的提交情况也进行了统计分析.

![Linus对linux库的提交星期分布(2019年)](http://qiniu.wangqy.top/didong/images/linux_commits_analysis_2.png)

> 注意:
>
> 这里依旧需要减去8小时.

可以看出:

1. 星期一和星期四, Linus的代码提交数最多;

2. 除去星期一和四, 其他星期工作日和休息日的差别不是很大.

#### 提交评论分析

代码文件为`./data_analysis/commits_comment_count_analysis.py`.

每一条提交下面都可以发布评论, 数据库中已经收集了各提交下的评论数, 下面对其进行一个统计.

1. 2019年总的评论数为91, 可以说很少, 因此后面只提取了评论数前5的提交信息;

2. 评论数最多的提交是7月18号torvalds提交的`合并floppy分支`, 评论数是28, 其次是3月3号torvalds提交的`Linux 5.0`, 评论数是16, 剩余的提交的评论数都很少.

```
Total comment count: 91

*****-----*****-----*****-----*****-----*****-----*****-----*****-----*****

author_date: 2019-07-18T15:43:20
author_login: torvalds
committer_date: 2019-07-18T15:43:20
committer_login: torvalds
comment_count: 28
message: Merge branch 'floppy'

Merge floppy ioctl verification fixes from Denis Efremov.

This also marks the floppy driver as orphaned - it turns out that Jiri
no longer has working hardware.

Actual working physical floppy hardware is getting hard to find, and
while Willy was able to test this, I think the driver can be considered
pretty much dead from an actual hardware standpoint.  The hardware that
is still sold seems to be mainly USB-based, which doesn't use this
legacy driver at all.

The old floppy disk controller is still emulated in various VM
environments, so the driver isn't going away, but let's see if anybody
is interested to step up to maintain it.

The lack of hardware also likely means that the ioctl range verification
fixes are probably mostly relevant to anybody using floppies in a
virtual environment.  Which is probably also going away in favor of USB
storage emulation, but who knows.

Will Decon reviewed the patches but I'm not rebasing them just for that,
so I'll add a

  Reviewed-by: Will Deacon <will@kernel.org>

here instead.

* floppy:
  MAINTAINERS: mark floppy.c orphaned
  floppy: fix out-of-bounds read in copy_buffer
  floppy: fix invalid pointer dereference in drive_name
  floppy: fix out-of-bounds read in next_valid_format
  floppy: fix div-by-zero in setup_format_params

*****-----*****-----*****-----*****-----*****-----*****-----*****-----*****

author_date: 2019-03-03T23:21:29
author_login: torvalds
committer_date: 2019-03-03T23:21:29
committer_login: torvalds
comment_count: 16
message: Linux 5.0

*****-----*****-----*****-----*****-----*****-----*****-----*****-----*****

author_date: 2019-07-30T18:15:44
author_login: bebarino
committer_date: 2019-09-04T10:43:49
committer_login: gregkh
comment_count: 4
message: tty: Remove dev_err() usage after platform_get_irq()

We don't need dev_err() messages when platform_get_irq() fails now that
platform_get_irq() prints an error message itself when something goes
wrong. Let's remove these prints with a simple semantic patch.

// <smpl>
@@
expression ret;
struct platform_device *E;
@@

ret =
(
platform_get_irq(E, ...)
|
platform_get_irq_byname(E, ...)
);

if ( \( ret < 0 \| ret <= 0 \) )
{
(
-if (ret != -EPROBE_DEFER)
-{ ...
-dev_err(...);
-... }
|
...
-dev_err(...);
)
...
}
// </smpl>

While we're here, remove braces on if statements that only have one
statement (manually).

Cc: Greg Kroah-Hartman <gregkh@linuxfoundation.org>
Cc: Jiri Slaby <jslaby@suse.com>
Cc: Greg Kroah-Hartman <gregkh@linuxfoundation.org>
Signed-off-by: Stephen Boyd <swboyd@chromium.org>
Link: https://lore.kernel.org/r/20190730181557.90391-45-swboyd@chromium.org
Signed-off-by: Greg Kroah-Hartman <gregkh@linuxfoundation.org>

*****-----*****-----*****-----*****-----*****-----*****-----*****-----*****

author_date: 2019-07-30T13:44:07
author_login: medude
committer_date: 2019-08-03T00:00:01
committer_login: miquelraynal
comment_count: 3
message: mtd: rawnand: micron: handle on-die "ECC-off" devices correctly

Some devices are not supposed to support on-die ECC but experience
shows that internal ECC machinery can actually be enabled through the
"SET FEATURE (EFh)" command, even if a read of the "READ ID Parameter
Tables" returns that it is not.

Currently, the driver checks the "READ ID Parameter" field directly
after having enabled the feature. If the check fails it returns
immediately but leaves the ECC on. When using buggy chips like
MT29F2G08ABAGA and MT29F2G08ABBGA, all future read/program cycles will
go through the on-die ECC, confusing the host controller which is
supposed to be the one handling correction.

To address this in a common way we need to turn off the on-die ECC
directly after reading the "READ ID Parameter" and before checking the
"ECC status".

Cc: stable@vger.kernel.org
Fixes: dbc44edbf833 ("mtd: rawnand: micron: Fix on-die ECC detection logic")
Signed-off-by: Marco Felsch <m.felsch@pengutronix.de>
Reviewed-by: Boris Brezillon <boris.brezillon@collabora.com>
Signed-off-by: Miquel Raynal <miquel.raynal@bootlin.com>

*****-----*****-----*****-----*****-----*****-----*****-----*****-----*****

author_date: 2019-10-27T17:19:19
author_login: torvalds
committer_date: 2019-10-27T17:19:19
committer_login: torvalds
comment_count: 2
message: Linux 5.4-rc5
```

然后找了一下`Linux 5.0`的评论(部分)和代码修改, 如下:

![Linux 5.0 提交部分评论](http://qiniu.wangqy.top/didong/images/linux_commits_analysis_3.png)

看来那个时候Linux5.0发布了, 大家都很兴奋啊!

#### 提交message分析

代码文件为`./data_analysis/message_analysis.py`.

由于每次提交的message都是由提交者自定义的, 并非结构化的数据, 虽然在编写的时候还是遵照了一定的规则, 但这里只能对message作部分标签手工提取, 所以统计的数据可能有遗漏或是有超出, 统计结果仅供参考.

> 注意:
> 
> 手工提取的标签是在查看最近三个月(从2020年1月1日开始)的提交数据后的所设置的.


下面是各类型的提交所占2019年总提交数的百分比:

![各类型提交百分比](http://qiniu.wangqy.top/didong/images/linux_commits_analysis_4.png)

下面是除去`Others`的图表:

![各类型提交百分比(除去Others)](http://qiniu.wangqy.top/didong/ima
>  ges/linux_commits_analysis_5.png)

可以看出:

1. `Other`占了很大一部分, 由于是手工提取标签, 所以这一点难以解决;

2. 除去`Others`的部分, `drm`占比最多, 为32.35%, 其次是`Merge`(合并操作), 占比为22.84%, 再者是`Net`, 占比为18.48%.

#### 个人上传和提交次数对比分析

代码文件为`./data_analysis/person_author_committer_compare.py`.

1. 首先需要从`commits`表里的`74010`条数据中把个人的上传和提交次数统计出来, 用如下方法计算上传次数, 同理可以得到提交次数(commit count):

```python
def getAuthorCount(str):
    return list(author_commit_df["author_login"]).count(str)
```

2. 然后把得到的数据temp.csv和user.csv的数据按用户名合并,注意temp.csv和user.csv文件的字段如下:

| user   | author_login | commit_login |
| ------ | ------------ | ------------ |
| 用户名 | 上传次数     | 提交次数     |

| _id        | user   | avatar   | html     |
| ---------- | ------ | -------- | -------- |
| 唯一的标识 | 用户名 | 头像链接 | 主页链接 |

```python
newUser = pd.merge(newUser, users, on='user') # 合并
newUser = newUser.drop_duplicates(subset='user', keep='last')# 去重
# 生成json文件, 用于前端页面展示, 在结果展示页面中说明
```

3. 将去重后的temp.csv按`author_commit`字段进行排序, 调用`pandas`的`describe()`得到平均值, 方差等数据(排序前调用也可以).

4. 画两个折线图, 一个是每位用户的上传和提交次数的对比图, 横坐标表示用户名(空间有限, 没有全写), 纵坐标表示数量; 另一个是用户统计信息对比折线图, 纵坐标表示数量:

![用户上传和提交对比折线图](http://qiniu.wangqy.top/didong/images/linux_commits_analysis_liquanyang_2.png)

![统计信息对比折线图](http://qiniu.wangqy.top/didong/images/linux_commits_analysis_liquanyang_3.png)

5. 从`上传和提交对比折线图`来看, 每位用户上传和提交数量没有什么关系, 且总体来说每个人提交的次数要大于自己上传的次数; 从`统计信息对比折线图`来看, 用户上传的数量波动较小, 除去一个最大值24699, 其他人的上传量基本在13左右. 

### 结果展示

结果展示页面分为主页和数据分析结果展示页面. 

主页显示每位用户得姓名, 头像, 上传和提交次数, 采用网格布局. 点击头像可以跳转到个人主页, 因为数据太多, 所以采用分页显示, 点击上一页, 下一页, 或想要跳转的页面时, 触发鼠标点击事件, 用Ajax请求从json文件中读取数据, 再用模板展示出来. (js写的分页, 逻辑简单, 不做详述, 详见front-end/js/index.js).

数据分析结果展示页面, 采用两栏布局, 右侧区域用Ajax局部刷新技术, 可以根据需求显示不同的图表, 或者跳转回主页. 

![主页](http://qiniu.wangqy.top/didong/images/linux_commits_analysis_liquanyang_1.png)

![数据分析结果展示页面](http://qiniu.wangqy.top/didong/images/linux_commits_analysis_liquanyang_0.png)

项目展示页面: [http://works.wangqy.top/linux_commits_analysis/](http://works.wangqy.top/linux_commits_analysis/)

## 项目分析

总体来说, 这一次的项目做的还是很不错的. 从数据的抓取, 到数据的各种分析, 以及最后的分析结果的展示, 基本上都圆满地完成了.

特别是数据的各种分析, 基本上对有意义的统计分析都做到了覆盖. 同时, 实现了统计结果的可视化, 也对分析结果进行了说明和可能的解释. 但是, 由于时间的原因, 一方面, 原始数据并不是真正意义上的2019年全年的所有提交, 所以分析得出的结果也仅供参考, 另一方面, 在做message分类统计的时候, 由于message是提交者自定义的, 虽然编写的时候有一定的规则, 但并不是结构化的数据, 所以只能人工打上标签, 并对那些标签进行统计. 但这样的标签肯定是有遗漏或者超出的. 同时由于是人工打上标签, 意味着数目不可能多, 也因此, Others所占的比重特别多, 这一部分的统计是不太准确的. 

数据抓取方面, 由于有API可以调用, 所以从一定程度上减轻了数据抓取方面的负担, 不需要对网页结构进行解析, 直接发送HTTP请求就可以获得相应的json格式数据. 也避免了需要避开反爬虫机制的问题.

分析结果展示方面, 最后所有的分析结果做成一个独立的网页, 从而在文档的基础上, 对成果进一步提取重点并展示.

最后, 在这一次的项目中, 得益于git的使用, 无论是文档, 还是代码的交流, 都变得非常方便快捷. 各种开源工具的支持, 也是项目成功的关键.

## 不足及可改进之处

1. 可以使用更先进的爬虫技术获取开源网站中的相关信息;

2. 除了探究提交上传次数与时间, 我们还可以制作一个热点词汇云, 将注释截取出, 对比统计出现词汇频率等相关信息, 然后选取TOP10做成热点词汇云;

3. 还可以探究大部分提交上传者所在城市的分布情况, 绘制国内程序员分布走势图. 

## 总结

总的来说, 这是一个很成功的项目. 从项目的选取, 数据获取, 分析及结果展示, 各个环节我们都尽力做到最好. 从确定项目开始, 我们就开始分工, 然后编写代码, 撰写报告. 我们把主要的时间花在了数据的分析上, 从多角度, 多方面对抓取的信息进行分析解读, 并且对每个分析结果都用相应的图表把它可视化了出来, 最后把所有分析结果图表汇总到一个网页, 并发布到服务器上. 

团队合作过程很顺利, 这主要得益于git分布式的版本管理, 对比集中式的版本管理系统来说不会出现中心服务器死机就影响工作, 而是可以先存储在本地, 等服务器修改好还可以接着进行工作, 并且git的社区灵活, 拥有丰富的资料来进行学习查阅, 并且git是开源的, 它强调个体, 并且对于公共服务器压力不会太大, 大小项目均可管理, 拥有良好的分支机制, git的分支只要不提交合并, 对其他人没有任何影响. 这些优点都提高了我们开发的效率. 

## 感想

> 从接触linux开始, 我就对开源有了极大的兴趣, 虽然并没有贡献过代码. 以前对一些开源软件有了一定的了解, 但在这次的开源软件基础的课上, 又了解了更多, 巩固了许多. 同时, 对开源其本身的含义, 和开源的精神, 以及开源背后的各种逸闻趣事和背景等都有了全方位的了解. 这或许是上这门课的乐趣之一.
> 
> 其次, 当然还有各种开源软件的学习. 比如说git. 这是第二次将git真正用于团队协作中, 只有这个时候, 我才会体会到git的强大之处(主要是平时也不怎么用). 除此之外, 还有其他很多好用的开源的工具, 在这次的项目开发中也发挥了极大的作用. 
> 
> 另外, 我认为开源软件基础对构建我们自身的整个软件开发框架是很有帮助的. 比如, 这一次的项目开发, 从数据的爬取, 到数据的分析, 再到最后的网页成果展示. 一套流程走下来, 事实上, 对各种技术都会有了一定的了解.
> 
> 最后, 在这次的项目中, 我认为最重要的一点还是团队合作, 通过git, 不同的人负责自己擅长的那块, 大大增加了开发的速度和效率. 大部分的交流都可以线上完成.
> 
> Wrote By 王庆宇

> 首先, 我想谈谈我对此次大作业的感想, 在我第一次接触题目时, 我觉得他是一个巨大的, 不可能完成的工程. Git库, Python, 甚至是数据的分析...... 每一方面知识的运用都是我之前没有接触到的. 大作业的完成也是一拖再拖, 在仅剩一周的时间之后, 我才组好我们的队伍. 接下来是真正着手自己分工负责的内容, 我的任务是把得到的开源信息可视化出来. 在刚刚接收组员给我的数据信息后, 我研究发现, 信息是存在组员的数据库中, 这给我的操作增加了难度, 在实验远程数据库直接连接处理数据失败后, 我跟组员共同商量, 研究, 探讨, 决定将数据以.csv文件的形式存储, 这样我可以轻松把信息下载到本地进行操作. 在读取文件后, 数据的处理也是一大难关, 在我仔细分析我最终想要生成可视化图表所需参数后, 我把commits表中的记录按月份截取出, 并分别计算每月的提交量. 最后, 我通过Python的一些可视化工具成功绘制了committer_date柱状图, 饼图; author_date柱状图, 饼图. 在绘制结束后, 我又对committer和author的提交, 上传时间比较产生了兴趣, 于是计划外地绘制了二者对比折线图, 实现了二者对比, 探究了数据更深层次的联系. 
> 
> 接下来, 我要分享一下我对这门开源技术课程的感想. 在上课之前, 老师让我们填了一张调查问卷, 我记得我当时的答案是对编程不感兴趣, 而实际上, 由于之前编码基础的缺失, 确实使我在编程方面没有自信, 甚至感到排斥与恐惧. 但在这门开源技术课上, 老师很耐心地给我们一点点一遍遍演示他的代码, 讲解他的思路, 我在跟随老师脚步的过程中, 一点点解开编码这层神秘的面纱, 逐渐被每一次成功编码的喜悦所吸引. 在课程的最后, 老师又让我们重新填写了调查问卷, 这次, 我跟着自己的心, 选择了喜欢这个选项.
> 
> 最后, 我觉得很幸运在我对编码彷徨的时候, 通过学习这门课程, 使我重新拾起了对代码的自信与兴趣.
> 
> Wrote By 刘恺伊

> 这次大作业让我对python和开源有了一个新的认识, 我觉得python是一门很有趣的编程语言, 很方便很实用, 而且功能非常强大. 刚开始写的时候, 一看是7万多条数据, 我都懵了, 加载了半天都没有把数据读取出来, 后来发现了一个很好用的库pandas, 一下子豁然开朗...... 队友也很给力, 非常厉害, 所以我觉得整个项目下来感觉自己学到了挺多东西. 
> 
> 我觉得系统的学习一些东西还是很有必要的, 比如这次写作业的时候, 磕磕绊绊, 中间也遇到了很多bug, 但是我马上就能想到这个应该是什么地方出了问题, 比如说用csv.writer写入的时候, 格式转换出错, 以及前端的jQuery引入问题等. 很多知识点只有真正的去实践了才会理解, 我觉得编程的过程可以让一个人静下心来去思考和沉淀, 在自己有了一定的知识积累后, 学习新的知识就会简单的多, 这时候再去写代码, 会有一种不同的感受. 
> 
> 最后, 希望自己能保持对编程的热情, 不断进步. 
>
> Wrote By 李泉泱
