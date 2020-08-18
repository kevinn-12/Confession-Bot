from instabot import Bot
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime
import re
import os
from PIL import Image, ImageTk
import shutil
import tkinter as tk
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

        driver.quit()

        # Pic Formating
        for pics in os.listdir("to_post/"):
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

        # Posting Tells to Instagram
        bot = Bot()

        bot.login(username = ig_account_input,
          		password = ig_password_input)

        for pics in os.listdir("to_post/"):
            bot.upload_photo("to_post/" + str(pics), caption = "test")

        # Movig pics from to_post folder -> posted
        for pics in os.listdir("to_post/"):
            shutil.move("to_post/" + pics, "posted")
            os.rename("posted/" + pics, "posted/" + re.sub(".REMOVE_ME", "", str(pics)))

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
