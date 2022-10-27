from tkinter.constants import E
import keyboard
import sys
import tkinter
from PIL import Image, ImageTk
import threading
import time
import winsound
import simpleaudio
import wave
import pyaudio
#音声処理用ライブラリ
import speech_recognition as sr
#発話用ライブラリ
import win32com.client
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
import random

#辞書登録
kiso = {"用途":"","接続":"","ノイズキャンセリング":"","音質":"","操作方法":"","マイク":""}
conference = {"用途":"会議","マイク":"あり"}
gaming = {"用途":"ゲーム","接続":"有線","マイク":"あり"}
music = {"用途":"音楽","ノイズキャンセリング":"あり","音質":"いい","マイク":"なし"}
movie = {"用途":"動画","ノイズキャンセリング":"あり","音質":"いい","マイク":"なし"}

#### 関数 ####
#画像表示
def show_image():
#外から触れるようにグローバル変数で定義
    global root,item, canvas, txt, value

    root = tkinter.Tk()
    root.title('test')
    root.geometry("250x300")
    canvas = tkinter.Canvas(bg = "black", width=250, height=250)
    canvas.place(x=0, y=30)
    img = Image.open('image1.png')
    img= ImageTk.PhotoImage(img)
    item = canvas.create_image(0, 0, image=img, anchor=tkinter.NW)
    root.mainloop()

#音声録音
def voice_recoad():
    rec_time = 5            # 録音時間[s]
    file_path = "output.wav" #音声を保存するファイル名
    fmt = pyaudio.paInt16  # 音声のフォーマット
    ch = 1              # チャンネル1(モノラル)
    sampling_rate = 44100 # サンプリング周波数
    chunk = 2**11       # チャンク（データ点数）
    audio = pyaudio.PyAudio()
    index = 1 # 録音デバイスのインデックス番号（デフォルト1）

    stream = audio.open(format=fmt, channels=ch, rate=sampling_rate, input=True,
                        input_device_index = index,
                        frames_per_buffer=chunk)
    print("recording start...")
    # 録音処理
    frames = []
    winsound.PlaySound("system35.wav", winsound.SND_FILENAME)
    for i in range(0, int(sampling_rate / chunk * rec_time)):
        data = stream.read(chunk)
        frames.append(data)

    print("recording  end...")

    # 録音終了処理
    stream.stop_stream()
    stream.close()
    audio.terminate()

    # 録音データをファイルに保存
    wav = wave.open(file_path, 'wb')
    wav.setnchannels(ch)
    wav.setsampwidth(audio.get_sample_size(fmt))
    wav.setframerate(sampling_rate)
    wav.writeframes(b''.join(frames))
    wav.close()

def voiceTOtext():
    voice_recoad()
    with sr.AudioFile("output.wav") as source:
        audio = r.record(source)
    text = r.recognize_google(audio, language='ja-JP')
    print(text)
    return(text)

#VUIが喋る
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
#音声の再生
def sound_effect(filename):
    wav_obj = simpleaudio.WaveObject.from_wave_file(filename)
    play_obj = wav_obj.play()
    play_obj.wait_done()

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

#セリフ
Notext = "認識できませんでした"

# 検索フォームのテキストをクリア
#browser.find_element_by_name("field-keywords").clear()
#イヤホンの検索
talk("お探しの物はなんですか？")
keyword = ""
while True:
    try:
        keyword = voiceTOtext()
        break
    except:
        print(Notext)
"""while True:
    start = time.process_time()
    sound_effect("sound\system41.wav")
    with sr.Microphone() as input:
        r.adjust_for_ambient_noise(input)
        print("録音中:")
        audio = r.listen(input)
        end = time.process_time()
    try:
        text = r.recognize_google(audio, language='ja-JP')
        #text = input(イヤホン)
        print(text)
        keyword = text
        print(keyword)
        break
    except:
        print("認識できませんでした")
"""
# 検索フォームにキーワードを入力
element.send_keys(keyword)
#イヤホンを検索

# 検索実行
element.send_keys(Keys.RETURN)

