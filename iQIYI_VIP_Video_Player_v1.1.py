import requests
from bs4 import BeautifulSoup
import threading
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchWindowException, WebDriverException, TimeoutException
import tkinter as tk
import tkinter.font as tf
from tkinter.messagebox import askyesno
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
    pil_image = pil_image.resize((150, int(h / w * 150)), Image.ANTIALIAS)
    tk_image = ImageTk.PhotoImage(pil_image)
    return tk_image


class VideoPage(tk.Toplevel):
    __driver_index = 0

    def __init__(self, info, tk_image):
        super().__init__()
        self.driver_list = []
        self.info = info
        self.url_list = self.info[3]
        self.title(self.info[2])
        self.iconbitmap(".\\iQIYI.ico")
        self.resizable(0, 0)
        self.row1 = tk.Frame(self, bd=10)
        self.row1.pack(fill="both")
        self.row2 = tk.Frame(self, bd=10)
        self.row2.pack(fill="both")
        tk.Label(self.row1, image=tk_image).grid(row=0, column=0, rowspan=3)
        tk.Label(self.row1, text=self.info[1], font=tf.Font(size=10)).grid(row=0, column=1, sticky="ws")
        tk.Label(self.row1, text=self.info[2], font=tf.Font(size=30)).grid(row=1, column=1, sticky="w")
        tk.Button(self.row1, text="开始播放", font=tf.Font(size=20), cursor="hand2",
                  command=lambda m=0: self.prepare_play(m, False, self.__driver_index)).grid(row=2, column=1,
                                                                                             sticky="wn", padx=10,
                                                                                             pady=10)
        tk.Label(self.row1, text="片头片尾不填则默认为0（没有片头片尾）").grid(row=0, column=2, columnspan=2, sticky="s")
        tk.Label(self.row1, text="片头多长（单位：秒）：").grid(row=1, column=2, sticky="es")
        self.e1 = tk.Entry(self.row1, width=30)
        self.e1.grid(row=1, column=3, sticky="ws")
        tk.Label(self.row1, text="片尾多长（单位：秒）：").grid(row=2, column=2, sticky="en")
        self.e2 = tk.Entry(self.row1, width=30)
        self.e2.grid(row=2, column=3, sticky="wn")
        column = 0
        row = 0
        for i in range(len(self.url_list)):
            if column > 9:
                column = 0
                row = row + 1
            n = i
            tk.Button(self.row2, text="第" + str(n + 1) + "集", cursor="hand2", font=tf.Font(size=15),
                      command=lambda m=n: self.prepare_play(m, False, self.__driver_index)).grid(row=row, column=column,
                                                                                                 padx=10, pady=10)
            column = column + 1

    def prepare_play(self, index, isnext, driver_index):
        print("播放第" + str(index + 1) + "集")
        if not isnext:
            # from selenium.webdriver.chrome.options import Options
            # options = Options()
            # options.binary_location = "Application/360chrome.exe"
            # options.add_argument('disable-infobars')
            # driver = webdriver.Chrome(executable_path="chromedriver.exe", options=options)
            driver = webdriver.Chrome()
            self.driver_list.append(driver)
            self.__driver_index = self.__driver_index + 1

        s_t = self.e1.get()
        if s_t == '':
            s_t = '0'
        t_play = threading.Thread(target=self.play, args=(self.url_list[index], s_t, driver_index))
        t_play.start()

        e_t = self.e2.get()
        if e_t == '':
            e_t = '0'
        t_end = threading.Thread(target=self.end, args=(e_t, index, driver_index))
        t_end.start()

    def play_next(self, index, driver_index):
        if index < len(self.url_list) - 1:
            print("播放下一集\n")
            self.prepare_play(index + 1, True, driver_index)
        else:
            print("已播完最后一集")
            self.driver_list[driver_index].close()

    def play(self, url, start_time, driver_index):
        play_url = "https://www.administratorw.com/video.php?url=" + url
        self.driver_list[driver_index].get(play_url)
        while True:
            iframe = self.find_tag_name("iframe", driver_index)
            if iframe == 'error':
                break
            if iframe == 'replay':
                threading.Thread(target=self.play, args=(url, start_time, driver_index)).start()
                return
            self.driver_list[driver_index].switch_to.frame(iframe)
        start = self.find_xpath("//*[@id='video']/div[4]/div[2]/button", driver_index)
        if start == 'error':
            return
        if start == 'replay':
            threading.Thread(target=self.play, args=(url, start_time, driver_index)).start()
            return
        print("开始播放")
        start.send_keys(Keys.SPACE)
        print("快进" + str(int(start_time)) + "秒")
        for i in range(int(int(start_time) / 5)):
            time.sleep(0.1)
            start.send_keys(Keys.ARROW_RIGHT)

    def end(self, end_time, index, driver_index):
        while True:
            time.sleep(1)
            total_ = self.find_xpath("//*[@id='video']/div[4]/div[2]/span/span[1]", driver_index)
            if total_ == 'error':
                return
            if total_ == 'replay':
                threading.Thread(target=self.end, args=(end_time, index, driver_index)).start()
                return
            total = total_.get_attribute("innerHTML")
            if total != "00:00":
                break
        total_time = int(time.mktime(time.strptime("2020-01-01 00:" + total, "%Y-%m-%d %H:%M:%S")))
        while True:
            time.sleep(2)
            current_ = self.find_xpath("//*[@id='video']/div[4]/div[2]/span/span[2]", driver_index)
            if current_ == 'error':
                return
            if current_ == 'replay':
                threading.Thread(target=self.end, args=(end_time, index, driver_index)).start()
                return
            current = current_.get_attribute("innerHTML")
            current_time = int(time.mktime(time.strptime("2020-01-01 00:" + current, "%Y-%m-%d %H:%M:%S")))
            if total_time - current_time <= int(end_time) + 3:
                break
        t_play_next = threading.Thread(target=self.play_next, args=(index, driver_index))
        t_play_next.start()

    def find_xpath(self, xpath, driver_index):
        try:
            res = WebDriverWait(self.driver_list[driver_index], 30, 0.5).until(
                EC.presence_of_element_located((By.XPATH, xpath)))
            return res
        except TimeoutException:
            return 'replay'
        except WebDriverException:
            return 'error'
        except NoSuchWindowException:
            return 'error'
        except:
            return 'error'

    def find_tag_name(self, tag_name, driver_index):
        try:
            res = WebDriverWait(self.driver_list[driver_index], 3, 0.5).until(
                EC.presence_of_element_located((By.TAG_NAME, tag_name)))
            return res
        except:
            return 'error'

    def closeWindow(self):
        ans = askyesno(title="提示", message="是否要关闭？")
        if ans:
            for driver in self.driver_list:
                driver.quit()
            self.destroy()
        else:
            return


