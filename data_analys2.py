# -*- coding: utf-8 -*-
import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.font_manager as fm

# 设置中文字体
font_path = 'C:/Windows/Fonts/simhei.ttf'  # 这里假设你使用的是Windows系统，并且有simhei字体
my_font = fm.FontProperties(fname=font_path)

# 连接到MySQL数据库
db_connection = mysql.connector.connect(
    host="localhost",       # 例如：'localhost'
    user="root",            # 用户名
    password="123456",      # 密码
    database="douban_movies" # 数据库名称
)

# 查询数据
query = "SELECT release_year, rating FROM movies ORDER BY release_year ASC"
df = pd.read_sql(query, con=db_connection)

# 关闭数据库连接
db_connection.close()

# 设置matplotlib和seaborn的字体为支持中文的字体
plt.rcParams['font.sans-serif'] = ['SimHei']  # 指定默认字体为黑体
plt.rcParams['axes.unicode_minus'] = False    # 解决保存图像时负号'-'显示为方块的问题

# 绘制评分分布图
plt.figure(figsize=(12, 8))

# 按年份分组绘制评分分布
sns.histplot(df, x='release_year', hue='rating', multiple='stack', palette='viridis', bins=20)

plt.title('年份与评分分布', fontproperties=my_font)
plt.xlabel('年份', fontproperties=my_font)
plt.ylabel('频率分布', fontproperties=my_font)

# 设置刻度标签的字体属性
plt.xticks(fontproperties=my_font, fontsize=10, rotation=45)  # 减小字号并旋转标签
plt.yticks(fontproperties=my_font)

plt.show()
