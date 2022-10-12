import keyboard
import sys
import tkinter
from PIL import Image, ImageTk
import threading
import time
value = 2

"""
def key_input():
  global item, canvas, txt, value
  value = txt.get()
"""

def show_image():
#外から触れるようにグローバル変数で定義
    global item, canvas, txt, value

    root = tkinter.Tk()
    root.title('test')
    root.geometry("400x300")
    canvas = tkinter.Canvas(bg = "black", width=400, height=300)
    canvas.place(x=0, y=0)
    img = Image.open('image1.png')
    img= ImageTk.PhotoImage(img)
    item = canvas.create_image(25, 25, image=img, anchor=tkinter.NW)
    root.mainloop()
"""
#入力ボックス作成
    txt = tkinter.Entry(width=20)
    txt.place(x=90, y=70)
    btn = tkinter.Button(root, text='変更', command=key_input)
    btn.place(x=140, y=70)

"""
#音声処理用ライブラリ
import speech_recognition as sr

# Webサイトにアクセスするためのライブラリ
import requests
# Webページの中のデータにアクセスできるようにするためのライブラリ
from bs4 import BeautifulSoup
#Web検索を行えるライブラリ
from selenium import webdriver
import chromedriver_binary
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.chrome.options import Options
import urllib
driver_path = "C:\\driver\\chromedriver.exe"

#スレッドを立ててtkinterの画像表示を開始する
thread1 = threading.Thread(target = show_image)
thread1.start()


r = sr.Recognizer()
 
  
#url = 'https://www.amazon.co.jp/s?k='+text+'&__mk_ja_JP=カタカナ'
#requests.get(url)
options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
browser = webdriver.Chrome(options=options)
browser.get("http://www.amazon.co.jp/")
# 検索フォームが表示されるまで10秒待つ
element = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.NAME, "field-keywords")))

# 検索フォームのテキストをクリア
#browser.find_element_by_name("field-keywords").clear()
while True:
    start = time.process_time()
    with sr.Microphone() as input:
        r.adjust_for_ambient_noise(input)
        print("録音中:")
        audio = r.listen(input)
        end = time.process_time()
        if int(end-start) >= 10:
            continue
    try:
        text = r.recognize_google(audio, language='ja-JP')
        print(text)
        keyword = text
        print(keyword)
        break
    except:
        print("認識できませんでした")
# 検索フォームにキーワードを入力
element.send_keys(keyword)

# 検索実行
element.send_keys(Keys.RETURN)

link = browser.current_url
print(link)
linkjp = urllib.parse.unquote(link, 'UTF-8')
print(linkjp)
html = requests.get(link)
# ライブラリ'BeautifulSoup'を使って中のデータに自由にアクセスできるようにします。
soup = BeautifulSoup(html.content, 'html.parser') 
cats = soup.select("div#departments > ul > li")
idlist = []
for cat in cats:
  idlist.append(cat.get('id'))
print(idlist)
time.sleep(5)  # Let the user actually see something!

while True:
    start = time.process_time()
    with sr.Microphone() as input:
        r.adjust_for_ambient_noise(input)
        print("録音中:")
        audio = r.listen(input)
        end = time.process_time()
        if int(end-start) >= 10:
            continue
    try:
        text = r.recognize_google(audio, language='ja-JP')
        print(text)
        if text == "シャーペン":
          img = Image.open('image1.png')
          img= ImageTk.PhotoImage(img)
          canvas.itemconfig(item,image=img)
        elif text == "鉛筆" or text == "えんぴつ":
          img = Image.open('image2.png')
          img= ImageTk.PhotoImage(img)
          canvas.itemconfig(item,image=img)
    except:
        print("認識できませんでした")