class MainWindow(tk.Tk):
    image = []

    def __init__(self):
        super().__init__()
        self.title("iQIYI_VIP_Video_Player_v1.1")
        self.iconbitmap(".\\iQIYI.ico")
        self.resizable(0, 0)
        self.row1 = tk.Frame(self, bd=10)
        self.row1.pack(fill="both")
        self.row2 = tk.Frame(self)
        self.row2.pack(fill="both")
        self.e1 = tk.Entry(self.row1, width=50)
        self.e1.pack(side=tk.LEFT)
        self.b1 = tk.Button(self.row1, text='搜索', command=self.search, cursor="hand2")
        self.b1.pack(side=tk.LEFT)
        self.video_inf = []
        self.num_list = []
        for index in range(100):
            self.num_list.append(index)

    def search(self):
        self.row2.destroy()
        self.row2 = tk.Frame(self, bd=10)
        self.row2.pack(fill="both")
        threading.Thread(target=self.do_search).start()

    def do_search(self):
        global image
        image = []
        self.video_inf = self.video_search_iqiyi()
        if len(self.video_inf) == 0:
            tk.Label(self.row2, text='没有找到名为《' + self.e1.get() + '》的电影或电视剧！')
        else:
            row = 0
            column = 0
            i = 0
            for inf in self.video_inf:
                if column > 11:
                    column = 0
                    row = row + 2
                image.append(get_image(inf[0]))
                l1 = tk.Label(self.row2)
                l1.config(image=image[i])
                l1.grid(row=row, column=column, columnspan=3)
                tk.Label(self.row2, text=inf[1]).grid(row=row + 1, column=column)
                n = self.num_list[i]
                tk.Button(self.row2, text=inf[2], command=lambda m=n: self.open_video_page(m), cursor="hand2").grid(
                    row=row + 1, column=column + 1, columnspan=2, sticky="w")
                column = column + 3
                i = i + 1

    def open_video_page(self, column):
        global image
        self.withdraw()
        video_page = VideoPage(self.video_inf[column], image[column])
        video_page.protocol('WM_DELETE_WINDOW', lambda: self.close_video_page(video_page))
        video_page.mainloop()

    def close_video_page(self, video_page):
        video_page.closeWindow()
        self.update()
        self.deiconify()

    def video_search_iqiyi(self):
        r = requests.get("https://so.iqiyi.com/so/q_" + self.e1.get())
        r.encoding = r.apparent_encoding
        # print(r.text)
        soup = BeautifulSoup(r.text, 'html.parser')
        target = soup.find_all("div", class_="qy-search-result-item vertical-pic")
        video_inf = []
        try:
            for div in target:
                video_site = div.find('em', class_='player-name')
                if '爱奇艺' in video_site:
                    video_img = div.find('img').attrs['src']
                    video_type = div.find('span', class_='item-type').get_text()
                    video_name = div.find('a', class_='main-tit').attrs['title']
                    video_list = []
                    ul_list = div.find_all('ul', style="display:none;")
                    for ul in ul_list:
                        li_list = ul.find_all('li')
                        for li in li_list:
                            video_list.append('https:' + li.a.attrs['href'])
                    if len(video_list) == 0:
                        video_list.append('https:' + div.find('a', class_='qy-search-result-btn').attrs['href'])
                    video_inf.append([video_img, video_type, video_name, video_list])
        except Exception as error:
            print(error)
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

    def closeWindow(self):
        ans = askyesno(title="提示", message="是否要关闭？")
        if ans:
            self.destroy()
        else:
            return


if __name__ == "__main__":
    main_window = MainWindow()
    main_window.protocol('WM_DELETE_WINDOW', main_window.closeWindow)
    main_window.mainloop()
