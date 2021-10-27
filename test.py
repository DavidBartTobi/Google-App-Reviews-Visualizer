from tkinter import *

root = Tk()

button = Button(root, text="Click me!", border=0)
img = PhotoImage(file="logos/btn2.png") # make sure to add "/" not "\"
button.config(image=img)
button.pack() # Displaying the button

root.mainloop()
