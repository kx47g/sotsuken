# -*- coding: utf-8 -*-
from tkinter.constants import E, FIRST
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
samplename = ""
glflag = False

#{"title": "", "genre": "", "regu": "", "solo": "", }

#ジャンルごとのソフト一覧
RPG2 = re.compile(r'PokémonLEGENDSアルセウス|ポケモンアルセウス|アルセウス')
RPG3 = re.compile(r'ドラゴンクエストXI過ぎ去りし時を求めてS|ドラゴンクエスト11|ドラクエ11|ドラゴンクエストイレブン|ドラクエイレブン')
RPG4 = re.compile(r'XenobladeDefinitiveEdition|ゼノブレイド')
RPG = re.compile(r'ドラゴンクエストX目覚めし五つの種族オフライン|ドラゴンクエスト10オフライン|ドラクエ10オフライン|ドラクエ10')
ACT = re.compile(r'鬼滅の刃ヒノカミ血風譚|鬼滅の刃|')
ACT2 = re.compile(r'星のカービィ ディスカバリー|カービィ ディスカバリー|ディスカバリー|星のカービィ')
ACT3 = re.compile(r'モンスターハンターライズ：サンブレイク|モンハンライズ サンブレイク|サンブレイク|モンハンライズ')
ACT4 = re.compile(r'Marvel‘sSpider-Man:MilesMorales|マーベルスパイダーマン')
ACT5 = re.compile(r'クラッシュ・バンディングー4とんでもマルチバース|クラッシュ・バンディグ')
ACT6 = re.compile(r'Detroit Become Human|デトロイト ビカム ヒューマン')
LACT = re.compile(r'初音ミクProjectDIVAFutureToneDX|プロジェクトディーヴァ|初音ミク')
ACTRPG = re.compile(r'ドラゴンボールZKAKAROT|ドラゴンボールゼットカカロット')
ACTRPG2 = re.compile(r'ペルソナ5スクランブルザファントムストライカーズ|ペルソナ5スクランブル|ペルソナファイブスクランブル')
AD = re.compile(r'十三機兵防衛圏')
AD2 = re.compile(r'ペーパーマリオオリガミキング|オリガミキング')
SHUM = re.compile(r'あつまれどうぶつの森|あつ森')
SHUM2 = re.compile(r'StardewValley|スターデューバレー|スタードゥバレー')
SHUM3 = re.compile(r'ファイアーエムブレム 風花雪月|風花雪月')
SHUT = re.compile(r'スプラトゥーン3|Splatoon 3|スプラ3')
SHUT2 = re.compile(r'apex|エーペックス|エイベックス')
OPW = re.compile(r'ゼルダの伝説ブレスオブザワイルド|ゼルダ BOW')
HOL = re.compile(r'Deadby Day light|デッドバイデイライト')
HOL2 = re.compile(r'リトルナイトメア2|リトルナイトメア')
HOL3 = re.compile(r'バイオハザード ヴィレッジ|バイオ')
FIT = re.compile(r'リングフィットアドベンチャー|リングフィット')
FIT2 = re.compile(r'FitBoxing2|フィットボクシング')
SPO = re.compile(r'Nintendo Switch Sports|ニンテンドースイッチスポーツ|スイッチスポーツ')
SPO2 = re.compile(r'eBASEBALLパワフルプロ野球2022|イーベースボール|パワプロ')
RA = re.compile(r'マリオカート8デラックス|マリカー|マリカ')
YACT = re.compile(r'夜廻三|夜回りさん|よまわりさん')

