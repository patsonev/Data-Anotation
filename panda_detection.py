from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk
import pandas as pd
import os

FONT_TYPE = "Helvetica"

root = Tk()
root.resizable(0, 0)
root.title("Panda selector")
root.geometry("750x550")

def load_img():
    global img_num
    img_num = 0

    global main_dir
    main_dir = filedialog.askdirectory(title="Select directory")

    img_path_entry.delete(0, END)
    img_path_entry.insert(0, f"{main_dir}")

def show_img(img_change_num = 0):
    global img_num

    if img_change_num == 1:
        img_num += 1

    elif img_change_num == -1:
        img_num -= 1

    for widget in img_frame.winfo_children():
        widget.destroy()

    global image
    image = ImageTk.PhotoImage(Image.open(f"{main_dir}/{os.listdir(main_dir)[img_num % len(os.listdir(main_dir))]}").resize((512, 435)))

    global selected_image_canvas
    selected_image_canvas = Canvas(
        img_frame,
        width=image.width(), 
        height=image.height(),
        borderwidth=0,
        highlightthickness=0,
        bg="white",
        cursor="crosshair"
    )
    selected_image_canvas.pack()

    selected_image_canvas.img = image

    selected_image_canvas.create_image(0, 0, image=image, anchor="nw")

    top_x, top_y, bottom_x, bottom_y = 0, 0, 0, 0

    global selecton_area
    selecton_area = selected_image_canvas.create_rectangle(top_x, top_y, bottom_x, bottom_y, fill='', width=3, outline='red')

    selected_image_canvas.bind('<Button-1>', get_mouse_position)
    selected_image_canvas.bind('<B1-Motion>', update_selected_rect)

def update_selected_rect(event):
    global selecton_area
    global top_x, top_y, bottom_x, bottom_y

    bottom_x, bottom_y = event.x, event.y

    if bottom_x < 0:
        bottom_x = 0
    elif bottom_x > image.width():
        bottom_x = image.width()
        
    if bottom_y < 0:
        bottom_y = 0
    elif bottom_y > image.height():
        bottom_y = image.height()

    selected_image_canvas.coords(selecton_area, top_x, top_y, bottom_x, bottom_y)

def get_mouse_position(event):
    global top_y, top_x

    top_x, top_y = event.x, event.y

def clear_img():
    for widget in img_frame.winfo_children():
        widget.destroy()

    img_frame["width"] = 740
    img_frame["height"] = 435

def save_selection():
    data = pd.read_csv("data.csv").iloc[:, 1:]

    data.loc[len(data)] = [
        os.listdir(main_dir)[img_num], 
        int((bottom_x + top_x) / 2), 
        int((bottom_y + top_y) / 2), 
        int(bottom_x - top_x), 
        int(bottom_y - top_y)
    ]
    
    data.to_csv("data.csv")

img_path_frame = Frame(root, height=50, width=740, bg="white")
img_path_frame.pack(pady=5)

img_path_entry = Entry(
    img_path_frame, 
    width=121
)
img_path_entry.pack(padx=5, pady=10)

btns_frame = Frame(root, height=50, width=740, bg="white")
btns_frame.pack()

load_img_btn = Button(
    btns_frame,
    text="Load",
    width=21, 
    height=2, 
    font=(FONT_TYPE, 11), 
    command=lambda: [load_img(), show_img()]
)
load_img_btn.grid(row=0, column=0, padx=5, pady=5)

clear_roi_btn = Button(
    btns_frame,
    text="Clear ROI",
    width=21, 
    height=2, 
    font=(FONT_TYPE, 11),
    command=lambda: [clear_img(), show_img()]
)
clear_roi_btn.grid(row=0, column=1)

save_selection_btn = Button(
    btns_frame,
    text="Save",
    width=21, 
    height=2, 
    font=(FONT_TYPE, 11), 
    command=lambda: [save_selection(), clear_img(), show_img()]
)
save_selection_btn.grid(row=0, column=2, padx=5)

previous_btn = Button(
    btns_frame,
    text="<",
    width=5, 
    height=2, 
    font=(FONT_TYPE, 11), 
    command=lambda: show_img(-1)
)
previous_btn.grid(row=0, column=3)

next_btn = Button(
    btns_frame,
    text=">",
    width=5, 
    height=2, 
    font=(FONT_TYPE, 11), 
    command=lambda: show_img(1)
)
next_btn.grid(row=0, column=4, padx=5)

img_frame = Frame(root, height=435, width=740, bg="white")
img_frame.pack(pady=5)

root.mainloop()