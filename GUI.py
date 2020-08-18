import tkinter as tk
from PIL import ImageTk, Image
import sys
import os

window = tk.Tk()
window.title("Confessions Bot")
window.geometry("600x300")
window.grid_columnconfigure((0,2), weight = 1)

# Labels
label_tell_account = tk.Label(window, text = "Tellonym Account")
label_tell_password = tk.Label(window, text = "Tellonym Password")
label_ig_account = tk.Label(window, text = "Instagram Account")
label_ig_password = tk.Label(window, text = "Instagram Password")

# Run Button Function
def execute_script():
    os.system('python bot.py')


# Interactive Elements
tell_account = tk.Entry(window)
tell_password = tk.Entry(window)
ig_account = tk.Entry(window)
ig_password = tk.Entry(window)
run = tk.Button(text = "Run!")

#Format Grid
image = ImageTk.PhotoImage(Image.open("logo.png"))
tk.Label(window, image = image).grid(row = 0, column = 1, padx = 10, pady = 10)
label_tell_account.grid(row = 1, column = 0)
tell_account.grid(row = 1, column = 2, padx = 10, pady = 10)
label_tell_password.grid(row = 2, column = 0, padx = 10, pady = 10)
tell_password.grid(row = 2, column = 2, padx = 10, pady = 10)
label_ig_account.grid(row = 3, column = 0, padx = 10, pady = 10)
ig_account.grid(row = 3, column = 2, padx = 10, pady = 10)
label_ig_password.grid(row = 4, column = 0, padx = 10, pady = 10)
ig_password.grid(row = 4, column = 2, padx = 10, pady = 10)
run.grid(row = 5, column = 1, padx = 10, pady = 10)

window.mainloop()
