import tkinter as tk


def new_window():
    data = entry.get()
    window = tk.Tk()
    label = tk.Label(window, text=data).pack()
    window.mainloop()


if __name__ == "__main__":
    root = tk.Tk()
    entry = tk.Entry(root, width=30)
    btn = tk.Button(root, text='test', command=new_window)
    entry.pack()
    btn.pack()
    root.mainloop()
