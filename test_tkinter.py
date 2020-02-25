import tkinter as tk

window = tk.Tk()
window.title('Hello World!')
window.geometry('500x300')
var = tk.StringVar()
l = tk.Label(window, textvariable=var, bg='green', font=('Arial', 12), width=30, height=2)
l.pack()


def hit_me():
    var.set(e.get())


b = tk.Button(window, text='hit me', font=('Arial', 12), width=10, height=1, command=hit_me)
b.pack()
e = tk.Entry(window, show='*')
e.pack()
window.mainloop()
