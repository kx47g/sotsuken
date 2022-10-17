import win32com.client
import time

sapi = win32com.client.Dispatch("SAPI.SpVoice")
dog = win32com.client.Dispatch("SAPI.SpObjectTokenCategory")
dog.SetID(r"HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech_OneCore\Voices", False)

v = [t for t in dog.EnumerateTokens() if t.GetAttribute("Name") == "Microsoft sayaka"]
if v:
    oldv = sapi.Voice
    sapi.Voice = v[0]
    sapi.Speak("わかりました。価格の安い順に並べ替えます")
    sapi.Voice = oldv

for token in dog.EnumerateTokens():
    print(token.GetDescription())
"""

sapi = win32com.client.Dispatch("SAPI.SpVoice")
cat  = win32com.client.Dispatch("SAPI.SpObjectTokenCategory")
cat.SetID(r"HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech_OneCore\Voices", False)
v = [t for t in cat.EnumerateTokens() if t.GetAttribute("Name") == "Microsoft sayaka"]
if v:
    fs = win32com.client.Dispatch("SAPI.SpFileStream")
    fs.Open("sayaka.wav", 3)
    sapi.AudioOutputStream = fs
    oldv = sapi.Voice
    sapi.Voice = v[0]
    sapi.Speak("検索キーワードを喋ってください")
    sapi.Voice = oldv
    fs.Close()
"""