#ジャンルごとのソフト一覧
Switch=[{"Ntext": "RPGの代表にふれたことはありますか？","tname": "ドラゴンクエストテン　目覚めしいつつの種族オフライン","title":RPG,"genre":"RPG","regu":"A","solo":True,"URL":"https://www.dqx.jp/ad/DQXoff/"},
        {"Ntext": "新しいポケモンを体験してみませんか？","tname": "ポケモンレジェンズアルセウス","title":RPG2,"genre":"RPG","regu":"A","solo":True,"URL":"https://www.pokemon.co.jp/ex/legends_arceus/ja/"},
        {"Ntext": "ドラゴンクエストの世界に触れてみませんか？","tname": "ドラゴンクエストイレブン　過ぎ去りしときを求めて","title":RPG3,"genre":"RPG","regu":"A","solo":True,"URL":"https://www.dq11.jp/s/pf/index.html"},
        {"Ntext": "圧倒的なボリューム、プレイして世界かんに浸かる貴方が見えました","tname": "ゼノブレイド","title":RPG4,"genre":"RPG","regu":"C","solo":True,"URL":"https://www.nintendo.co.jp/switch/aubqa/index.html"},
        {"Ntext": "お一人でプレイをするのが好きそうなあなたには、アクションをおすすめします。","tname": "きめつのやいば　ヒノカミけっぷうたん","title":ACT,"genre":"アクション","regu":"C","solo":False,"URL":"https://game.kimetsu.com/hinokami/"},
        {"Ntext": "ほおばりヘンケイによりさまざまなアクションが可能になったカービィはいかがですか？","tname": "星のカービィ　ディスカバリー","title":ACT2,"genre":"アクション","regu":"A","solo":False,"URL":"https://www.nintendo.co.jp/switch/arzga/index.html"},
        {"Ntext": "1人でも、みんなでも楽しめる、アクションゲームはどうですか？","tname": "モンスターハンターライズ　サンブレイク","title":ACT3,"genre":"アクション","regu":"C","solo":True,"URL":"https://www.monsterhunter.com/rise-sunbreak/ja/"},
        {"Ntext": "ドラゴンボール好きにはたまらない","tname": "ドラゴンボールゼットカカロット","title":ACTRPG,"genre":"アクションRPG","regu":"B","solo":True,"URL":"https://dbar.bn-ent.net/"},
        {"Ntext": "君も悪を滅する心の怪盗団のメンバーに","tname": "ペルソナファイブ　スクランブルザファントムストライカーズ","title":ACTRPG2,"genre":"アクションRPG","regu":"B","solo":True,"URL":"https://p5s.jp/"},
        {"Ntext": "このゲームでしか味わえない読後感を体験してみませんか？","tname": "じゅうさんきへいぼうえいけん","title":AD,"genre":"アドベンチャー","regu":"C","solo":True,"URL":"https://13sar.jp/"},
        {"Ntext": "ペラペラな世界で謎解きと360°バトルのアドベンチャーを体験してみませんか？","tname": "ペーパーマリオオリガミキング","title":AD2,"genre":"アドベンチャー","regu":"A","solo":True,"URL":"https://www.nintendo.co.jp/switch/aruua/index.html"},
        {"Ntext": "ほのぼのとした島生活をしませんか？","tname": "あつまれどうぶつの森","title":SHUM,"genre":"シミュレーション","regu":"A","solo":True,"URL":"https://www.nintendo.co.jp/switch/acbaa/index.html"},
        {"Ntext": "自給自足のシュミレーションゲームはいかがですか？","tname": "スタードゥバレー","title":SHUM2,"genre":"シミュレーション","regu":"A","solo":True,"URL":"https://store-jp.nintendo.com/list/software/70010000005423.html"},
        {"Ntext": "ふうかせつげつ、この言葉がかっこいいと思った貴方はハマります","tname": "ファイアーエムブレムふうかせつげつ","title":SHUM3,"genre":"シミュレーション","regu":"B","solo":True,"URL":"https://www.nintendo.co.jp/switch/anvya/pc/index.html"},
        {"Ntext": "何もかもぶちまけたい時ってありますよね、そんな貴方に。","tname": "スプラトゥーンスリー","title":SHUT,"genre":"シューティング","regu":"A","solo":False,"URL":"https://www.nintendo.co.jp/switch/av5ja/index.html"},
        {"Ntext": "仲間とゲームをするのが好きそうなあなたには、シューティングゲームをおすすめします。","tname": "エーペックス","title":SHUT2,"genre":"シューティング","regu":"D","solo":False,"URL":"https://www.ea.com/ja-jp/games/apex-legends"},
        {"Ntext": "枠にとらわれないあなただけの冒険をしませんか？","tname": "ゼルダの伝説ブレスオブザワイルド","title":OPW,"genre":"オープンワールド","regu":"B","solo":True,"URL":"https://www.nintendo.co.jp/software/feature/zelda/index.html"},
        {"Ntext": "マルチプレイアクションのサバイバルホラーゲームはいかがですか？","tname": "デッドバイデイライト","title":HOL,"genre":"ホラー","regu":"Z","solo":False,"URL":"https://deadbydaylight.com/ja/"},
        {"Ntext": "この世界観は唯一無二です。不気味ながら引き込まれる体験をどうぞ","tname": "リトルナイトメアツー","title":HOL2,"genre":"ホラー","regu":"C","solo":True,"URL":"https://n6ls.bn-ent.net/"},
        {"Ntext": "一人だからこそできる、フィットネスをおすすめします。","tname": "リングフィットアドベンチャー","title":FIT,"genre":"フィットネス","regu":"A","solo":True,"URL":"https://www.nintendo.co.jp/ring/"},
        {"Ntext": "ボクシングを通して自分自身と対戦。エクササイズのリング場へようこそ","tname": "フィットボクシングツー","title":FIT2,"genre":"フィットネス","regu":"A","solo":True,"URL":"https://fitboxing.net/2/"},
        {"Ntext": "スポーツする道具が無い？言い訳です。道具のハッピーセットを貴方に","tname": "ニンテンドースイッチスポーツ","title":SPO,"genre":"スポーツ","regu":"A","solo":False,"URL":"https://www.nintendo.co.jp/switch/as8sa/"},
        {"Ntext": "キャラクターカスタマイズができる、シュミレーションゲームをおすすめします。","tname": "イーベースボールパワフルプロ野球二千二十二","title":SPO2,"genre":"スポーツ","regu":"A","solo":False,"URL":"https://www.konami.com/pawa/2022/"},
        {"Ntext": "ともだちや家族と集まって遊べる、レースゲームをおすすめします。","tname": "マリオカートエイトデラックス","title":RA,"genre":"レーシング","regu":"A","solo":False,"URL":"https://www.nintendo.co.jp/switch/aabpa/index.html"},
        {"Ntext": "子どものころに感じた怖さを呼び起こす。","tname": "よまわりさん" ,"title":YACT,"genre":"夜道探索アクション","regu":"C","solo":True,"URL":"https://nippon1.jp/consumer/yomawari3/enter.html"},
]#スイッチのソフト一覧
PS=[{"Ntext": "RPGの代表にふれたことはありますか？","tname": "ドラゴンクエストテン　目覚めしいつつの種族オフライン","title":RPG,"genre":"RPG","regu":"A","solo":True,"URL":"https://www.dqx.jp/ad/DQXoff/"},
    {"Ntext": "ドラゴンクエストの世界に触れてみませんか？","tname": "ドラゴンクエストイレブン　過ぎ去りしときを求めて","title":RPG3,"genre":"RPG","regu":"A","solo":True,"URL":"https://www.dq11.jp/s/pf/index.html"},
    {"Ntext": "このゲームでしか味わえない読後感を体験してみませんか？","tname": "じゅうさんきへいぼうえいけん","title":AD,"genre":"アドベンチャー","regu":"C","solo":True,"URL":"https://13sar.jp/"},
    {"Ntext": "仲間とゲームをするのが好きそうなあなたには、シューティングゲームをおすすめします。","tname": "エーペックス","title":SHUT2,"genre":"シューティング","regu":"D","solo":False,"URL":"https://www.ea.com/ja-jp/games/apex-legends"},
    {"Ntext": "マルチプレイアクションのサバイバルホラーゲームはいかがですか？","tname": "デッドバイデイライト","title":HOL,"genre":"ホラー","regu":"Z","solo":False,"URL":"https://deadbydaylight.com/ja/"},
    {"Ntext": "この世界観は唯一無二です。不気味ながら引き込まれる体験をどうぞ","tname": "リトルナイトメアツー","title":HOL2,"genre":"ホラー","regu":"C","solo":True,"URL":"https://n6ls.bn-ent.net/"},
    {"Ntext": "映画の世界を駆け回りたい、と思ったことがある方におすすめします。","tname": "マーベル、スパイダーマン","title":ACT4,"genre":"アクション","regu":"C","solo":True,"URL":"https://www.playstation.com/ja-jp/games/marvels-spider-man-remastered/"},
    {"Ntext": "ドラゴンボール好きにはたまらない","tname": "ドラゴンボールゼットカカロット","title":ACTRPG,"genre":"アクション","regu":"B","solo":True,"URL":"https://dbar.bn-ent.net/"},
    {"Ntext": "君も悪を滅する心の怪盗団のメンバーに","tname": "ペルソナファイブ　スクランブルザファントムストライカーズ","title":ACTRPG2,"genre":"アクションRPG","regu":"B","solo":True,"URL":"https://p5s.jp/"},
    {"Ntext": "1台の本体で一緒にあそべる、アクションゲームをおすすめします。","tname": "クラッシュ・バンディングーフォー、とんでもマルチバース","title":ACT5,"genre":"アクション","regu":"A","solo":False,"URL":"https://www.crashbandicoot.com/ja/crash4/home"},
    {"Ntext": "ボカロの殿堂入り。いつだって最前線。そんな彼女の集大成を一緒に","tname": "初音ミクプロジェクトディーヴァ","title":LACT,"genre":"リズムアクション","regu":"C","solo":True,"URL":"https://miku.sega.jp/FT/"},
    {"Ntext": "近未来の体験をあなたに","tname": "デトロイトビカムヒューマン","title":ACT6,"genre":"アクション","regu":"D","solo":True,"URL":"https://www.playstation.com/ja-jp/games/detroit-become-human/"},
    {"Ntext": "一人でするサバイバルホラーって楽しいですよね。","tname": "バイオハザードヴィレッジ","title":HOL3,"genre":"ホラー","regu":"D","solo":True,"URL":"https://www.capcom.co.jp/biohazard/village/"},
    {"Ntext": "子どものころに感じた怖さを呼び起こす。","tname": "よまわりさん","title":YACT,"genre":"夜道探索アクション","regu":"C","solo":True,"URL":"https://nippon1.jp/consumer/yomawari3/enter.html"},
]
#プレステのソフト一覧

