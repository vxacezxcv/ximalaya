#!/usr/bin/env python

# pylint: disable=invalid-name
# pylint: disable=bare-except
# pylint: disable=missing-function-docstring

import hashlib
import json
import os
import random
import threading
import time
import tkinter as tk
import tkinter.filedialog
import tkinter.messagebox
from tkinter import ttk
from urllib import parse

import requests

columns1 = ("TITLE", "ID")
headers = {
    "user-agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/72.0.3626.96 Safari/537.36"
    )
}


def xm_md5():
    url = "https://www.ximalaya.com/revision/time"
    header = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/72.0.3626.96 Safari/537.36"
        ),
        "Host": "www.ximalaya.com",
        "Accept-Encoding": "gzip, deflate, br",
    }
    try:
        html = requests.get(url, headers=header)
        nowTime = str(round(time.time() * 1000))

        part_a = str(hashlib.md5(f"himalaya-{html.text}".encode()).hexdigest())
        part_b = "({})".format(str(round(random.random() * 100)))
        part_c = html.text
        part_d = "({})".format(str(round(random.random() * 100)))
        part_e = nowTime
        sign = f"{part_a}{part_b}{part_c}{part_d}{part_e}"
    except Exception:
        tkinter.messagebox.showerror("错误", "请检查网络是否畅通")
    return sign


def open_link():
    Listbox1.delete(0, tk.END)
    Listbox2.delete(0, tk.END)
    link = Entry2.get()
    try:
        albumId = link.split("/")[4]
    except Exception:
        tkinter.messagebox.showerror("错误", "请输入正确的链接")
    url = (
        f"http://mobwsa.ximalaya.com/mobile/playlist/album/page?"
        f"albumId={albumId}&pageId=1"
    )
    try:
        html = requests.get(url)
        all = json.loads(html.text)
        maxPageId = all["maxPageId"]
        list1 = range(1, maxPageId + 1)
        for n in list1:
            url = (
                f"http://mobwsa.ximalaya.com/mobile/playlist/album/page?"
                f"albumId={albumId}&pageId={n}"
            )
            html = requests.get(url)
            all = json.loads(html.text)
            data = all["list"]
            for a in data:
                title = a["title"]
                playUrl64 = a["playUrl64"]
                Listbox1.insert(tk.END, title)
                Listbox2.insert(tk.END, playUrl64)
    except Exception:
        tkinter.messagebox.showerror("错误", "请检查网络是否畅通")
    Text1.insert(tk.END, "> 解析线程结束\n")
    Text1.see(tk.END)


def download():
    global path
    chosen_indices = Listbox1.curselection()
    Text1.insert(tk.END, "> " + str(len(chosen_indices)) + "个任务正在下载\n")
    Text1.see(tk.END)
    total = len(chosen_indices)
    for cur, chosen_idx in enumerate(chosen_indices):
        fname = Listbox1.get(chosen_idx)
        url = Listbox2.get(chosen_idx)
        os.system(f"mkdir -p {path}")
        fprefix = str(cur + 1).zfill(len(str(total)))
        fpath = f"{path}/{fprefix}-{fname}.mp3"
        file1 = requests.get(url, headers=headers)
        with open(fpath, "wb") as code:
            code.write(file1.content)
        Text1.insert(tk.END, f"> [{cur+1}/{total}] {fpath} 下载成功\n")
        Text1.see(tk.END)
    Text1.insert(tk.END, "> 全部下载完成.\n")
    Text1.see(tk.END)


def solve():
    Text1.insert(tk.END, "> 解析线程开始\n")
    Text1.see(tk.END)
    Listbox1.delete(0, tk.END)
    Listbox2.delete(0, tk.END)
    for item in treeview1.selection():
        item_text = treeview1.item(item, "values")
        albumId = item_text[1]
    url = (
        f"http://mobwsa.ximalaya.com/mobile/playlist/album/page?"
        f"albumId={albumId}&pageId=1"
    )
    try:
        html = requests.get(url)
        all = json.loads(html.text)
        maxPageId = all["maxPageId"]
        list1 = range(1, maxPageId + 1)
        for n in list1:
            url = (
                f"http://mobwsa.ximalaya.com/mobile/playlist/album/page?"
                f"albumId={albumId}&pageId={n}"
            )
            html = requests.get(url)
            all = json.loads(html.text)
            data = all["list"]
            for a in data:
                title = a["title"]
                playUrl64 = a["playUrl64"]
                Listbox1.insert(tk.END, title)
                Listbox2.insert(tk.END, playUrl64)
    except Exception:
        tkinter.messagebox.showerror("错误", "请检查网络是否畅通")
    Text1.insert(tk.END, "> 解析线程结束\n")
    Text1.see(tk.END)


