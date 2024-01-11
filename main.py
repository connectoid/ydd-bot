import os
import dotenv
import requests
from urllib.parse import urlencode

from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message

dotenv.load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

BASE_URL = 'https://cloud-api.yandex.net/v1/disk/public/resources/download?'
TEST_URL = 'https://disk.yandex.ru/d/-kncz6cshtxBlQ'
TEST_URL = 'https://disk.yandex.ru/i/yBRtFPHfjceDxw'

def download_file(url):
    # Получаем загрузочную ссылку
    final_url = BASE_URL + urlencode(dict(public_key=url))
    response = requests.get(final_url)
    if response.status_code == 200:
        print(url)
        print(response)
        download_url = response.json()['href']

        # Загружаем файл и сохраняем его
        download_response = requests.get(download_url)
        if download_response.status_code == 200:
            print(download_response)
            with open('downloaded_file.txt', 'wb') as f:   # Здесь укажите нужный путь к файлу
                f.write(download_response.content)
        else: 
            print('CANT DOWNLOAD')
    else:
        print('WRONG LINK')

@dp.message(Command(commands=['start']))
async def proccess_start_command(message: Message):
    await message.answer('Приветствую. Вы запустили бот-загрузчик файлов с Яндекс Диска. '
                         'Отправьте мне ссылку на файл находящийся на Яндекс Диске.')
    
@dp.message()
async def send_echo(message: Message):
    await message.reply(message.text)
    download_file(message.text)

if __name__ == '__main__':
    dp.run_polling(bot)
    # download_file(TEST_URL)