PC=[{"Ntext": "RPGの代表にふれたことはありますか？","tname": "ドラゴンクエストテン　目覚めしいつつの種族オフライン","title":RPG,"genre":"RPG","regu":"A","solo":True,"URL":"https://www.dqx.jp/ad/DQXoff/"},
    {"Ntext": "ドラゴンクエストの世界に触れてみませんか？","tname": "ドラゴンクエストイレブン　過ぎ去りしときを求めて","title":RPG3,"genre":"RPG","regu":"A","solo":True,"URL":"https://www.dq11.jp/s/pf/index.html"},
    {"Ntext": "1人でも、みんなでも楽しめる、アクションゲームはどうですか？","tname": "モンスターハンターライズ　サンブレイク","title":ACT3,"genre":"アクション","regu":"C","solo":True,"URL":"https://www.monsterhunter.com/rise-sunbreak/ja/"},
    {"Ntext": "仲間とゲームをするのが好きそうなあなたには、シューティングゲームをおすすめします。","tname": "エーペックス","title":SHUT2,"genre":"シューティング","regu":"D","solo":False,"URL":"https://www.ea.com/ja-jp/games/apex-legends"},
    {"Ntext": "マルチプレイアクションのサバイバルホラーゲームはいかがですか？","tname": "デッドバイデイライト","title":HOL,"genre":"ホラー","regu":"Z","solo":False,"URL":"https://store-jp.nintendo.com/list/software/70010000016125.html"},
    {"Ntext": "この世界観は唯一無二です。不気味ながら引き込まれる体験をどうぞ","tname": "リトルナイトメアツー","title":HOL2,"genre":"ホラー","regu":"C","solo":True,"URL":"https://n6ls.bn-ent.net/"},
    {"Ntext": "「映画の世界を駆け回りたい」と思ったことがある方におすすめします。","tname": "マーベル、スパイダーマン","title":ACT4,"genre":"アクション","regu":"C","solo":True,"URL":"https://www.playstation.com/ja-jp/games/marvels-spider-man-remastered/"},
    {"Ntext": "近未来の体験をあなたに","tname": "デトロイトビカムヒューマン","title":ACT6,"genre":"アクション","regu":"D","solo":True,"URL":"https://www.playstation.com/ja-jp/games/detroit-become-human/"},
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
Oktext = [' OKです ',' 了解しました ',' 分かりました ',' 確認できました ']

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
    l = 0
    if 'PC' in text or 'パソコン' in text or 'ゲーミング' in text:
        gamelist.extend(PC)
        l += 1
    if 'ニンテンドースイッチ' in text or 'スイッチ' in text or 'スイッチライト' in text or  'switch' in text or 'SWITCH' in text:
        gamelist.extend(Switch)
        l += 1
    if 'PleyStation' in text or 'PS' in text or 'プレイステーション' in text or 'プレステ' in text:
        gamelist.extend(PS)
        l += 1
    gamelist.extend(Switch)
    gamelist.extend(PC)
    gamelist.extend(PS)
    #print(gamelist)

def gamefriendORsolo(text):
    global soloflag,genreflag, reguflag
    if bool(PSolopattern.search(text)):
        if bool(Npattern.search(text)):
            soloflag = False
            if glflag == True:
                l = []
                for i in range(len(gamelist)):
                    if bool(gamelist[i]["solo"].search(True)):
                        l.extend(gamelist[i])
                    a = random.choice(l)
                    genreflag = a["title"]
                    reguflag = a["regu"]
        else:
            soloflag = True
    else:
        soloflag = False

def samplegametitle(text):
    global genreflag, reguflag, glflag, samplename
    for i in range(len(gamelist)):
        if bool(gamelist[i]["title"].search(text)):
            genreflag = gamelist[i]["genre"]
            reguflag = gamelist[i]["regu"]
            samplename = gamelist[i]["tname"]
            glflag =- True        


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
count = 0
while True:
    try:
        gameList(voiceTOtext())
        #print(gamelist)
        print(random.sample(Oktext,1))
        break
    except:
        print(Notext)
        count += 1
        if count % 2 == 0:
            talk(ConsoleQ+"おっしゃっていただければ、その内容を参考に、おすすめのゲームを紹介できます")
            print("ニンテンドースイッチ　など")

count = 0
talk(friendORsoloQ)
while True:
    try:
        gamefriendORsolo(voiceTOtext())
        #print(soloflag)
        print(random.sample(Oktext,1))
        break
    except:
        print(Notext)
        count += 1
        if count % 2 == 0:
            talk(friendORsoloQ)

count = 0
talk(RecentlyQ)
while True:
    try:
        samplegametitle(voiceTOtext())
        #print(genreflag)
        #print(reguflag)
        print(random.sample(Oktext,1))
        break
    except:
        print(Notext)
        count += 1
        if count % 2 == 0:
            talk(RecentlyQ)

count = 0
talk(TimeQ)
while True:
    try:
        text = voiceTOtext()
        Timehour = int(re.sub(r"\D", "", text))
        timeflag = Timehour
        #print(timeflag)
        break
    except:
        print(Notext)
        count += 1
        if count >= 1:
            break

outputlistT = []
outputlistF = []
solopass = False

#ゲーム機、好きなジャンル、対象年齢、ソロプレイ派かマルチ派かで絞り込み
for i in range(len(gamelist)):
    test = 0
    l_namelist = [d.get('tname') for d in outputlistT]
    if gamelist[i]["regu"] == reguflag:
        test += 1
    if gamelist[i]["genre"] == genreflag:
        test += 1
    if soloflag == gamelist[i]["solo"]:
        test += 1
    if samplename == gamelist[i]["tname"]:
        continue
    if gamelist[i]["tname"] in l_namelist:
        continue
    if test == 3:
        a = [{"tname":gamelist[i]["tname"],
              "title":gamelist[i]["title"],
              "genre":gamelist[i]["genre"],
              "regu":gamelist[i]["regu"],
              "solo":gamelist[i]["solo"],
              "URL":gamelist[i]["URL"],
              "Ntext":gamelist[i]["Ntext"]}]
        outputlistT.extend(a)
    if test == 1:
        outputlistT.extend(random.sample(gamelist, 2))

for item in gamelist:
    if item in outputlistT:
        pass

    else:
        b = [{"tname":item["tname"],
             "title":item["title"],
              "genre":item["genre"],
              "regu":item["regu"],
              "solo":item["solo"],
              "URL":item["URL"],
              "Ntext":item["Ntext"]}]
        outputlistF.extend(b)

#ユーザーが好きそうなゲーム一覧
#print("T",outputlistT)
#ユーザーがやったことなさそうなゲーム一覧
#print("F",outputlistF)

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
videolist.extend(random.sample(outputlistF, valueF))
message = []

s = ""
if soloflag == True:
    s = "一人で"
else:
    s = "複数にんで"

l_genre = [d.get('genre') for d in videolist]


l_solo = [d.get('solo') for d in videolist]

l_ntext = [d.get('Ntext') for d in videolist]

l_tname = [d.get('tname') for d in videolist]


driver_path = "C:\\driver\\chromedriver.exe"
options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
browser = webdriver.Chrome(options=options)

#紹介の実行　デフォルトでは１０秒おきに次のゲーム画面に移動
for i in range(valueT):
    browser.get(videolist[i]["URL"])
    time.sleep(1)
    talk(l_ntext[i])
    time.sleep(1)

for i in range(valueF):
    browser.get(videolist[i+valueT]["URL"])
    talk("あなたには、新しく" + l_genre[i+valueT] + "をおすすめします。あなたの持っているハードで" + s + "するなら" + l_tname[i+valueT] + "がよいでしょう")
    time.sleep(1)