def clear_list(tree):
    x = tree.get_children()
    for item in x:
        tree.delete(item)


def search():
    """按照关键词进行搜索"""

    Text1.insert(tk.END, "> 搜索线程开始\n")
    Text1.see(tk.END)
    clear_list(treeview1)
    name = parse.quote(Entry1.get())
    url = (
        f"https://www.ximalaya.com/revision/search?"
        f"core=album&kw={name}&spellchecker=true&rows=20&"
        f"condition=relation&device=iPhone"
    )
    head = {
        "user-agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/72.0.3626.96 Safari/537.36"
        ),
        "xm-sign": xm_md5(),
    }
    try:
        html = requests.get(url, headers=head)
        all = json.loads(html.text)
        total_pages = all["data"]["result"]["response"]["totalPage"]
        pages_list = range(1, total_pages + 1)
        for n in pages_list:
            url = (
                f"https://www.ximalaya.com/revision/search?"
                f"core=album&kw={name}&page={n}&spellchecker=true&rows=20&"
                f"condition=relation&device=iPhone"
            )
            html = requests.get(url, headers=head)
            all = json.loads(html.text)
            data = all["data"]["result"]["response"]["docs"]
            for x in data:
                title = x["title"]
                id = x["id"]
                treeview1.insert("", "end", values=(title, id))
    except Exception:
        tkinter.messagebox.showerror("错误", "请检查网络是否畅通")
    Text1.insert(tk.END, "> 搜索线程结束\n")
    Text1.see(tk.END)


def set_dir():
    global path
    path = tkinter.filedialog.askdirectory()
    Entry3.delete(0, tk.END)
    Entry3.insert(tk.END, path)


def pass_download():
    threading.Thread(target=download).start()


def open_link_button_click():
    threading.Thread(target=open_link).start()


def treeview1_click(event):
    threading.Thread(target=solve).start()


def search_button_click():
    threading.Thread(target=search).start()


def set_dir_click():
    threading.Thread(target=set_dir).start()


# GUI
windows = tk.Tk()
windows.geometry("917x564")  # +34+306
windows.title("喜马拉雅专辑下载4.2 BY:Snow")
windows.resizable(0, 0)
Label1 = tk.Label(windows)
Label1.place(height=22, width=904, x=5, y=420)
Entry1 = tk.Entry(windows)
Entry1.place(height=34, width=531, x=4, y=5)
Entry2 = tk.Entry(windows)
Entry2.place(height=34, width=531, x=4, y=42)
Entry3 = tk.Entry(windows)
Entry3.place(height=34, width=531, x=4, y=80)
path = os.path.expanduser("~/Downloads/ximalaya")
Entry3.insert(tk.END, path)
Button1 = tk.Button(windows, text="搜索", command=search_button_click)
Button1.place(height=34, width=123, x=539, y=5)
Button2 = tk.Button(windows, text="下载选中", command=pass_download)
Button2.place(height=109, width=246, x=664, y=5)
Button3 = tk.Button(windows, text="打开链接", command=open_link_button_click)
Button3.place(height=34, width=123, x=539, y=43)
Button4 = tk.Button(windows, text="选择目录", command=set_dir_click)
Button4.place(height=34, width=123, x=539, y=80)
Text1 = tk.Text(windows)
Text1.place(height=88, width=904, x=5, y=469)
Text1.insert(tk.END, "> 启动成功！\n")
Text1.see(tk.END)

# 列表1
treeview1 = ttk.Treeview(windows, height=10, show="headings", columns=columns1)
treeview1.place(height=299, width=530, x=5, y=116)
treeview1.column("TITLE", width=330, anchor="center")  # 表示列, 不显示
treeview1.column("ID", width=200, anchor="center")
treeview1.heading("TITLE", text="TITLE")  # 显示表头
treeview1.heading("ID", text="ID")
treeview1.bind("<Double-1>", treeview1_click)
Scrollbar1 = tk.Scrollbar(treeview1)
Scrollbar1.pack(side=tk.RIGHT, fill=tk.Y)

# 列表2
Listbox1 = tk.Listbox(windows, selectmode=tk.EXTENDED)
Listbox1.place(height=299, width=370, x=539, y=116)
Scrollbar2 = tk.Scrollbar(Listbox1)
Scrollbar2.pack(side=tk.RIGHT, fill=tk.Y)
Listbox2 = tk.Listbox(windows)
Listbox2.place(height=0, width=0, x=0, y=0)
treeview1.config(yscrollcommand=Scrollbar1.set)
Listbox1.config(yscrollcommand=Scrollbar2.set)
Scrollbar1.config(command=treeview1.yview)
Scrollbar2.config(command=Listbox1.yview)


if __name__ == "__main__":
    windows.mainloop()
