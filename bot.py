from instabot import Bot
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime
import re
import os
from os import path
from PIL import Image, ImageTk, ImageDraw
import shutil
import tkinter as tk
from tkinter import messagebox
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options

# GUI
window = tk.Tk()
window.title("Confessions Bot")
window.geometry("600x350")
window.grid_columnconfigure((0,2), weight = 1)

label_tell_account = tk.Label(window, text = "Tellonym Account")
label_tell_password = tk.Label(window, text = "Tellonym Password")
label_ig_account = tk.Label(window, text = "Instagram Account")
label_ig_password = tk.Label(window, text = "Instagram Password")

tell_account = tk.Entry(window)
tell_password = tk.Entry(window)
ig_account = tk.Entry(window)
ig_password = tk.Entry(window)

# Main Function
def bot(tell_account_input, tell_password_input, ig_account_input, ig_password_input):
    # Script Setup
    folders = ["to_post/", "not_posted/", "posted"]
    for folder in folders:
        if not path.exists(folder):
            os.mkdir(folder)

    # Getting Tells to Post
    chrome_options = Options()
    mobile_emulation = { "deviceName": "iPhone X" }
    chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)

    driver = webdriver.Chrome(ChromeDriverManager().install(), options = chrome_options)
    driver.get("https://tellonym.me/login?redirect=/tells")

    username = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.NAME, "email")))
    username.clear()
    username.send_keys(tell_account_input)

    password = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.NAME, "password")))
    password.clear()
    password.send_keys(tell_password_input)

    driver.find_element_by_tag_name("button").click()

    try:
        for element in WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "rmq-f5f56a03"))):
             unclean_name = re.findall("element\s*=\s*([\S\s]+)", str(element))
             name = re.sub('[^\w]', '', str(unclean_name))
             element.screenshot("to_post/" + datetime.now().strftime("%Y_%m_%d-%I_%M_%S_%p") + str(name) + ".png")

        for i in range(len(driver.find_elements_by_class_name("rmq-f5f56a03"))):
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "rmq-f5f56a03"))).click()
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "answer"))).send_keys("posted")
            driver.find_element_by_tag_name("button").click()

        WebDriverWait(driver, 10)
        driver.quit()

        # Pic Formating
        for pics in os.listdir("to_post/"):
            # if not pics.startswith("NOT_POSTED"):
            image = Image.open("to_post/" + pics, 'r')
            image = image.convert('RGB')
            box = (1, 1, image.width - 45, image.height - 35)
            image = image.crop(box)
            zoom = (image.width*2, image.height*2)
            image = image.resize(zoom)
            v_line = ImageDraw.Draw(image)
            v_line.line([1, 30, 1, image.width], fill = "grey", width = 10)
            template = Image.open("template.jpg")
            template.paste(image, (70,350))
            template.save(re.sub(".png", ".jpg", str("to_post/" + pics)))

        for item in os.listdir("to_post/"):
             if item.endswith(".png"):
                 os.remove(os.path.join("to_post/", item))

        # Picture Popup Check
        top = tk.Toplevel(window)
        top.focus_force()
        top.lift()
        top.geometry("600x550")
        top.grid_columnconfigure((0, 4), weight = 1)

        current = 0
        image_list = [os.path.join("to_post/", files) for files in os.listdir("to_post/")]
        caption_text = tk.Entry(top)
        caption_text.grid(row = 3, column = 1)

        def move(delta):
            nonlocal current, image_list, top
            if not (0 <= current - delta < len(image_list)):
                messagebox.showinfo('End', 'No more images to post.')
                top.destroy()
                return
            current -= delta
            image = Image.open(image_list[current])
            photo = ImageTk.PhotoImage(image.resize((400, 400)))
            label['image'] = photo
            label.photo = photo

        # Posting Tells to Instagram
        def instagram():
            nonlocal ig_account_input, ig_password_input, current, image_list, caption_text
            if not caption_text.get():
                messagebox.showinfo('End', 'Caption Missing')
            else:
                try:
                    bot = Bot()
                    bot.login(username = ig_account_input, password = ig_password_input)
                    bot.upload_photo(image_list[current], caption = caption_text.get())
                    os.rename(image_list[current] + ".REMOVE_ME", re.sub("to_post/", "posted/", image_list[current]))
                    move(-1)
                except:
                    messagebox.showerror('Next',
                        "Couldn't connect to Instagram. Logg-in details may be wrong. Edited pictures moved to 'Not Posted'. Try again")
                    # os.rename(image_list[current], re.sub("to_post/", "not_posted/", image_list[current]))
                    for pics in os.listdir("to_post/"):
                        os.rename("to_post/" + pics, "not_posted/" + pics)
                    window.destroy()

        def dont_post():
            os.rename(image_list[current], re.sub("to_post/", "not_posted/", image_list[current]))
            move(-1)

        label = tk.Label(top)
        label.grid(row = 0, column = 1, padx = 10, pady = 10)

        tk.Button(top, text = "Don't Post", command = dont_post).grid(row = 1, column = 0, columnspan = 1)
        tk.Button(top, text = "Post to Instagram", command = instagram).grid(row = 1, column = 3, columnspan = 4)
        tk.Label(top, text = "Caption:").grid(row = 2, column = 1)

        move(0)

    except TimeoutException as ex:
        driver.quit()
        tk.Label(window, text = "There is nothing to post. Try again later!").grid(row = 6, column = 1, padx = 10, pady = 10)

run = tk.Button(text = "Run!", command = lambda: bot(tell_account.get(), tell_password.get(), ig_account.get(), ig_password.get()))

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
