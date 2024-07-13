import requests
import time
from bs4 import BeautifulSoup

url = "https://news.yahoo.co.jp/articles/99c1992bf6e8488ae77ef6fc6bd6c4c9e252cfc6/comments"

response = requests.get(url)
response.raise_for_status()

# HTMLをparse
soup = BeautifulSoup(response.text, "html.parser")

# コメント部分を含むarticle要素をすべて取得
comment_articles = soup.find_all('article', class_='sc-5amsu5-3')

comment_datas = []

for comment_article in comment_articles:
     # コメント記入者の名前を取得
    author = comment_article.find('a', class_='sc-5amsu5-7').text.strip()
    # コメント内容を取得
    comment = comment_article.find('p', class_='sc-5amsu5-11').text.strip()
    comment_datas.append({'author': author, 'comment': comment})

# 結果を表示
for data in comment_datas:
    print(f"Author: {data['author']}\nComment: {data['comment']}\n")