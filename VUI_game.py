from tkinter.constants import E
import keyboard
import sys
import tkinter
from PIL import Image, ImageTk
import winsound
import time
import datetime
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

#制御用変数
double_continue = False
firstflag = True
endflag = False
soloflag = False
genreflag = ""
reguflag = ""

#{"title": "", "genre": "", "regu": "", "solo": "", }

#ジャンルごとのソフト一覧
RPG = re.compile(r'ファイアーエムブレム風花雪月|風花雪月')

#ジャンルごとのソフト一覧
Switch=[
    {"title":RPG,"genre":"シミュレーション","regu":"B","solo":True,"URL":"https://www.nintendo.co.jp/switch/anvya/pc/index.html"},
    {"title":"PokémonLEGENDSアルセウス-ポケモン","genre":"RPG","regu":"A","solo":True,"URL":"https://www.pokemon.co.jp/ex/legends_arceus/ja/"},
    {"title":"ドラゴンクエストXI過ぎ去りし時を求めてS　ドラクエイレブンドラクエ11","genre":"RPG","regu":"A","solo":True,"URL":"https://www.dq11.jp/s/pf/index.html"},
    {"title":"鬼滅の刃ヒノカミ血風譚","genre":"アクション","regu":"C","solo":False,"URL":"https://game.kimetsu.com/hinokami/"},
    {"title":"星のカービィディスカバリー","genre":"アクション","regu":"A","solo":False,"URL":"https://www.nintendo.co.jp/switch/arzga/index.html"},
    {"title":"モンスターハンターライズ：サンブレイク　モンハンライズ","genre":"アクション","regu":"C","solo":True,"URL":"https://www.monsterhunter.com/rise-sunbreak/ja/"},
    {"title":"十三機兵防衛圏","genre":"アドベンチャー","regu":"C","solo":True,"URL":"https://13sar.jp/"},
    {"title":"ペーパーマリオオリガミキング","genre":"アドベンチャー","regu":"A","solo":True,"URL":"https://www.nintendo.co.jp/switch/aruua/index.html"},
    {"title":"あつまれ　どうぶつの森","genre":"シミュレーション","regu":"A","solo":True,"URL":"https://www.nintendo.co.jp/switch/acbaa/index.html"},
    {"title":"StardewValley-スタードゥバレー","genre":"シミュレーション","regu":"A","solo":True,"URL":"https://store-jp.nintendo.com/list/software/70010000005423.html"},
    {"title":"ゼルダの伝説ブレスオブザワイルドゼルダbow","genre":"オープンワールド","regu":"B","solo":True,"URL":"https://www.nintendo.co.jp/software/feature/zelda/index.html"},
    {"title":"XenobladeDefinitiveEdition,Switchゼノブレイド","genre":"RPG","regu":"C","solo":True,"URL":"https://www.nintendo.co.jp/switch/aubqa/index.html"},
    {"title":"スプラトゥーン3スプラ3","genre":"シューティング","regu":"A","solo":False,"URL":"https://www.nintendo.co.jp/switch/av5ja/index.html"},
    {"title":"apexエーペックスレジェンズ","genre":"シューティング","regu":"D","solo":False,"URL":"https://www.ea.com/ja-jp/games/apex-legends"},
    {"title":"DeadbyDaylightデッドバイデイライト","genre":"ホラー","regu":"Z","solo":False,"URL":"https://deadbydaylight.com/ja/"},
    {"title":"リトルナイトメア2","genre":"ホラー","regu":"C","solo":True,"URL":"https://n6ls.bn-ent.net/"},
    {"title":"リングフィットアドベンチャー","genre":"フィットネス","regu":"A","solo":True,"URL":"https://www.nintendo.co.jp/ring/"},
    {"title":"FitBoxing2フィットボクシング","genre":"フィットネス","regu":"A","solo":True,"URL":"https://fitboxing.net/2/"},
    {"title":"NintendoSwitchSportsニンテンドースイッチスポーツ","genre":"スポーツ","regu":"A","solo":False,"URL":"https://www.nintendo.co.jp/switch/as8sa/"},
    {"title":"eBASEBALLパワフルプロ野球2022イーベースボール","genre":"スポーツ","regu":"A","solo":False,"URL":"https://www.konami.com/pawa/2022/"},
    {"title":"マリオカート8デラックス","genre":"レーシング","regu":"A","solo":False,"URL":"https://www.nintendo.co.jp/switch/aabpa/index.html"},
    {"title":"ドラゴンクエストX目覚めし五つの種族オフラインドラゴンクエスト10オフラインドラクエ10オフライン","genre":"RPG","regu":"A","solo":True,"URL":"https://www.dqx.jp/ad/DQXoff/"},
    {"title":"ドラゴンボールZKAKAROTドラゴンボールゼットカカロット","genre":"アクションRPG","regu":"B","solo":True,"URL":"https://dbar.bn-ent.net/"},
    {"title":"ペルソナ5スクランブルザファントムストライカーズペルソナファイブスクランブル","genre":"アクションRPG","regu":"B","solo":True,"URL":"https://p5s.jp/"},
    {"title":"夜廻三夜回りさん　よまわりさん","genre":"夜道探索アクション","regu":"C","solo":True,"URL":"https://nippon1.jp/consumer/yomawari3/enter.html"},
]#スイッチのソフト一覧
PS=[{"title":"ドラゴンクエストXI過ぎ去りし時を求めてSドラクエイレブンドラクエ11","genre":"RPG","regu":"A","solo":True,"URL":"https://www.dq11.jp/s/pf/index.html"},
    {"title":"十三機兵防衛圏","genre":"アドベンチャー","regu":"C","solo":True,"URL":"https://13sar.jp/"},
    {"title":"apexエーペックスレジェンズ","genre":"シューティング","regu":"D","solo":False,"URL":"https://www.ea.com/ja-jp/games/apex-legends"},
    {"title":"DeadbyDaylightデッドバイデイライト","genre":"ホラー","regu":"Z","solo":False,"URL":"https://deadbydaylight.com/ja/"},
    {"title":"リトルナイトメア2","genre":"ホラー","regu":"C","solo":True,"URL":"https://n6ls.bn-ent.net/"},
    {"title":"ドラゴンクエストX目覚めし五つの種族オフラインドラゴンクエスト10ドラクエ10","genre":"RPG","regu":"A","solo":True,"URL":"https://www.dqx.jp/ad/DQXoff/"},
    {"title":"Marvel‘sSpider-Man:MilesMoralesマーベルスパイダーマン","genre":"アクション","regu":"C","solo":True,"URL":"https://www.playstation.com/ja-jp/games/marvels-spider-man-remastered/"},
    {"title":"ドラゴンボールZKAKAROTドラゴンボールゼットカカロット","genre":"アクション","regu":"B","solo":True,"URL":"https://dbar.bn-ent.net/"},
    {"title":"ペルソナ5スクランブルザファントムストライカーズペルソナファイブスクランブル","genre":"アクションRPG","regu":"B","solo":True,"URL":"https://p5s.jp/"},
    {"title":"クラッシュ・バンディングー4とんでもマルチバース","genre":"アクション","regu":"A","solo":False,"URL":"https://www.crashbandicoot.com/ja/crash4/home"},
    {"title":"初音ミクProjectDIVAFutureToneDXプロジェクトディーヴァ","genre":"リズムアクション","regu":"C","solo":True,"URL":"https://miku.sega.jp/FT/"},
    {"title":"Detroit:BecomeHumanデトロイトビカムヒューマン","genre":"アクション","regu":"D","solo":True,"URL":"https://www.playstation.com/ja-jp/games/detroit-become-human/"},
    {"title":"バイオハザードヴィレッジ","genre":"ホラー","regu":"D","solo":True,"URL":"https://www.capcom.co.jp/biohazard/village/"},
    {"title":"夜廻三夜回りさん　よまわりさん","genre":"夜道探索アクション","regu":"C","solo":True,"URL":"https://nippon1.jp/consumer/yomawari3/enter.html"},
]
#プレステのソフト一覧

