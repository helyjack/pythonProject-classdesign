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
query = "SELECT rating FROM movies"
df = pd.read_sql(query, con=db_connection)

# 关闭数据库连接
db_connection.close()

# 绘制评分直方图
plt.figure(figsize=(10, 6))
sns.histplot(df['rating'], bins=20, kde=True)

plt.title('电影评分分布', fontproperties=my_font)
plt.xlabel('评分', fontproperties=my_font)
plt.ylabel('频率', fontproperties=my_font)

# 设置刻度标签的字体属性
plt.xticks(fontproperties=my_font)
plt.yticks(fontproperties=my_font)

plt.show()
