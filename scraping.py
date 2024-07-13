import requests
from bs4 import BeautifulSoup
from urllib import robotparser
from urllib.parse import urljoin
import sys
import time
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

# robots.txtを確認
def check_robots_txt(base_url):
    robots_txt_url = f'{base_url}/robots.txt'
    targets_url = [f'{base_url}',
                   f'{base_url}/articles'
                   f'{base_url}/articles/*/comments',
                   f'{base_url}/search']
    user_agent = '*'

    # robots.txtの取得
    rp = robotparser.RobotFileParser()
    rp.set_url(robots_txt_url)
    rp.read()
    time.sleep(1)

    not_list = []

    # 各URLがスクレイピング可能かチェック
    for url in targets_url:
        res = rp.can_fetch(user_agent, f'{url}*')
        if res is False:
            print(f"You can not scrape: {url}")
            not_list.append(url)
    
    return len(not_list) == 0

def main():
    url = "https://www.yahoo.co.jp/"

    # robots.txtのチェック
    if not check_robots_txt(url):
        print("指定したターゲットにスクレイピングが禁止されたものがあります")
        sys.exit()
    return

if __name__ == "__main__":
    main()