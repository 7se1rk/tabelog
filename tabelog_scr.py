import pytz
import certifi
import urllib.request
import requests
import json
from bs4 import BeautifulSoup
import sys
import time
from selenium import webdriver
import chromedriver_binary
import re

def main():
    driver = webdriver.Chrome("./chromedriver.exe")
    #browser.implicitly_wait = 10

    # urlopen error [SSL: CERTIFICATE_VERIFY_FAILED]を回避
    import ssl
    ssl._create_default_https_context = ssl._create_unverified_context

    #食べログのurlと検索フォーム
    url_site = "https://tabelog.com/"
    driver.get(url_site)
    #エリア、キーワードを入力させる
    basyo = input("エリアを入力してください: ")
    shop_area = driver.find_element_by_css_selector(".js-search-area-input").send_keys(basyo)
    jyanru = input("キーワードを入力してください: ")
    shop_keyword = driver.find_element_by_css_selector(".js-search-keyword-input").send_keys(jyanru)
    #検索ボタンを押す
    driver.find_element_by_css_selector(".p-global-search__search-btn").click()
    #検索結果ページのニューショップ順ボタンを押す
    driver.find_element_by_css_selector(".navi-rstlst__text--new").click()
    #最初の店だけ取得
    soup = BeautifulSoup(driver.page_source, "html.parser")
    first = soup.find(class_="list-rst")
    #print(first.find(class_="list-rst__rst-name-target").string)
    tag_url = first.find(class_="list-rst__rst-name-target").get("href")
    print(syosai_scrape(tag_url))
    #前回取得した店名が違う場合その店名を取得する、同じ場合は"新店舗なし"と送る

def syosai_scrape(syosai_url):
    html = requests.get(syosai_url)
    soup = BeautifulSoup(html.text, "html.parser")
    data=[]
    tables = soup.find_all("table",{"class":"c-table c-table--form rstinfo-table__table"})
    for table in tables:
        rows = table.find_all("tr")
        for row in rows:
            t_col1 = row.find("th").text.replace('\n',' ').replace('\t',' ').strip()
            t_col2 = row.find("td").text.replace('\n',' ').replace('\t',' ').strip()
            col1 = re.sub(r'\s+',u' ',t_col1) # 連続する空白を一つの空白に置換
            col2 = re.sub(r'\s+',u' ',t_col2) # 連続する空白を一つの空白に置換
            data.append([col1,col2])

    result = [""]*15
    for row in data:
        if u"店名" == row[0]:
            result[0] = row[1]
        if u"ジャンル" == row[0]:
            result[1] = row[1]
        if u"予約・お問い合わせ" == row[0]:
            result[2] = row[1]
        if u"予約可否" == row[0]:
            result[3] = row[1]
        if u"住所" == row[0]:
            result[4] = row[1].replace(' 大きな地図を見る 周辺のお店を探す','') # 不要なキーワードを削除
        if u"交通手段" == row[0]:
            result[5] = row[1]
        if u"営業時間・定休日" == row[0]:
            result[6] = row[1]
        if u"予算（口コミ集計）" == row[0]:
            result[7] = row[1]
        if u"席数" == row[0]:
            result[8] = row[1]
        if u"個室" == row[0]:
            result[9] = row[1]
        if u"禁煙・喫煙" == row[0]:
            result[10] = row[1]
        if u"駐車場" == row[0]:
            result[11] = row[1]
        if u"料理" == row[0]:
            result[12] = row[1]
        if u"オープン日" == row[0]:
            result[13] = row[1]
    result[14] = soup.find("span",{"class" : "linktree__parent-target-text"}).string # 最寄り駅取得

    return result


if __name__ == "__main__":
    main()
