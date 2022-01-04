from tkinter import *
from hand_gesture import *

mode = False


def login():
    global password
    var = password.get()
    if var == "000000":
        if mode:
            hg = Hand_Gesture(True, True)
        else:
            hg = Hand_Gesture(False, True)
        hg.run_app()


def change_mode():
    global mode
    if mode:
        mode = False
    else:
        mode = True
    print("模式切换成功")
    print("当前模式为" + str(mode))
    return mode


def run():
    global password
    root = Tk()
    root.title('控制器')
    root.geometry('300x300')
    label1 = Label(root, text='控制器',
                   bg='#d3fbfb',
                   fg='red',
                   font=('华文新魏', 32),
                   width=20,
                   height=2,
                   relief=SUNKEN)
    label1.pack()
    password = Entry(root, width=20, textvariable=StringVar())
    password.pack()
    button1 = Button(root, text='登录', command=login)
    button1.place(relx=0.2, rely=0.5)
    button2 = Button(root, text='退出', command=exit)
    button2.place(relx=0.6, rely=0.5)
    button3 = Button(root, text='模式', command=change_mode)
    button3.place(relx=0.4, rely=0.5)
    root.mainloop()