link = browser.current_url
print(link)
linkjp = urllib.parse.unquote(link, 'UTF-8')
print(linkjp)
html = requests.get(link)
#このURLが表示される
#https://www.amazon.co.jp/s?k=%E3%82%A4%E3%83%A4%E3%83%9B%E3%83%B3&__mk_ja_JP=%E3%82%AB%E3%82%BF%E3%82%AB%E3%83%8A&crid=N3WMK3PTNQVA&sprefix=%E3%82%A4%E3%83%A4%E3%83%9B%E3%83%B3%2Caps%2C192&ref=nb_sb_noss_1

#ここで用途を聞きたい
talk("主な用途はなんですか")
text = ""
while True:
    try:
        text = voiceTOtext()
        break
    except:
        print(Notext)

#用途に合わせて検索してその画面を表示
if "会議" in text or  "オンライン" in text or "meeting" in text or "会議" in text or "ミーティング" in text or "zoom" in text or "LINE" in text or "PS4" in text or "ライン" in text:
    print(list(conference.items()))
    browser.get("https://www.amazon.co.jp/%E3%83%9E%E3%82%A4%E3%82%AF%E4%BB%98%E3%81%8D%E3%82%A4%E3%83%A4%E3%83%9B%E3%83%B3/s?k=%E3%83%9E%E3%82%A4%E3%82%AF%E4%BB%98%E3%81%8D%E3%82%A4%E3%83%A4%E3%83%9B%E3%83%B3")
    talk("他に必要な機能を教えてください")
    while True:
        try:
            text = voiceTOtext()
            break
        except:
            print(Notext)
    if "ワイヤレス" in text  or "無線" in text or "Bluetooth" in text or "ブルートゥース" in text or "wireless" in text or "bluetooth" in text:
        browser.get("https://www.amazon.co.jp/%E3%83%9E%E3%82%A4%E3%82%AF%E4%BB%98%E3%81%8D%E3%82%A4%E3%83%A4%E3%83%9B%E3%83%B3/s?k=%E3%83%9E%E3%82%A4%E3%82%AF%E4%BB%98%E3%81%8D%E3%82%A4%E3%83%A4%E3%83%9B%E3%83%B3&rh=n%3A3477981%2Cp_n_feature_nine_browse-bin%3A2113278051&dc&ds=v1%3AAHRXWRjv5ikTiYMR9JCG%2BiDvGyW0X5R4l%2FPH1xj0t0s&qid=1666757958&rnid=2113277051&ref=sr_nr_p_n_feature_nine_browse-bin_1")
        talk("ではお買い物をお楽しみください")
    elif "ノイズキャンセリング" in text or "キャンセル" in text or "ノイキャン" in text or "ANC" in text or "ノイズ" in text:
        browser.get("https://www.amazon.co.jp/s?k=%E3%83%9E%E3%82%A4%E3%82%AF%E4%BB%98%E3%81%8D%E3%82%A4%E3%83%A4%E3%83%9B%E3%83%B3&i=electronics&rh=n%3A3477981%2Cp_n_feature_nine_browse-bin%3A2113280051&dc&qid=1666758716&rnid=2113277051&ref=sr_nr_p_n_feature_nine_browse-bin_2&ds=v1%3AxZbBcQOB8mKEx6U96IwYbHtk6yoq7HotRTnjsoTUzsY")
        talk("ではお買い物をお楽しみください")
    elif "音質" in text:
        browser.get("https://www.amazon.co.jp/s?k=%E3%83%9E%E3%82%A4%E3%82%AF%E4%BB%98%E3%81%8D%E3%82%A4%E3%83%A4%E3%83%9B%E3%83%B3&rh=n%3A3477981%2Cp_n_feature_nine_browse-bin%3A3937867051&dc&ds=v1%3APU8LUuWZCEAWbrRjc7SBK%2BxZjwtcYf4ZgM0hNaBnum0&__mk_ja_JP=%E3%82%AB%E3%82%BF%E3%82%AB%E3%83%8A&crid=38SXSCL6BIFKB&qid=1666758902&rnid=2113277051&sprefix=%E3%83%9E%E3%82%A4%E3%82%AF%E4%BB%98%E3%81%8D%E3%82%A4%E3%83%A4%E3%83%9B%E3%83%B3%2Caps%2C193&ref=sr_nr_p_n_feature_nine_browse-bin_9")
        talk("ではお買い物をお楽しみください")
    elif "値段" in text or "価格"in text:
        talk("予算はいくらですか")
        while True:
            try:
                text = voiceTOtext()
                break
            except:
                print(Notext)
        price = text
        plice_line = ""
        talk(price+"以下の商品を表示します")
        if "万円" in text or "万" in text:
            price_line = str(re.sub(r"\D", "", text)+"000000")
        elif "円" in text:
            price_line = str(re.sub(r"\D", "", text)+"0000")
        price_int = "&rh=p_36%3A-" + price_line
        browser.get("https://www.amazon.co.jp/%E3%83%9E%E3%82%A4%E3%82%AF%E4%BB%98%E3%81%8D%E3%82%A4%E3%83%A4%E3%83%9B%E3%83%B3/s?k=%E3%83%9E%E3%82%A4%E3%82%AF%E4%BB%98%E3%81%8D%E3%82%A4%E3%83%A4%E3%83%9B%E3%83%B3"+ price_int)#ページ読み込み
        talk(price+ "付近商品のみ表示しました。何かありましたらもう一度声をかけてください。")
    else:
        print(Notext)
