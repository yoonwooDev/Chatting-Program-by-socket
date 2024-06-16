import tkinter
import ttkbootstrap
from ttkbootstrap.constants import *
import socket
from threading import Thread

def send(event=None):
    msg = input_msg.get()
    sock.send(bytes(msg, 'utf-8'))
    input_msg.set("")
    if msg == "/bye":
        sock.close()
        win.quit()

def recvMsg():
    while True:
        msg = sock.recv(1024).decode("utf-8")
        len_of_msg = len(msg) - (msg.find("]") + 1)
        msg1 = ""
        msg2 = ""
        if len_of_msg > 29:
            for i in range(0,28):
                msg1 += msg[i]
            for j in range(28, len_of_msg+1):
                msg2 += msg[j]
            chat_list.insert(tkinter.END, msg1)
            chat_list.insert(tkinter.END, msg2)
        else:
            chat_list.insert(tkinter.END, msg)

def on_delete(event=None):
    input_msg.set("/bye")
    send()

win = ttkbootstrap.Window(themename='morph')
win.title("채팅 앱")

frame = tkinter.Frame(win)
input_msg = tkinter.StringVar()

scroll = ttkbootstrap.Scrollbar(frame)
scroll.pack(side=tkinter.RIGHT, fill=tkinter.Y)
chat_list = tkinter.Listbox(frame, height=15, width=50, yscrollcommand=scroll.set)
chat_list.insert(tkinter.END, "* 종료시 /bye를 입력해주세요 *")
chat_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
frame.pack()

inputbox = tkinter.Entry(win, textvariable=input_msg)
inputbox.bind("<Return>", send)
inputbox.pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=tkinter.YES, padx=5, pady=5)

sendbutton = ttkbootstrap.Button(win, text='전송', command=send, bootstyle=SUCCESS)
sendbutton.pack(side=tkinter.RIGHT, fill=tkinter.X, padx=5, pady=5)
win.protocol("WM_DELETE_WINDOW", on_delete)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(("IP", 8080))
    
receive_thread = Thread(target=recvMsg)
receive_thread.daemon = True
receive_thread.start()

win.mainloop()