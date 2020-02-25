from selenium import webdriver
from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.common.action_chains import ActionChains
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import tkinter as tk
import threading


def find_xpath(xpath):
    try:
        res = WebDriverWait(driver, 30, 0.5).until(EC.presence_of_element_located((By.XPATH, xpath)))
        return res
    except:
        return find_xpath(xpath)


def find_tag_name(tag_name):
    try:
        res = WebDriverWait(driver, 30, 0.5).until(EC.presence_of_element_located((By.TAG_NAME, tag_name)))
        return res
    except:
        return find_tag_name(tag_name)


driver = webdriver.Chrome()

root = tk.Tk()
root.title('My test')
root.geometry('500x300')

# name = input("搜索：")
# url = "https://so.iqiyi.com/so/q_" + name
play_url = "https://www.administratorw.com/video.php?url=http://www.iqiyi.com/v_19rur9poxc.html"
# play(url)

label_s_t = tk.Label(root, text="start time")
label_s_t.pack()
entry_s_t = tk.Entry(root, width=30)
entry_s_t.pack()
label_e_t = tk.Label(root, text="end time")
label_e_t.pack()
entry_e_t = tk.Entry(root, width=30)
entry_e_t.pack()


def prepare_play(url):
    s_t = entry_s_t.get()
    t_play = threading.Thread(target=play, args=(url, s_t))
    t_play.start()

    e_t = entry_e_t.get()
    t_end = threading.Thread(target=end, args=(e_t,))
    t_end.start()


def play_next():
    print("播放下一集")
    return True


def play(url, start_time):
    driver.get(url)
    iframe = find_tag_name("iframe")
    driver.switch_to.frame(iframe)
    iframe = find_tag_name("iframe")
    driver.switch_to.frame(iframe)
    iframe = find_tag_name("iframe")
    driver.switch_to.frame(iframe)
    start = find_xpath("//*[@id='a1']/div[4]/div[2]/button[1]")
    print("发送空格")
    start.send_keys(Keys.SPACE)
    print("快进" + str(int(start_time)) + "秒")
    for i in range(int(int(start_time) / 5)):
        time.sleep(0.1)
        start.send_keys(Keys.ARROW_RIGHT)


def end(end_time):
    while True:
        time.sleep(1)
        total = find_xpath("//*[@id='a1']/div[4]/div[2]/span/span[1]").get_attribute("innerHTML")
        if total != "00:00":
            break
    total_time = int(time.mktime(time.strptime("2020-01-01 00:" + total, "%Y-%m-%d %H:%M:%S")))
    while True:
        time.sleep(5)
        current = find_xpath("//*[@id='a1']/div[4]/div[2]/span/span[2]").get_attribute("innerHTML")
        current_time = int(time.mktime(time.strptime("2020-01-01 00:" + current, "%Y-%m-%d %H:%M:%S")))
        if total_time - current_time <= int(end_time):
            break
    t_play_next = threading.Thread(target=play_next, args=())
    t_play_next.start()


btn_play = tk.Button(root, text="play",
                     command=lambda url=play_url: prepare_play(url))
btn_play.pack()
root.mainloop()
