# Github开源项目**torvalds/linux**历史提交信息分析统计

## 项目背景及意义

### 背景

#### Github

Github拥有超过900万开发者用户. 随着越来越多的应用程序转移到了云上, Github已经成为了管理软件开发以及发现已有代码的首选方法. 如前所述作为一个分布式的版本控制系统, 在Git中并不存在主库这样的概念, 每一份复制出的库都可以独立使用, 任何两个库之间的不一致之处都可以进行合并. GitHub可以托管各种git库, 并提供一个web界面, GitHub的独特卖点在于从另外一个项目进行分支的简易性. 

#### 开源

开放源代码也称为源代码公开, 指的是一种软件发布模式. 一般的软件仅可取得已经过编译的二进制可执行档, 通常只有软件的作者或著作权所有者等拥有程序的原始码. 

#### Git

Git是Linus Torvalds为了帮助管理Linux内核开发而开发的一个开放源码的版本控制软件. 

#### Linux

Linux继承了Unix以网络为核心的设计思想, 是一个性能稳定的多用户网络操作系统. 与其他操作系统相比, 具有开放源码, 没有版权, 技术社区用户多等特点, 开放源码使得用户可以自由裁剪, 灵活性高, 功能强大, 成本低. 尤其系统中内嵌网络协议栈, 经过适当的配置就可实现路由器的功能. 这些特点使得Linux成为开发路由交换设备的理想开发平台. 

### 意义

通过python的pandas, matplotlib, pyecharts等库, 对数据进行统计分析, 将信息可视化, 绘制成条形图, 柱状图, 饼状图, 折线图等, 从而探究linux有关代码在2019年的用户提交上传次数, 提交上传时间等信息. 通过分析 linux 2019年的历史提交信息, 我们可以发现一些大型软件工程的开发规律和特点, 从中知道软件的演化过程,
从而为以后的软件开发过程规范化总结经验.

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

#### commits数据可视化

首先将爬虫的数据存成`.csv`文件. 下面我们分析的数据均来自生成的`datefile.csv`文件:

```python
# 读取.csv文件, 这里引用了pandas包和csv包
import pandas as pd
import csv
pr= pd.read_csv(r'C:\Users\w\Desktop\datefile.csv',encoding='ISO-8859-1')
```

然后将每月提交量按月份取出.

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

(放上两个图片)

可以看出:

1. 2019年6月与10月是Linux提交的高峰期, 看来大佬们喜欢把统一提交时间定在6月与10月;

2. 12月的提交量相对于别的月份来说, 尤其少, 看来管理者在一年的结尾都不是很想工作;

3. 总体说来, 6月提交量最多为8148次, 而12月的最少为1398次.

#### author_date数据可视化

同committer_date一样, 首先将爬虫的数据存成`.csv`文件. 下面我们分析的数据均来自生成的`datefile.csv`文件:

```python
# 读取.csv文件, 这里引用了pandas包和csv包
import pandas as pd
import csv
pr= pd.read_csv(r'C:\Users\w\Desktop\datefile.csv',encoding='ISO-8859-1')
```

然后将每月上传量按月份取出

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

(放上两个图片)

可以看出

1. 2019年6月与8月是Linux上传的高峰期, 此时应该已经进入了工作的白热化阶段;

2. 12月的上传量相对于别的月份来说, 尤其少, 看来程序员在一年的结尾也同样不是很想工作;

3. 总体说来, 6月上传量最多为7435次, 而12月的最少为1183次.

#### 上传与提交次数可视化对比

我们还想探究一下上传与提交的关系, 所以在这里我们又生成了一个两者对比折线图. 

将两个数据放在一起进行比较：
```python
plt.plot(x,month_counts,label='committer_date',color='y',linewidth=3.0)
plt.plot(x,month_counts1,label='author_date',color='b',linewidth=2.0)
```

然后将折线图可视化出来, 效果如下:

(折线图)

可以看出：

1. 提交量普遍高于上传量, 看来编码比审核复杂;

3. 总体说来, 提交与上传的整体走势还是一致的.

#### Coding时间分布

