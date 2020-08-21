from instabot import Bot
import sys

bot = Bot()
try:
    bot.login(username = "ig_account_input", password = "ig_password_input")
except:
    print("Oops!", sys.exc_info()[0], "occurred.")
