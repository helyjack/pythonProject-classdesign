import requests
import re
import mysql.connector

def start():
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="123456",
        database="douban_movies"
    )
    cursor = db.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS movies (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        movie_name VARCHAR(255),
                        director_and_actors TEXT,
                        rating VARCHAR(10),
                        `rank` INT,
                        release_year VARCHAR(10),
                        country VARCHAR(255),
                        plot TEXT
                    )''')

    cursor.execute('ALTER TABLE movies AUTO_INCREMENT = 1')

    for i in range(0, 250, 25):
        url = 'https://movie.douban.com/top250?start=' + str(i) + '&filter='
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 SE 2.X MetaSr 1.0"
        }
        response = requests.get(url, headers=headers, verify=False)
        text = response.text
        regex = r'<div class="item">.*?<em class="">(.*?)</em>.*?<span class="title">(.*?)</span>.*?<span class="other">(.*?)</span>.*?<p class="">(.*?)<br>(.*?)</p>.*?<span class="rating_num".*?average">(.*?)</span>.*?<span class="inq">(.*?)</span>'
        results = re.findall(regex, text, re.S)

        for item in results:
            rank = item[0].strip()
            title = item[1].strip()
            other_title = re.sub('&nbsp;', '', item[2].strip())
            movie_name = title + ' ' + other_title
            director_and_actors = re.sub('<br\s*/?>', ' ', re.sub('&nbsp;', '', item[3].strip()))
            release_year_and_country = item[4].strip().replace(u'\xa0', '')
            rating = item[5].strip()
            plot = item[6].strip() if item[6] else '暂无'

            release_year_search = re.search(r'(\d{4})', release_year_and_country)
            release_year = release_year_search.group(1) if release_year_search else '未知'
            country_search = re.findall(r'[\w\s]+', release_year_and_country.split('/')[1].strip())
            remove = ' '.join([c.strip() for c in country_search if c.strip() != '&nbsp;'])
            country = remove.replace(u'\xa0', '') if country_search else '未知'

            dic = {
                '电影名称': movie_name,
                '导演和演员': director_and_actors,
                '评分': rating + '分',
                '排名': rank,
                '上映年份': release_year,
                '国家': country,
                '剧情': plot
            }

            print(dic)
            insert_data(cursor, dic)

    db.commit()
    cursor.close()
    db.close()

def insert_data(cursor, dic):
    sql = "INSERT INTO movies (movie_name, director, rating, `rank`, release_year, country, plot) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    values = (dic['电影名称'], dic['导演和演员'], dic['评分'], dic['排名'], dic['上映年份'], dic['国家'], dic['剧情'])
    cursor.execute(sql, values)

if __name__ == '__main__':
    start()