PC=[{"title":"ドラゴンクエストXI過ぎ去りし時を求めてSドラクエイレブンドラクエ11","genre":"RPG","regu":"A","solo":True,"URL":"https://www.dq11.jp/s/pf/index.html"},
    {"title":"モンスターハンターライズ：サンブレイク　モンハンライズ","genre":"アクション","regu":"C","solo":True,"URL":"https://www.monsterhunter.com/rise-sunbreak/ja/"},
    {"title":"apexエーペックスレジェンズ","genre":"シューティング","regu":"D","solo":False,"URL":"https://www.ea.com/ja-jp/games/apex-legends"},
    {"title":"DeadbyDaylightデッドバイデイライト","genre":"ホラー","regu":"Z","solo":False,"URL":"https://store-jp.nintendo.com/list/software/70010000016125.html"},
    {"title":"リトルナイトメア2","genre":"ホラー","regu":"C","solo":True,"URL":"https://n6ls.bn-ent.net/"},
    {"title":"ドラゴンクエストX目覚めし五つの種族オフラインドラゴンクエスト10ドラクエ10","genre":"RPG","regu":"A","solo":True,"URL":"https://www.dqx.jp/ad/DQXoff/"},
    {"title":"Marvel‘sSpider-Man:MilesMoralesマーベルスパイダーマン","genre":"アクション","regu":"C","solo":True,"URL":"https://www.playstation.com/ja-jp/games/marvels-spider-man-remastered/"},
    {"title":"Detroit:BecomeHumanデトロイトビカムヒューマン","genre":"アクション","regu":"D","solo":True,"URL":"https://www.playstation.com/ja-jp/games/detroit-become-human/"},
]#PCゲームソフト一覧
#最終的に紹介するゲームソフト
gamelist = []

