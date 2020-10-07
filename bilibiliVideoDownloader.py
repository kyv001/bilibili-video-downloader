import requests
import tkinter as tk
from tkinter import ttk
from threading import Thread

def start():
    button_start['text'] = '正在下载……'
    button_start['command'] = lambda :...
    av = int(entry_av.get())
    progress_download.start()
    headers = {
        'host': 'api.bilibili.com',
        'User-Agent':\
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'
    }
    json = \
         requests.get(
             "https://api.bilibili.com/x/player/pagelist?aid={av}&jsonp=jsonp".format(av=av),
             headers=headers
         ).json()

    cid = json['data'][0]['cid']


    json = \
         requests.get(
             "https://api.bilibili.com/x/player/playurl?avid={av}&cid={cid}&qn=32&type=&otype=json".format(
                 av=av,
                 cid=cid),
             headers=headers
         ).json()

    flv_url = json['data']['durl'][0]['url']
    headers = {
        "host": flv_url.split('/')[2],
        "Referer": 'https://www.bilibili.com',
        "User-Agent": "Mozilla/5.0(Windows NT 10.0;WOW64) AppleWebKit/537.36(KHTML,likeGecko)Chrome/63.0.3239.132Safari/537.36"
    }

    flv = requests.get(flv_url, headers=headers, stream=True).content

    with open("video_AV{av}.flv".format(av=av), 'wb') as video:
        video.write(flv)
    
    progress_download.stop()
    button_start['text'] = '开始下载'
    button_start['command'] = Thread(target=start).start

root = tk.Tk("哔哩哔哩视频下载器")

label_av = tk.Label(text="AV号：（不带前缀）")
entry_av = tk.Entry()
button_start = tk.Button(command=Thread(target=start).start, text='开始下载')
progress_download = ttk.Progressbar(mode='indeterminate', length=500)
progress_download.step(10)

label_av.pack()
entry_av.pack()
progress_download.pack()
button_start.pack()

tk.mainloop()