elif "ゲーム" in text or "ゲーミング" in text or "switch" in text or "音ゲ" in text or "PS4" in text:
    print(list(gaming.items()))
    browser.get("https://www.amazon.co.jp/s?k=%E3%82%B2%E3%83%BC%E3%83%9F%E3%83%B3%E3%82%B0%E3%82%A4%E3%83%A4%E3%83%9B%E3%83%B3&__mk_ja_JP=%E3%82%AB%E3%82%BF%E3%82%AB%E3%83%8A&crid=60BPQIG4HV4D&sprefix=%E3%82%B2%E3%83%BC%E3%83%9F%E3%83%B3%E3%82%B0%E3%82%A4%E3%83%A4%E3%83%9B%E3%83%B3%2Caps%2C209&ref=nb_sb_noss_1")
    talk("他に必要な機能を教えてください")
    while True:
        try:
            text = voiceTOtext()
            break
        except:
            print(Notext)
    if "ワイヤレス" in text  or "無線" in text or "Bluetooth" in text or "ブルートゥース" in text or "wireless" in text or "bluetooth" in text:
        browser.get("https://www.amazon.co.jp/s?k=%E3%82%B2%E3%83%BC%E3%83%9F%E3%83%B3%E3%82%B0%E3%82%A4%E3%83%A4%E3%83%9B%E3%83%B3&rh=n%3A4817937051%2Cp_n_feature_twenty_browse-bin%3A10421953051&dc&ds=v1%3ADkZNociqZ%2BAVqk7Uf6eclHMm9NyyvC9K36GXWBQ38fQ&__mk_ja_JP=%E3%82%AB%E3%82%BF%E3%82%AB%E3%83%8A&crid=60BPQIG4HV4D&qid=1666759991&rnid=10421952051&sprefix=%E3%82%B2%E3%83%BC%E3%83%9F%E3%83%B3%E3%82%B0%E3%82%A4%E3%83%A4%E3%83%9B%E3%83%B3%2Caps%2C209&ref=sr_nr_p_n_feature_twenty_browse-bin_1")
        talk("では買い物をお楽しみください")
    elif "ノイズキャンセリング" in text or "キャンセル" in text or "ノイキャン" in text or "ANC" in text or "ノイズ" in text:
        browser.get("https://www.amazon.co.jp/s?k=%E3%82%B2%E3%83%BC%E3%83%9F%E3%83%B3%E3%82%B0%E3%82%A4%E3%83%A4%E3%83%9B%E3%83%B3&rh=n%3A4817937051%2Cp_n_feature_twenty-two_browse-bin%3A10471757051&dc&ds=v1%3Afp7tkKd1Tqmh9duEFGop8wQ1bEdR2AL%2B2moDvgb39cQ&__mk_ja_JP=%E3%82%AB%E3%82%BF%E3%82%AB%E3%83%8A&crid=60BPQIG4HV4D&qid=1666759991&rnid=10471755051&sprefix=%E3%82%B2%E3%83%BC%E3%83%9F%E3%83%B3%E3%82%B0%E3%82%A4%E3%83%A4%E3%83%9B%E3%83%B3%2Caps%2C209&ref=sr_nr_p_n_feature_twenty-two_browse-bin_2")
        talk("ではお買い物をお楽しみください")
    elif "値段" in text or "価格"in text:
        talk("予算はいくらですか")
        while True:
            try:
                text = voiceTOtext()
                break
            except:
                print(Notext)
        price = text
        talk(price+"以下の商品を表示します")
        if "万円" in text or "万" in text:
            price_line = str(re.sub(r"\D", "", text)+"000000")
        elif "円" in text:
            price_line = str(re.sub(r"\D", "", text)+"0000")
        price_int = "&rh=p_36%3A-" + price_line
        browser.get("https://www.amazon.co.jp/s?k=%E3%82%B2%E3%83%BC%E3%83%9F%E3%83%B3%E3%82%B0%E3%82%A4%E3%83%A4%E3%83%9B%E3%83%B3&__mk_ja_JP=%E3%82%AB%E3%82%BF%E3%82%AB%E3%83%8A&crid=60BPQIG4HV4D&sprefix=%E3%82%B2%E3%83%BC%E3%83%9F%E3%83%B3%E3%82%B0%E3%82%A4%E3%83%A4%E3%83%9B%E3%83%B3%2Caps%2C209&ref=nb_sb_noss_1"+ price_int)#ページ読み込み
        talk((price)+ "付近商品のみ表示しました。何かありましたらもう一度声をかけてください。")
