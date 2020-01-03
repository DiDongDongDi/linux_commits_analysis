import pandas as pd
from pandas import DataFrame
import pyecharts.options as opts
from pyecharts.faker import Faker
from pyecharts.charts import Line

author_commit_count = pd.read_csv('csvfolder/temp.csv', encoding='utf-8')
author_commit_df = pd.DataFrame(author_commit_count)
# 去重
author_commit_unique = author_commit_df.drop_duplicates(subset='user', keep='last')

# 按committer_login次数对用户排序
author_commit_sort = DataFrame.sort_values(self=author_commit_unique, by="committer_login", axis=0, ascending=False,
                                           inplace=False, kind='quicksort', na_position='last')
author_commit_describe = author_commit_sort.describe()

# 画每位用户的author_login,committer_login次数的对比图
x=list(author_commit_sort["user"])
y1=author_commit_sort["author_login"]
y2=author_commit_sort["committer_login"]

Line=(
        Line()
            .add_xaxis(x)
            .add_yaxis("author_count", y1)
            .add_yaxis("committer_count",y2 )
            .set_global_opts(title_opts=opts.TitleOpts(title="上传和提交对比折线"))
    )
yaxis_opts=opts.AxisOpts(name="数量")
Line.render("author_committer_counts.html")


x_describe=["总数","平均数","方差","最小值","25%","50%","75%","最大值"]
y1_describe=author_commit_describe["author_login"]
y2_describe=author_commit_describe["committer_login"]
Line2=(
        Line()
            .add_xaxis(x_describe)
            .add_yaxis("author_count", y1_describe)
            .add_yaxis("committer_count",y2_describe )
            .set_global_opts(title_opts=opts.TitleOpts(title="统计信息对比折线图"))
    )
Line2.render("author_committer_describe.html")



