import requests
from bs4 import BeautifulSoup
import threading
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import tkinter as tk
import io
from PIL import Image, ImageTk
from urllib.request import urlopen


def get_image(url):
    if url.split("//")[0] != "http:":
        url = "http:" + url
    image_bytes = urlopen(url).read()
    data_stream = io.BytesIO(image_bytes)
    pil_image = Image.open(data_stream)
    w, h = pil_image.size
    pil_image = pil_image.resize((300, int(h / w * 300)), Image.ANTIALIAS)
    tk_image = ImageTk.PhotoImage(pil_image)
    return tk_image


class MainWindow(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title("iQIYI_VIP_Video_Player_1.0")
        self.row1 = tk.Frame(self, bd=10)
        self.row1.pack(fill="both")
        self.row2 = tk.Frame(self)
        self.row2.pack(fill="both")
        self.e1 = tk.Entry(self.row1, width=50)
        self.e1.pack(side=tk.LEFT)
        self.b1 = tk.Button(self.row1, text='搜索', command=self.search)
        self.b1.pack(side=tk.LEFT)

    def search(self):
        self.row2.destroy()
        self.row2 = tk.Frame(self, bd=10)
        self.row2.pack(fill="both")
        threading.Thread(target=self.do_search).start()

    def do_search(self):
        global image
        image = []
        video_inf = self.video_search_iqiyi()
        if len(video_inf) == 0:
            tk.Label(self.row2, text='没有找到名为《' + self.e1.get() + '》的电影或电视剧！')
        else:
            row = 0
            column = 0
            i = 0
            for inf in video_inf:
                if column > 11:
                    column = 0
                    row = row + 2
                image.append(get_image(inf[0]))
                l1 = tk.Label(self.row2)
                l1.config(image=image[i])
                l1.grid(row=row, column=column, columnspan=3)
                tk.Label(self.row2, text=inf[1]).grid(row=row + 1, column=column)
                tk.Button(self.row2, text=inf[2]).grid(row=row + 1, column=column + 1, columnspan=2, sticky="w")
                column = column + 3
                i = i + 1

    def video_search_iqiyi(self):
        r = requests.get("https://so.iqiyi.com/so/q_" + self.e1.get())
        r.encoding = r.apparent_encoding
        # print(r.text)
        soup = BeautifulSoup(r.text, 'html.parser')
        target = soup.find_all("div", class_="qy-search-result-item vertical-pic")
        video_inf = []
        try:
            for div in target:
                video_site = div.contents[3].find('div', class_='result-bottom').div.div.span.em.get_text()
                if '爱奇艺' in video_site:
                    video_img = div.div.div.div.a.img.attrs['src']
                    video_type = div.contents[3].h3.span.get_text()
                    video_name = div.contents[3].h3.a.attrs['title']
                    video_list = []
                    ul_list = div.contents[3].find_all('ul', style="display:none;")
                    for ul in ul_list:
                        li_list = ul.find_all('li')
                        for li in li_list:
                            video_list.append(li.a.attrs['href'])
                    video_inf.append([video_img, video_type, video_name, video_list])
                else:
                    continue
        except:
            print("查找完毕")
        print("结果如下：")
        for inf in video_inf:
            print(inf[0])
            print(inf[1])
            print(inf[2])
            i = 1
            for temp in inf[3]:
                print("第" + str(i) + "集:" + temp)
                i = i + 1
            print()
        return video_inf


if __name__ == "__main__":
    main_window = MainWindow()
    main_window.mainloop()