elif "音楽" in text or "music" in text or "ミュージック" in text or "スポティファイ" in text or "Spotify" in text or "music" in text or "歌" in text:
    print(list(music.items()))
    browser.get("https://www.amazon.co.jp/s?k=%E3%82%A4%E3%83%A4%E3%83%9B%E3%83%B3+%E9%AB%98%E9%9F%B3%E8%B3%AA&__mk_ja_JP=%E3%82%AB%E3%82%BF%E3%82%AB%E3%83%8A&crid=3ES5TZRUU46M2&sprefix=%E3%82%A4%E3%83%A4%E3%83%9B%E3%83%B3+%E9%AB%98%E9%9F%B3%E8%B3%AA%2Caps%2C196&ref=nb_sb_noss_1")
    talk("他に必要な機能を教えてください")
    if "ワイヤレス" in text  or "無線" in text or "bluetooth" in text or "ブルートゥース" in text or "wireless" in text or "Bluetooth" in text:
        browser.get("https://www.amazon.co.jp/s?k=%E3%82%A4%E3%83%A4%E3%83%9B%E3%83%B3+%E9%AB%98%E9%9F%B3%E8%B3%AA&rh=n%3A3477981%2Cp_n_feature_nine_browse-bin%3A2113278051&dc&ds=v1%3AEz%2Fox9QDtpEJttVvBoI%2FrzEieGgY2IvW%2FT9d2MrRApk&__mk_ja_JP=%E3%82%AB%E3%82%BF%E3%82%AB%E3%83%8A&crid=3ES5TZRUU46M2&qid=1666766808&rnid=2113277051&sprefix=%E3%82%A4%E3%83%A4%E3%83%9B%E3%83%B3+%E9%AB%98%E9%9F%B3%E8%B3%AA%2Caps%2C196&ref=sr_nr_p_n_feature_nine_browse-bin_1")
        talk("では買い物をお楽しみください")
    elif "ノイズキャンセリング" in text or "キャンセル" in text or "ノイキャン" in text or "ANC" in text or "ノイズ" in text:
        browser.get("https://www.amazon.co.jp/s?k=%E3%82%A4%E3%83%A4%E3%83%9B%E3%83%B3+%E9%AB%98%E9%9F%B3%E8%B3%AA&rh=n%3A3477981%2Cp_n_feature_nine_browse-bin%3A2113280051&dc&ds=v1%3A2mf5qniqsQ0yN%2FvFn30OnL%2BIJKMVgqH2iI27QuKzzJk&__mk_ja_JP=%E3%82%AB%E3%82%BF%E3%82%AB%E3%83%8A&crid=3ES5TZRUU46M2&qid=1666766808&rnid=2113277051&sprefix=%E3%82%A4%E3%83%A4%E3%83%9B%E3%83%B3+%E9%AB%98%E9%9F%B3%E8%B3%AA%2Caps%2C196&ref=sr_nr_p_n_feature_nine_browse-bin_2")
        talk("ではお買い物をお楽しみください")
    elif "値段" in text or "価格"in text:
        talk("予算はいくらですか")
        while True:
            try:
                text = voiceTOtext()
                break
            except:
                print(Notext)
        price = text
        talk(price+"以下の商品を表示します")
        if "万円" in text or "万" in text:
            price_line = str(re.sub(r"\D", "", text)+"000000")
        elif "円" in text:
            price_line = str(re.sub(r"\D", "", text)+"0000")
        price_int = "&rh=p_36%3A-" + price_line
        browser.get("https://www.amazon.co.jp/s?k=%E3%82%A4%E3%83%A4%E3%83%9B%E3%83%B3+%E9%AB%98%E9%9F%B3%E8%B3%AA&__mk_ja_JP=%E3%82%AB%E3%82%BF%E3%82%AB%E3%83%8A&crid=3ES5TZRUU46M2&sprefix=%E3%82%A4%E3%83%A4%E3%83%9B%E3%83%B3+%E9%AB%98%E9%9F%B3%E8%B3%AA%2Caps%2C196&ref=nb_sb_noss_1"+ price_int)#ページ読み込み
        talk((price)+ "付近商品のみ表示しました。何かありましたらもう一度声をかけてください。")
