import keyboard
import sys
import tkinter
from PIL import Image, ImageTk
import threading
import time
import simpleaudio

value = 2
double_continue = False


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
    root.geometry("250x250")
    canvas = tkinter.Canvas(bg = "black", width=250, height=250)
    canvas.place(x=0, y=0)
    img = Image.open('image\image1.png')
    img= ImageTk.PhotoImage(img)
    item = canvas.create_image(0, 0, image=img, anchor=tkinter.NW)
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
#発話用ライブラリ
import win32com.client
import winsound

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
#文字列から抽出
import re

driver_path = "C:\\driver\\chromedriver.exe"
def talk(content):
    sapi = win32com.client.Dispatch("SAPI.SpVoice")
    dog = win32com.client.Dispatch("SAPI.SpObjectTokenCategory")
    dog.SetID(r"HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech_OneCore\Voices", False)

    v = [t for t in dog.EnumerateTokens() if t.GetAttribute("Name") == "Microsoft Sayaka"]
    if v:
        oldv = sapi.Voice
        sapi.Voice = v[0]
        sapi.Speak(content)
        sapi.Voice = oldv

def sound_effect(filename):
    wav_obj = simpleaudio.WaveObject.from_wave_file(filename)
    play_obj = wav_obj.play()
    play_obj.wait_done()

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
talk("お探しの物はなんですか？")
while True:
    start = time.process_time()
    sound_effect("sound\system41.wav")
    with sr.Microphone() as input:
        r.adjust_for_ambient_noise(input)
        print("録音中:")
        audio = r.listen(input)
        end = time.process_time()
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
departlist = []
for cat in cats:
  departlist.append(cat.get('id'))
print(departlist)
birds = soup.select("div#brandsRefinements> ul > li")
refinelist = []
for bird in birds:
  refinelist.append(bird.get('id'))
print(refinelist)

talk("価格やブランド、接続方式と、重視するポイントが決まっていれば教えてください。")
price = ""
brand = ""
while True:
    start = time.process_time()
    sound_effect("sound\system41.wav")
    with sr.Microphone() as input:
        r.adjust_for_ambient_noise(input)
        print("録音中:")
        audio = r.listen(input)
        end = time.process_time()
    try:
        text = r.recognize_google(audio, language='ja-JP')
        print(text)
        if "安い" in text:
            price = "&s=price-asc-rank"
            browser.get(linkjp + brand + price)#ページ読み込み
            talk("価格の安い順で並べ替えました。何かありましたらもう一度声をかけてください。")
            continue
        elif "高い" in text:
            price = "&s=price-desc-rank"
            browser.get(linkjp + brand + price)#ページ読み込み
            talk("価格の高い順で並べ替えました。何かありましたらもう一度声をかけてください。")
            continue
        elif "円" in text:
            price_only = ""
            price_line = int(re.sub(r"\D", "", text))
            if "万円" in text:
                price_only = str(price_line) + "0000"
            price_line = str(price_line*0.9) + "-"  + str(price_line*1.1)
            price = "&price=" + price_line
            browser.get(linkjp + brand + price)#ページ読み込み
            talk((price_only)+ "円付近商品のみ表示しました。何かありましたらもう一度声をかけてください。")
            continue
        elif "リセット" in text or "解除" in text:
            brand = ""
            price = ""
            browser.get(linkjp)#ページ読み込み
            talk("すべての検索条件をリセットしました。何かありましたらもう一度声をかけてください")
        elif 'p_89/' + text in refinelist:
            text = text.replace('p_89/',"")
            brand = "&rh=n:3210981,p_89:" + text
            print(linkjp + "&s=price-asc-rank" + brand +price_line)
            browser.get(linkjp + brand + price)#ページ読み込み
            talk(text + "の商品のみ表示しました。何かありましたらもう一度声をかけてください")
        elif "価格" in text:
            talk("価格の安い順、高い順、具体的な価格は決まっていますか？")
            continue
        elif "ブランド" in text:
            talk("どのブランドでしょうか？")
        elif "接続方式" in text:
            talk("ここに接続方式の処理をかく")
    except:
          print("認識できませんでした")