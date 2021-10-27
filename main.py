from tkinter import *
from PIL import ImageTk, Image
from program import Program
import gui



root = Tk()
gui.Window_Style(root, "Google App Reviews Visualizer", "538x538")

image = Image.open('logos/logo.jpg')
image.thumbnail((538, 538))
resized_image = ImageTk.PhotoImage(image)
img_label = Label(root, image=resized_image, bg=gui.Main_Theme_Color())
img_label.grid(row=0, column=0, rowspan=9, columnspan=3)

Program(root)

root.mainloop()