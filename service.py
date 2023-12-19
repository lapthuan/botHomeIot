
import os
import requests
import telebot
import sys

from dotenv import load_dotenv
from pathlib import Path
from requests.exceptions import ConnectionError, ReadTimeout

dotenv_path = Path('.env')
load_dotenv(dotenv_path=dotenv_path)


# Lấy thông tin đăng nhập từ biến môi trường
BOT_TOKEN = os.getenv('BOT_TOKEN')
USERNAME = os.getenv('VISA_USERNAME')
PASSWORD = os.getenv('VISA_PASSWORD')
bot = telebot.TeleBot(BOT_TOKEN)

# Định nghĩa các URL cần sử dụng
search_url = os.getenv('SEARCH_URL')
login_url = os.getenv('LOGIN_URL')
doOpenSuspend_url = os.getenv('DO_OPEN_SUSPEND_URL')
detail_url = os.getenv('DETAIL_URL')

# Khởi tạo một session HTTP sử dụng module requests
session = requests.Session()
url = "https://homeiotnew-default-rtdb.asia-southeast1.firebasedatabase.app/iotdata.json"
print(f"Khởi động chương trình")


def checkND():
    try:
        response = session.get(url)
        data = response.json()
        dhtsensor_data = data.get("dhtsensor")
        value = dhtsensor_data.get("nhietdo")
        return value
    except:
        return ('Lỗi kết nối hãy thử lại')


@bot.message_handler(commands=['nhietdo'])
def nhietdo_command(message):
    try:
        status = checkND()
        bot.reply_to(message, f"Nhiệt độ hiện tại là : {status} °C")
    except:
        bot.reply_to(message, f"Lỗi")


def checkDA():
    try:
        response = session.get(url)
        data = response.json()
        dhtsensor_data = data.get("dhtsensor")
        value = dhtsensor_data.get("doam")
        return value
    except:
        return ('Lỗi kết nối hãy thử lại')


@bot.message_handler(commands=['doam'])
def doam_command(message):
    try:
        status = checkDA()
        bot.reply_to(message, f"Độ ẩm hiện tại là : {status} %")
    except:
        bot.reply_to(message, f"Lỗi")


def checkLua():
    try:
        response = session.get(url)
        data = response.json()
        value = data.get("Flame")
        if (value == 1):
            return "cảnh báo"
        else:
            return "Bình thường"
        return value
    except:
        return ('Lỗi kết nối hãy thử lại')


@bot.message_handler(commands=['lua'])
def Lua_command(message):
    try:
        status = checkLua()
        bot.reply_to(message, f"Phát hiện lửa : {status} ")
    except:
        bot.reply_to(message, f"Lỗi")


def checkCD():
    try:
        response = session.get(url)
        data = response.json()
        value = data.get("chuyendong")
        if (value == 1):
            return "có người"
        else:
            return "không có người"
    except:
        return ('Lỗi kết nối hãy thử lại')


@bot.message_handler(commands=['chuyendong'])
def CD_command(message):
    try:
        status = checkCD()
        bot.reply_to(message, f"Phát hiện : {status} ")
    except:
        bot.reply_to(message, f"Lỗi")


@bot.message_handler(commands=['lenh'])
def help_command(message):
    try:
        key_string = """/nhietdo
/doam
/chuyendong 
/lua
"""
        bot.reply_to(message, key_string)
    except Exception as e:
        bot.reply_to(message, "Mất kết nối")


try:
    bot.infinity_polling(timeout=10, long_polling_timeout=5)
except (ConnectionError, ReadTimeout) as e:
    sys.stdout.flush()
    os.execv(sys.argv[0], sys.argv)
else:
    bot.infinity_polling(timeout=10, long_polling_timeout=5)
