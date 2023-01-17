from instabot import Bot
from credential.models import Credential


bot = Bot()
bot.login(username=Credential.name, password=Credential.password)
bot.upload_photo(r"C:\photos\girl.jfif", caption="rose image")
