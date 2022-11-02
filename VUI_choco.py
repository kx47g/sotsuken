# -*- coding: utf-8 -*-
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

value = 2
double_continue = False
firstflag = True


def show_image():
#外から触れるようにグローバル変数で定義
    global root,item, canvas, txt, value

    root = tkinter.Tk()
    root.title('test')
    root.geometry("250x300")
    canvas = tkinter.Canvas(bg = "black", width=250, height=250)
    canvas.place(x=0, y=30)
    img = Image.open('defaultimage.png')
    img= ImageTk.PhotoImage(img)
    item = canvas.create_image(0, 0, image=img, anchor=tkinter.NW)
    root.mainloop()

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
    #winsound.PlaySound("system35.wav", winsound.SND_FILENAME)
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

r = sr.Recognizer()

  
AmazonUrl = 'https://www.amazon.co.jp/'
#requests.get(url)
options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
browser = webdriver.Chrome(options=options)
browser.get("http://www.amazon.co.jp/")
element = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.NAME, "field-keywords")))
chocoUrl = "https://www.amazon.co.jp/s?bbn=2424488051&rh=n%3A2424488051%2Cp_n_feature_"

#スレッドを立ててtkinterの画像表示を開始する
thread1 = threading.Thread(target = show_image)
thread1.start()

departlist = []#カテゴリ一覧
refinelist = []#ブランド一覧
filltername = []#フィルタ一覧
fillterUrl = []#フィルタごとの遷移URL
tastelist = ["ココナッツ","カカオ","グリーンティー","オレンジ","アーモンド","チョコレート","キャラメル"]

#エージェント画像読み込み
imgOkashi = Image.open('chocoimage.jpg')
imgOkashi= ImageTk.PhotoImage(imgOkashi)
#セリフ
rooptext = "何かありましたらもう一度声をおかけください。その場合は先ほどと同じように絞り込む項目と内容を話してください。"

#talk("価格やブランド、接続方式と、重視するポイントが決まっていれば教えてください。")
linkjp = ""
link = ""
price = ""
brand = ""
order = ""
endflag = False
okasitext = "お探しの物はなんですか？"
add = "チョコレートとおっしゃっていただければ、お探ししますよ"
talk(okasitext)
count = 0
while True:
    voice_recoad()
    with sr.AudioFile("output.wav") as source:
        audio = r.record(source)
    try:
        text = r.recognize_google(audio, language='ja-JP')
        print(text)
        if "お菓子" in text:
            browser.get("https://www.amazon.co.jp/b/?node=71314051&ref_=Oct_d_odnav_d_57239051_3&pd_rd_w=5lqwu&content-id=amzn1.sym.ad2d8932-38de-4c02-8219-342e02bf2a77&pf_rd_p=ad2d8932-38de-4c02-8219-342e02bf2a77&pf_rd_r=0PM6RE9D1XENNAKCVPEZ&pd_rd_wg=rDvy0&pd_rd_r=f65588eb-641a-49cd-8368-17d26d4f0908#section:~:text=Next%20page-,%E3%82%AB%E3%83%86%E3%82%B4%E3%83%AA%E3%83%BC%E3%81%8B%E3%82%89%E6%8E%A2%E3%81%99,-%E3%82%B9%E3%83%8A%E3%83%83%E3%82%AF%E8%8F%93%E5%AD%90")
            canvas.itemconfig(item,image = imgOkashi)
            okasitext = "駄菓子やスナック、チョコなどがあります。気になるものを選んでください。"
            add = ""
            talk(okasitext)
        elif "板チョコ" in text:
            browser.get("https://www.amazon.co.jp/b/?node=2424488051&ref_=Oct_d_odnav_d_71315051_0&pd_rd_w=Tpv7q&content-id=amzn1.sym.ad2d8932-38de-4c02-8219-342e02bf2a77&pf_rd_p=ad2d8932-38de-4c02-8219-342e02bf2a77&pf_rd_r=X6M1RTVEDDDVX54BK8J4&pd_rd_wg=3JM2Z&pd_rd_r=19284c33-bf16-4b96-b631-d4c9872d178f")
            canvas.itemconfig(item,image = imgOkashi)
            break
        elif "チョコ" in text:
            browser.get("https://www.amazon.co.jp/b/?node=71315051&ref_=Oct_d_odnav_d_71314051_2&pd_rd_w=kJRPK&content-id=amzn1.sym.ad2d8932-38de-4c02-8219-342e02bf2a77&pf_rd_p=ad2d8932-38de-4c02-8219-342e02bf2a77&pf_rd_r=P7EVYQEV135BG4CEYTC3&pd_rd_wg=juDNh&pd_rd_r=d7366d85-ec2a-482a-83d9-1c551e0ef8a5")
            canvas.itemconfig(item,image = imgOkashi)
            okasitext = "どのチョコレート菓子にしますか？"
            add = ""
            talk(okasitext)
    except:
        print("認識できませんでした")
        count += 1
        if count % 2 == 0:
            talk(okasitext+add)

