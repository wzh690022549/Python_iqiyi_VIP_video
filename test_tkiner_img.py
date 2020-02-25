import io
from PIL import Image, ImageTk
import tkinter as tk
from urllib.request import urlopen


root = tk.Tk()
url = 'https://pic0.iqiyipic.com/image/20180820/68/ec/a_100168808_m_601_m4_180_236.jpg'
image_bytes = urlopen(url).read()
data_stream = io.BytesIO(image_bytes)
pil_image = Image.open(data_stream)
w, h = pil_image.size
pil_image = pil_image.resize((300, int(h / w * 300)), Image.ANTIALIAS)
fname = url.split('/')[-1]
sf = "{}({}x{})".format(fname, w, h)
root.title("test")
tk_image = ImageTk.PhotoImage(pil_image)
row = 0
column = 0
for i in range(10):
    if column > 7:
        column = 0
        row = row + 2
    label_img = tk.Label(root, image=tk_image).grid(row=row, column=column, columnspan=2)
    label_count = tk.Label(root, text=i).grid(row=row + 1, column=column)
    btn_text = tk.Button(root, text=sf).grid(row=row + 1, column=column + 1)
    column = column + 2
# label.pack(padx=5, pady=5)
root.mainloop()