#条件分岐
#括弧の中のいずれかのワードが喋られた場合,各関数のif文が反応します。
"""
PCpattern = re.compile(r'PC|パソコン|ゲーミング')
SWpattern = re.compile(r'ニンテンドースイッチ|スイッチ|switch|SWITCH')
PSpattern = re.compile(r'プレイステーション|プレステ|PlayStation|PS')
"""

#変数名のPはポジティブ、Nはネガティブの意です。
PSolopattern = re.compile(r'好き|ソロ|一人|はい|うん|そう|せや')
Npattern = re.compile(r'じゃない|じゃあない|ではない|いや|嫌|困る|苦手|嫌い')

#セリフ
Hellotext = "  ゲームソフトを紹介します"
ConsoleQ = "どのゲーム機を持っていますか？"
friendORsoloQ = "ゲームは一人でプレイするのが好きですか？"
RecentlyQ = "最近なんのゲームをやりましたか？"
TimeQ = "いちにちに何時間くらいゲームをしますか？"
Notext = "認識できませんでした"

#ブラウザーを動作させる準備
#driver_path = "C:\\driver\\chromedriver.exe"
#options = webdriver.ChromeOptions()
#options.add_experimental_option('excludeSwitches', ['enable-logging'])
#browser = webdriver.Chrome(options=options)
#browser.get("http://www.amazon.co.jp/")

#ブラウザを動作させるための変数
linkjp = ""
link = ""
price = ""
brand = ""
order = ""

#喋るための準備
r = sr.Recognizer()

#### 関数 ####
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

def gameList(text):
    if 'PC' in text or 'パソコン' in text or 'ゲーミング' in text:
        gamelist.extend(PC)
    elif 'ニンテンドースイッチ' in text or 'スイッチ' in text or 'switch' in text or 'SWITCH' in text:
        gamelist.extend(Switch)
    elif 'PleyStation' in text or 'PS' in text or 'プレイステーション' in text or 'プレステ' in text:
        gamelist.extend(PS)

def gamefriendORsolo(text):
    global soloflag
    if bool(PSolopattern.search(text)):
        if bool(Npattern.search(text)):
            soloflag = False
        else:
            soloflag = True
    else:
        soloflag = False

def samplegametitle(text):
    global genreflag, reguflag
    for i in range(len(gamelist)):
        if bool(gamelist[i]["title"].search(text)):
            genreflag = gamelist[i]["genre"]
            reguflag = gamelist[i]["regu"]

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

def erroroutput(text):
    f = open('errortext.txt', 'a')

    datalist = [text]
    f.writelines(datalist)

    f.close()

#　Main処理開始　#
erroroutput(datetime.datetime.now().strftime('%Y年%m月%d日 %H:%M:%S'))
erroroutput('\n')

talk(Hellotext)

talk(ConsoleQ)
while True:
    try:
        gameList(voiceTOtext())
        print(gamelist)
        break
    except:
        print(Notext)

talk(friendORsoloQ)
while True:
    try:
        gamefriendORsolo(voiceTOtext())
        print(soloflag)
        break
    except:
        print(Notext)

talk(RecentlyQ)
while True:
    try:
        samplegametitle(voiceTOtext())
        print(genreflag)
        print(reguflag)
        break
    except:
        print(Notext)

talk(TimeQ)
while True:
    try:
        text = voiceTOtext()
        Timehour = int(re.sub(r"\D", "", text))
        timeflag = Timehour
        print(timeflag)
        break
    except:
        print(Notext)

outputlistT = []

#ゲーム機、好きなジャンル、対象年齢、ソロプレイ派かマルチ派かで絞り込み
for i in range(len(gamelist)):
    test = 0
    if gamelist[i]["regu"] == reguflag:
        test += 1
    if gamelist[i]["genre"] == genreflag:
        test += 1
    if soloflag == True:
        test += 1
    if test == 3:
        a = [{"title":gamelist[i]["title"],
              "genre":gamelist[i]["genre"],
              "regu":gamelist[i]["regu"],
              "solo":gamelist[i]["solo"]}]
        outputlistT.extend(a)

#ユーザーが好きそうなゲーム一覧
print("T",outputlistT)

outputlistF = []
for item in gamelist:
    if item in outputlistT:
        pass

    else:
        outputlistF.append(item)

#ユーザーがやったことなさそうなゲーム一覧
print("F",outputlistF)

valueT = 0

#それぞれのリストから紹介するゲームの個数をパランスよく決める
if len(outputlistT) == 0:
    valueT = 0
elif len(outputlistT) < 2:
    valueT = len(outputlistT)
else:

    valueT = 2

valueF = 3-valueT

videolist = []

#ゲームリストからランダムにゲームを選び、最終的に紹介するゲーム一覧をきめる。
videolist.extend(random.sample(outputlistT, valueT))
print("T", videolist)
videolist.extend(random.sample(outputlistF, valueF))
print("T&F",videolist)

driver_path = "C:\\driver\\chromedriver.exe"
options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
browser = webdriver.Chrome(options=options)

#紹介の実行　デフォルトでは１０秒おきに次のゲーム画面に移動
for i in range(3):
    browser.get(videolist[i]["URL"])
    time.sleep(10)