elif "YouTube" in text or "Twitter" in text or "Prime" in text or "プライム" in text  or "アマプラ" in text or "TikTok" in text or "ティックトック" in text or "ネットフリックス" in text or "Netflix" in text or "ネトフリ" in text:
    print(list(movie.items()))
    browser.get("https://www.amazon.co.jp/s?k=%E3%82%A4%E3%83%A4%E3%83%9B%E3%83%B3+%E9%AB%98%E9%9F%B3%E8%B3%AA&__mk_ja_JP=%E3%82%AB%E3%82%BF%E3%82%AB%E3%83%8A&crid=3ES5TZRUU46M2&sprefix=%E3%82%A4%E3%83%A4%E3%83%9B%E3%83%B3+%E9%AB%98%E9%9F%B3%E8%B3%AA%2Caps%2C196&ref=nb_sb_noss_1")
    talk("他に必要な機能を教えてください")
    if "ワイヤレス" in text  or "無線" in text or "bluetooth" in text or "ブルートゥース" in text or "wireless" in text or "Bluetooth" in text:
        browser.get("")
        talk("では買い物をお楽しみください")
    elif "ノイズキャンセリング" in text or "キャンセル" in text or "ノイキャン" in text or "ANC" in text or "ノイズ" in text:
        browser.get("")
        talk("ではお買い物をお楽しみください")
    elif "値段" in text or "価格"in text:
        talk("予算はいくらですか")
        while True:
            try:
                text = voiceTOtext()
                break
            except:
                print(Notext)
        price = text
        talk(price+"以下の商品を表示します")
        if "万円" in text or "万" in text:
            price_line = str(re.sub(r"\D", "", text)+"000000")
        elif "円" in text:
            price_line = str(re.sub(r"\D", "", text)+"0000")
        price_int = "&rh=p_36%3A-" + price_line
        browser.get("https://www.amazon.co.jp/s?k=%E3%82%A4%E3%83%A4%E3%83%9B%E3%83%B3+%E9%AB%98%E9%9F%B3%E8%B3%AA&__mk_ja_JP=%E3%82%AB%E3%82%BF%E3%82%AB%E3%83%8A&crid=3ES5TZRUU46M2&sprefix=%E3%82%A4%E3%83%A4%E3%83%9B%E3%83%B3+%E9%AB%98%E9%9F%B3%E8%B3%AA%2Caps%2C196&ref=nb_sb_noss_1"+ price_int)#ページ読み込み
        talk((price)+ "付近商品のみ表示しました。何かありましたらもう一度声をかけてください。")
else:
    print(Notext)