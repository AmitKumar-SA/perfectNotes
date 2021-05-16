#
# A Sample Notes App
#
# Copyright (c) 2020 by Amit Kumar
#
# meet.amit.kumar@gmail.com
#
from tkinter import *
from tkinter import messagebox
from tkinter import simpledialog
import os

# Root Config
root = Tk()
root.title("Perfect Notes")
root.iconbitmap("images/logo.ico")
root.state('zoomed')

# Global variables
flags = os.O_RDWR | os.O_CREAT
mode = 0o666
directory = "/notes"
buttons = {}
text = StringVar()
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()


def move_to_frame3(event):
    print("Method called")
    text.set(event.widget['text'])
    fd = os.open(directory+"/"+text.get(), flags, mode)
    print("File opened Successfully")
    my_text.delete('1.0', END)
    content = os.read(fd, os.path.getsize(fd))
    my_text.insert(END,content)
    os.close(fd)
    frame1.pack_forget()
    frame2.pack(expand=True)
    frame3.pack(expand=True)
    frame4.pack(expand=True)


def move_to_frame1():
    print("Method2 called")
    frame2.pack_forget()
    frame3.pack_forget()
    frame4.pack_forget()
    frame1.pack()


def save_content(event):
    print("Creating New File")
    content = my_text.get("1.0", END)
    with open(directory+"/"+text.get(), 'w') as handle:
        status_bar['text'] = "Saving.........."
        handle.write(content)
        status_bar['text'] = "Saved..........."


def popup(event):
    try:
        text.set(event.widget['text'])
        m.tk_popup(event.x_root, event.y_root)
    finally:
        m.grab_release()


def create():
    print("create called")
    if buttons.__len__() >= 20:
        messagebox.showinfo("Perfect notes", "You can't have more than 20 notes. Please delete unused notes to continue.")
        return
    new_filename = simpledialog.askstring('Create File', 'File Name: ')
    if new_filename:
        text.set(new_filename)
        try:
            with open(directory+"/"+new_filename, 'w') as fp:
                pass
            buttonNum = buttons.__len__()
            button = Button(frame1, bg="black", fg="white", text=new_filename, font=("Comfortaa", 15), width=30)
            buttons[button] = buttonNum
            buttonNum += 1
            button.bind("<Button-1>", move_to_frame3)
            button.bind("<Button-3>", popup)
            button.pack()
        except:
            messagebox.showerror('Perfect Notes', 'Invalid Filename. Please try again.')


def rename():
    print("rename called for" + text.get())
    new_filename = simpledialog.askstring('Rename File', 'File Name: ')
    if new_filename:
        try:
            if text.get() != new_filename:
                os.rename(directory+"/"+text.get(), directory+"/"+new_filename)
                for but in buttons:
                    if but['text'] == text.get():
                        but['text'] = new_filename
        except:
            messagebox.showerror('Perfect Notes', 'Invalid Filename. Please try again.')


def delete():
    print("delete called for" + text.get())
    resp = messagebox.askyesno('Delete File', 'Are you sure you want to delete ' + text.get() + ' ?', icon='warning')
    if resp:
        os.remove(directory+"/"+text.get())
        for but in list(buttons):
            if but['text'] == text.get():
                but.destroy()
                buttons.pop(but)


# Frames - Home and Notepad
frame1 = Frame(root)
frame2 = Frame(root, width=screen_width, height=screen_height*10/100)
frame3 = Frame(root, width=screen_width, height=screen_height - (screen_height*22/100))
frame4 = Frame(root, width=screen_width, height=screen_height*10/100)

files = os.listdir(directory)
buttonNum = 0

# Frame1
add_btn_img = PhotoImage(file='images/plus.png')
img_label = Label(image=add_btn_img)
add_button = Button(frame1, image=add_btn_img, borderwidth=0, command=create)
add_button.pack(side=TOP, anchor="e")

my_label = Label(frame1, text='Notebooks', font=("Arial", 44), fg="maroon2")
my_label.pack()
m = Menu(frame3, tearoff=0)
m.add_command(label="Rename", command=rename)
m.add_command(label="Delete", command=delete)

for f in files:
    button = Button(frame1, bg="black", fg="white", text=f, font=("Comfortaa", 15), width=30)
    buttons[button] = buttonNum
    buttonNum += 1
    button.bind("<Button-1>", move_to_frame3)
    button.bind("<Button-3>", popup)
    button.pack()

frame1.pack()

# Frame2
frame2.pack_propagate(False)

back_btn_img = PhotoImage(file='images/back.png')
back_label = Label(image=back_btn_img)
back_button = Button(frame2, image=back_btn_img, borderwidth=0, command=move_to_frame1)
back_button.pack(side=LEFT)

filename_label = Label(frame2, textvariable=text, font=("Arial", 44), fg="maroon2")
filename_label.pack()

# Frame3
frame3.pack_propagate(False)

text_scroll = Scrollbar(frame3)
text_scroll.pack(side=RIGHT, fill=Y)

my_text = Text(frame3, yscrollcommand=text_scroll.set)
my_text.bind("<KeyRelease>", save_content)
my_text.pack(side=LEFT, fill=BOTH, expand=True)

text_scroll.config(command=my_text.yview)

# frame4
frame4.pack_propagate(False)

status_bar = Label(frame4, text='Ready..........', bd=2, relief=SUNKEN, anchor=W, fg="blue", font=("Arial", 16))
status_bar.pack(fill=X, side=BOTTOM)

root.mainloop()