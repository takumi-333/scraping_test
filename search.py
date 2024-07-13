''' 
検索結果の件数を取得
'''

import requests
from bs4 import BeautifulSoup
import sys
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import re

url = "https://news.yahoo.co.jp/search"
keywords = []
while True:
    keyword = input()
    if (keyword == ''):
        break
    keywords.append(keyword)

query = "+".join(keywords)

#googlechromeを起動
driver = webdriver.Chrome()
#chromeドライバーが見つかるまでの待ち時間を設定
driver.implicitly_wait(3)

driver.get(f'{url}?p={query}&ei=utf-8')
time.sleep(3)

click_count = 0
# 「もっと見る」ボタンをクリックします（必要に応じてループさせます）
while True:
    try:
        more_button = driver.find_element(By.XPATH, '//button[@data-cl-params="_cl_vmodule:load;_cl_link:auto;"]')
        more_button.click()
        click_count += 1
        print(f"もっと見るボタンがクリックされました({click_count}回目)")
        # ページがロードされるのを待ちます（適宜調整してください）
        time.sleep(2)
    except:
        # 「もっと見る」ボタンが見つからない場合、ループを終了します
        break

# ページが展開された状態でHTMLを取得し、BeautifulSoupで解析します
html_content = driver.page_source
driver.quit()


# response = requests.get(f'{url}?p={query}&ei=utf-8')
# response.raise_for_status()

# HTMLをparse
soup = BeautifulSoup(html_content, "html.parser")

num_articles_container = soup.find('div', class_='sc-1veqoyo-2')
num_articles = 0
if num_articles_container:
    # <span>タグをすべて取得し、最初のもののテキストを取得
    num_articles_element = num_articles_container.find_all('span')
    if num_articles_element:
        number_text = num_articles_element[0].get_text().strip()
        try:
            num_articles = int(number_text)
            print(f"取得した数値: {num_articles}")
        except ValueError:
            print("数値の変換に失敗しました。")

else:
    print("記事数のコンテナが見つかりませんでした")

news_container_element = soup.find('div', class_='newsFeed')

article_elems = news_container_element.find_all(href=re.compile("https://news.yahoo.co.jp/(articles|expert/articles)"))

if num_articles != len(article_elems) :
    print("取得した記事の件数と実際の記事の件数が異なります")
    print(f"予想: {num_articles}件, 実際: {len(article_elems)}件")
else:
    print("正しい記事数を取得しました")

article_datas = []

for article in article_elems:
    response = requests.get(article.attrs['href'])
    soup = BeautifulSoup(article.content, "html.parser")
    container = soup.find('div', id_="contentsWrap")
    title = container.find('h1', class_='sc-uzx6gd-1').text.strip()
