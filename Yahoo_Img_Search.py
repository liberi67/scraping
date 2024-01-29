import time
import requests
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import os
from selenium.common.exceptions import NoSuchElementException

# msedgedriver.exeのパスを指定
edge_driver_path = './msedgedriver.exe'  # ダウンロードしたドライバーのパスに置き換える

# EdgeのWebDriverを初期化
driver = webdriver.Edge(service=Service(edge_driver_path))

# 対象のURLを開く
url = "https://search.yahoo.co.jp/image/search?p=splatoon3"  # 対象のページのURLに置き換える
driver.get(url)

# 保存先フォルダを作成
out_folder = url.split("=")[-1]
os.makedirs(out_folder, exist_ok=True)

while True:
    
    # スクロールを繰り返す
    for _ in range(5):  # 適当な回数繰り返す（必要に応じて調整）
        driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
        time.sleep(2)   # 適当な待ち時間を設ける（必要に応じて調整）

    # ここからは通常のBeautiful Soupの操作で画像を取得する
    for element in BeautifulSoup(driver.page_source, 'html.parser').find_all("img", alt=lambda value: value and value.strip()):
        image_url = element.get("src")
        filename = os.path.join(out_folder, os.path.basename(image_url))

        if os.path.exists(filename):
            continue

        imgdata = requests.get(image_url)

        with open(filename, mode="wb") as f:
            f.write(imgdata.content)

        time.sleep(1)

    try:
        # もっと見るボタンをクリック
        more_button = driver.find_element(By.CLASS_NAME, 'sw-MoreButton__button')
        more_button.click()
    except NoSuchElementException:
        # WebDriverを閉じる
        driver.quit()
        break