#絞り込み台詞
choicetext = "メーカーや価格、味などで絞り込めます。絞り込む項目と内容を話してください。"
talk(choicetext)
#ループ３
count = 0
startflag = True
while True:
    voice_recoad()
    with sr.AudioFile("output.wav") as source:
        audio = r.record(source)
    try:
        text = r.recognize_google(audio, language='ja-JP')
        print(text)  
        #安い
        if "安い" in text:
            price = "&s=price-asc-rank"
            browser.get(link + price)#ページ読み込み
            talk("価格の安い順")
            #高い
        elif "高い" in text:
            price = "&s=price-desc-rank"
            browser.get(link + price)#ページ読み込み
            talk("価格の高い順")
            #~円ぐらい
        elif "円以上" in text or "円より高い"in text:
            price_line = int(re.sub(r"\D", "", text))
            price_only = str(price_line)
            if "万円" in text and "0000" in text:
                price_line = int(str(price_line) + "0000")
            price = "&low-price=" + str(price_line)
            browser.get(link + price)#ページ読み込み
            talk(price_only+ "円以上の商品")
        elif "円以下" in text or "円より安い" in text:
            price_line = int(re.sub(r"\D", "", text))
            price_only = str(price_line)
            if "万円" in text and "0000" in text:
                price_line = int(str(price_line) + "0000")
            price = "&high-price=" + str(price_line)
            browser.get(link + price)#ページ読み込み
            talk(price_only+ "円以下の商品")
        elif "円" in text:
            price_line = int(re.sub(r"\D", "", text))
            price_only = str(price_line)
            if "万円" in text and "0000" in text:
                price_line = int(str(price_line) + "0000")
            price_line = str(price_line*0.9) + "-"  + str(price_line*1.1)
            price = "&price=" + price_line
            browser.get(link + price)#ページ読み込み
            talk(price_only+ "円付近の商品")
                #価格で絞り込む
        elif "価格" in text:
            choicetext = "価格の安い順、高い順、具体的な価格は決まっていますか？"
            talk(choicetext)
        #味で絞り込む
        elif "ココナッツ" == text:
            tasteUrl = "five_browse-bin%3A10552923051&dc&qid=1666160411&rnid=10552878051&ref=lp_2424488051_nr_p_n_feature_five_browse-bin_0"
            link = chocoUrl + tasteUrl
            browser.get(link + price)
            print("ココナッツ")
            talk(rooptext)
            startflag = False
        elif "カカオ" in text:
            print("カカオ")
            tasteUrl = "five_browse-bin%3A10552934051&dc&qid=1666155604&rnid=10552878051&ref=lp_2424488051_nr_p_n_feature_five_browse-bin_1"
            link = chocoUrl + tasteUrl
            browser.get(link + price)
            print("カカオ")
            talk(rooptext)
            startflag = False
        elif "グリーンティ" in text:
            tasteUrl = "five_browse-bin%3A10552924051&dc&qid=1666155604&rnid=10552878051&ref=lp_2424488051_nr_p_n_feature_five_browse-bin_2"
            link = chocoUrl + tasteUrl
            browser.get(link + price)
            print("グリーンティ")
            talk(rooptext)
            startflag = False
        elif "オレンジ" in text:
            tasteUrl = "five_browse-bin%3A10552889051&dc&qid=1666155604&rnid=10552878051&ref=lp_2424488051_nr_p_n_feature_five_browse-bin_3"
            link = chocoUrl + tasteUrl
            browser.get(link + price)
            print("オレンジ")
            talk(rooptext)
            startflag = False
        elif "アーモンド" in text:
            tasteUrl = "five_browse-bin%3A10552898051&dc&qid=1666155604&rnid=10552878051&ref=lp_2424488051_nr_p_n_feature_five_browse-bin_4"
            link = chocoUrl + tasteUrl
            browser.get(link + price)
            print("アーモンド")
            talk(rooptext)
            startflag = False
        elif "チョコ" in text:
            tasteUrl = "five_browse-bin%3A10552915051&dc&qid=1666155604&rnid=10552878051&ref=lp_2424488051_nr_p_n_feature_five_browse-bin_5"
            link = chocoUrl + tasteUrl
            browser.get(link + price)
            print("チョコレート")
            talk(rooptext)
            startflag = False
        elif "キャラメル" in text:
            tasteUrl = "five_browse-bin%3A10552946051&dc&qid=1666155604&rnid=10552878051&ref=lp_2424488051_nr_p_n_feature_five_browse-bin_6"
            link = chocoUrl + tasteUrl
            browser.get(link + price)
            print("キャラメル")
            talk(rooptext)
            startflag = False
        elif "味" in text:
            talk("ココナッツ、カカオ、グリーンティなどの種類があります。どれにいたしましょう。")
        #チョコレートタイプで絞り込む
        elif "ホワイト" in text:
            TypeUrl = "two_browse-bin%3A10511140051&dc&qid=1666240598&rnid=10511138051&ref=lp_2424488051_nr_p_n_feature_two_browse-bin_0"
            link = chocoUrl + TypeUrl
            browser.get(link + price)
            talk(rooptext)
            startflag = False
        elif "ミルク" in text:
            TypeURL = "two_browse-bin%3A10511139051&dc&qid=1666240325&rnid=10511138051&ref=lp_2424488051_nr_p_n_feature_two_browse-bin_1"
            link = chocoUrl + TypeUrl
            browser.get(link + price)
            talk(rooptext)
            startflag = False
        elif "ダーク" in text:
            TypeUrl = "two_browse-bin%3A10511141051&dc&qid=1666240325&rnid=10511138051&ref=lp_2424488051_nr_p_n_feature_two_browse-bin_2"
            link = chocoUrl + TypeUrl
            browser.get(link + price)
            talk(rooptext)
            startflag = False
        #メーカーで絞り込む
        elif "ロッテ" in text:
            MakerUrl = "s?bbn=2424488051&rh=n%3A2424488051%2Cp_89%3A%E3%83%AD%E3%83%83%E3%83%86&dc&qid=1666241034&rnid=2321255051&ref=lp_2424488051_nr_p_89_1"
            link = AmazonUrl + MakerUrl
            browser.get(link)
            talk(rooptext)
            startflag = False
        elif "キャドバリー" in text:
            MakerUrl = "s?bbn=2424488051&rh=n%3A2424488051%2Cp_89%3Aキャドバリー&dc&qid=1666240666&rnid=2321255051&ref=lp_2424488051_nr_p_89_2"
            link = AmazonUrl + MakerUrl
            browser.get(link)
            talk(rooptext)
            startflag = False
        elif "ブルボン" in text:
            MakerUrl = "s?bbn=2424488051&rh=n%3A2424488051%2Cp_89%3Aブルボン&dc&qid=1666240666&rnid=2321255051&ref=lp_2424488051_nr_p_89_3"
            link = AmazonUrl + MakerUrl
            browser.get(link)
            talk(rooptext)
            startflag = False
        elif "リンツ" in text:
            MakerUrl = "s?bbn=2424488051&rh=n%3A2424488051%2Cp_89%3ALindt%28リンツ%29&dc&qid=1666240666&rnid=2321255051&ref=lp_2424488051_nr_p_89_4"
            link = AmazonUrl + MakerUrl
            browser.get(link)
            talk(rooptext)
            startflag = False
        elif "明治" in text:
            MakerUrl = "s?bbn=2424488051&rh=n%3A2424488051%2Cp_89%3A明治&dc&ds=v1%3ArUM%2B7edKfR3VRj3ivDsU2FC3KW9lTQNrzpI4eb76hyY&qid=1666242010&rnid=2321255051&ref=sr_nr_p_89_1"
            link = AmazonUrl + MakerUrl
            browser.get(link)
            talk(rooptext)
            startflag = False
        elif "森永" in text:
            MakerUrl = "s?bbn=2424488051&rh=n%3A2424488051%2Cp_89%3A森永製菓&dc&qid=1666242210&rnid=2321255051&ref=sr_nr_p_89_1&ds=v1%3AU0UBz3RNOnv2o9HdiQENlsIyGnmkCDOleDU%2B8KswzUs"
            link = AmazonUrl + MakerUrl
            browser.get(link)
            talk(rooptext)
            startflag = False
    except:
        print("認識できませんでした")
        count += 1
        if count % 2 == 0 and startflag == True:
            talk(choicetext)