之前有一篇Ivan的关于[At what time of day do famous programmers work?](https://ivan.bessarabov.com/blog/famous-programmers-work-time)的博客, 下面是Linus对[https://github.com/torvalds/linux](https://github.com/torvalds/linux)库的提交时间图表:

![Linus对linux库的提交时间分布](http://qiniu.wangqy.top/didong/images/linux_commits_analysis_0.jpg)

在这里我们借此机会, 对其做一个验证.

> 注意:
>- API所提供的时间是UTC时区的时间, 所以如果对所有author或committer进行统计是没有意义的, 因此这里只选择了Linus进行统计, 根据维基百科中对[Linus Torvalds](https://en.wikipedia.org/wiki/Linus_Torvalds)的说明, 其住所应该是在*Dunthorpe, Oregon, U.S.*, 所以根据时区, Linus提交时的真实时间应该是UTC时区时间再减去8小时;
>- git中有author和committer的区别, 其中, author是编写补丁的人, committer是应用补丁的人, 可参考[https://stackoverflow.com/questions/18750808/difference-between-author-and-committer-in-git](https://stackoverflow.com/questions/18750808/difference-between-author-and-committer-in-git). 在这里, 对于Linus来说, 我们采用committer来进行统计.

最后的结果如下图:

![Linus对linux库的提交时间分布(2019年)](http://qiniu.wangqy.top/didong/images/linux_commits_analysis_1.png)

其中, Linus在2019年共提交了3770次.

可以看出:

1. 2019年9点左右是Linus提交的高峰期, 与Ivan的10点比较靠近, 18点又到达另一个提交的高峰期;

2. 作息依旧比较正常, 白天提交次数多, 晚上提交次数少, 6点开始提交次数慢慢变多, 8点(应该是正式开始工作)爆发, 22点开始提交次数就很少了;

3. 2点的提交还是挺多的, 看来大佬也熬夜;

4. 总体说来与Ivan的结果还是比较接近的, 但由于数据量较少的原因, 不是特别接近.

### 结果展示



## 测试



## 项目分析



## 不足及可改进之处
1.  可以使用更先进的爬虫技术获取开源网站中的相关信息。
2.  除了探究提交上传次数与时间，我们还可以制作一个热点词汇云，将注释截取出，对比统计出现词汇频率等相关信息，然后选取TOP10做成热点词汇云。
3.  还可以探究大部分提交上传者所在城市的分布情况，绘制国内程序员分布走势图。

## 总结



## 感想

> 
> Wrote By 王庆宇

>
> Wrote By 刘恺伊
>  
> 首先，我想谈谈我对此次大作业的感想，在我第一次接触题目时，我觉得他是一个巨大的，不可能完成的工程。Git库，Python，甚至是数据
的分析……每一方面知识的运用都是我之前没有接触到的。大作业的完成也是一拖再拖，在仅剩一周的时间之后，我才组好我们的队伍。接下来
是真正着手自己分工负责的内容，我的任务是把得到的开源信息可视化出来。在刚刚接收组员给我的数据信息后，我研究发现，信息是存在组员的
数据库中，这给我的操作增加了难度，在实验远程数据库直接连接处理数据失败后，我跟组员共同商量、研究、探讨，决定将数据以.csv文件的形
式存储，这样我可以轻松把信息下载到本地进行操作。在读取文件后，数据的处理也是一大难关，在我仔细分析我最终想要生成可视化图表所需参
数后，我把commits表中的记录按月份截取出，并分别计算每月的提交量。最后，我通过Python的一些可视化工具成功绘制了committer_date柱状图
、饼图；Author_date柱状图、饼图。在绘制结束后，我又对committer和author的提交、上传时间比较产生了兴趣，于是计划外地绘制了二者对比
折线图，实现了二者对比,探究了数据更深层次的联系。
    接下来，我要分享一下我对这门开源技术课程的感想。在上课之前，老师让我们填了一张调查问卷，我记得我当时的答案是对编程不感兴趣，而
实际上，由于之前编码基础的缺失，确实使我在编程方面没有自信，甚至感到排斥与恐惧。但在这门开源技术课上，老师很耐心地给我们一点点一遍
遍演示他的代码，讲解他的思路，我在跟随老师脚步的过程中，一点点解开编码这层神秘的面纱，逐渐被每一次成功编码的喜悦所吸引。在课程的最
后，老师又让我们重新填写了调查问卷，这次，我跟着自己的心，选择了喜欢这个选项。
    最后，我觉得很幸运在我对编码彷徨的时候，通过学习这门课程，使我重新拾起了对代码的自信与兴趣。
>  
> Wrote By 李泉泱
