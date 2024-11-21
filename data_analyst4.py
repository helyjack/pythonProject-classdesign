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
query = "SELECT release_year, COUNT(*) as movie_count FROM movies GROUP BY release_year ORDER BY release_year ASC"
df = pd.read_sql(query, con=db_connection)

# 关闭数据库连接
db_connection.close()

# 设置matplotlib和seaborn的字体为支持中文的字体
plt.rcParams['font.sans-serif'] = ['SimHei']  # 指定默认字体为黑体
plt.rcParams['axes.unicode_minus'] = False    # 解决保存图像时负号'-'显示为方块的问题

# 绘制不同年份的影片数量分布图
plt.figure(figsize=(12, 8))

# 绘制柱状图
sns.barplot(x='release_year', y='movie_count', data=df, palette='viridis')

plt.title('不同年份的影片数量分布', fontproperties=my_font)
plt.xlabel('年份', fontproperties=my_font)
plt.ylabel('影片数量', fontproperties=my_font)

# 设置刻度标签的字体属性
plt.xticks(fontproperties=my_font, fontsize=10, rotation=45)  # 减小字号并旋转标签
plt.yticks(fontproperties=my_font)

plt.show()

# 找出电影数量最多的年代
max_movies_year = df.loc[df['movie_count'].idxmax()]
print(f"电影数量最多的年代是：{max_movies_year['release_year']}年，共有{max_movies_year['movie_count']}部电影。")
