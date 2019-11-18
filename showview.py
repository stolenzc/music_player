# -*- coding: utf-8 -*-
import tkinter
# from tkinter import ttk
import pygame
import os
import tkinter.filedialog
from mutagen.mp3 import MP3
# import time
music_list = []
file_path = ''
pygame.mixer.init()


def play_func(i):
    global music_list
    global file_path
    print(music_list)
    # i = event.listbox.curselection()
    path = os.path.join(file_path, music_list[i[0]])
    print(path)
    print(MP3(path).info.length)

    pygame.mixer.music.load(path)
    pygame.mixer.music.play()


def before_play(i, music_list_view):
    global music_list
    num = i[0] - 1
    if num < 0:
        num = len(music_list) - 1
    before = (num,)
    music_list_view.select_set(num)
    music_list_view.select_clear(i[0])
    play_func(before)


def next_play(i, music_list_view):
    global music_list
    num = i[0] + 1
    if num == len(music_list):
        num = 0
    after = (num,)
    music_list_view.select_set(num)
    music_list_view.select_clear(i[0])
    play_func(after)


def pause_play(play_music):
    if play_music['text'] == '播放':
        pygame.mixer.music.pause()
        play_music['text'] = '暂停'
    elif play_music['text'] == '暂停':
        pygame.mixer.music.unpause()
        play_music['text'] = '播放'


def set_vol(i):

    i = i/100
    print(i)
    print(pygame.mixer.music.get_volume())
    pygame.mixer.music.set_volume(i)


def openfile(music_list_view):
    filename = tkinter.filedialog.askopenfilename(initialdir=r'F:/song/')

    index = filename.rfind('/')
    global file_path
    global music_list
    file_path = filename[:index]
    music_list = os.listdir(file_path)
    for music_name in music_list:
        if music_name[-3:] != 'mp3':
            music_list.remove(music_name)
    for item in music_list:
        # 按顺序添加
        print(item)
        music_list_view.insert(tkinter.END, item)


class MainWindow(tkinter.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.music_list = []

        # 左边歌曲列表显示
        self.frm_left = tkinter.Frame(self.master)
        self.music_list_view = tkinter.Listbox(self.frm_left,
                                               selectmode=tkinter.BROWSE,
                                               width=30,)
        self.music_list_bar = tkinter.Scrollbar(self.frm_left)

        # 右边控制区域
        self.frm_right = tkinter.Frame(self.master)
        self.frm_right_top = tkinter.Frame(self.frm_right)
        self.frm_right_bottom = tkinter.Frame(self.frm_right,)

        # 歌曲详情显示控制
        self.progress = tkinter.Scale(self.frm_right_bottom,
                                      from_=0,
                                      to=100,
                                      orient=tkinter.HORIZONTAL,
                                      repeatdelay=1000,)
        self.vol_bar = tkinter.Scale(self.frm_right_bottom,
                                     from_=0,
                                     to=100,
                                     orient=tkinter.HORIZONTAL,
                                     repeatdelay=10000,
                                     command=lambda event: set_vol(self.vol_bar.get()))
        self.before_music = tkinter.Button(self.frm_right_bottom, text='上一曲')
        self.play_music = tkinter.Button(self.frm_right_bottom, text='播放')
        self.next_music = tkinter.Button(self.frm_right_bottom, text='下一曲')

        # 菜单栏创建
        self.menu_bar = tkinter.Menu(self.master)
        self.menu1 = tkinter.Menu(self.menu_bar, tearoff=False)
        self.menu2 = tkinter.Menu(self.menu_bar, tearoff=False)

        self.window_init()

    def window_init(self):
        self.master.title('音乐播放器')
        self.master.geometry('600x400+250+30')
        self.master.resizable(0, 0)

        # 歌曲列表框的放置及下拉条绑定
        self.music_list_view.pack(side=tkinter.LEFT,
                                  fill=tkinter.Y, )
        self.music_list_bar.pack(side=tkinter.RIGHT,
                                 fill=tkinter.Y)
        self.music_list_bar.config(command=self.music_list_view.yview)
        self.music_list_view.config(yscrollcommand=self.music_list_bar.set)
        self.frm_left.pack(side=tkinter.LEFT,
                           fill=tkinter.Y, )

        # 歌曲控制及音量控制按钮放置
        self.progress.pack(fill=tkinter.X, side=tkinter.TOP)
        self.before_music.pack(side=tkinter.LEFT)
        self.play_music.pack(side=tkinter.LEFT)
        self.next_music.pack(side=tkinter.LEFT)
        self.vol_bar.pack(fill=tkinter.X)
        self.vol_bar.set(100)

        # 右边框架放置
        self.frm_right_top.pack(side=tkinter.TOP,
                                fill=tkinter.X)
        self.frm_right_bottom.pack(side=tkinter.BOTTOM,
                                   fill=tkinter.BOTH,
                                   anchor=tkinter.SW)
        self.frm_right.pack(side=tkinter.BOTTOM,
                            fill=tkinter.X)

        # 菜单栏放置及功能设置
        self.master.config(menu=self.menu_bar)
        self.menu1.add_command(label='打开目录', command=lambda: openfile(self.music_list_view))
        self.menu_bar.add_cascade(label='打开目录', menu=self.menu1)
        self.menu2.add_command(label='退出', command=self.quit)
        self.menu_bar.add_cascade(label='退出', menu=self.menu2)
        self.music_list_view.bind('<Double-Button-1>', lambda event: play_func(self.music_list_view.curselection()))
        self.before_music.bind('<Button-1>',
                               lambda event:
                               before_play(self.music_list_view.curselection(),
                                           self.music_list_view))
        self.next_music.bind('<Button-1>',
                             lambda event:
                             next_play(self.music_list_view.curselection(),
                                       self.music_list_view))
        self.play_music.bind('<Button-1>', lambda event: pause_play(self.play_music))


if __name__ == '__main__':
    app = MainWindow()
    app.mainloop()
