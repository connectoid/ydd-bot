import os
import dotenv
import requests
from urllib.parse import urlencode, unquote

from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.types import FSInputFile

dotenv.load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

BASE_URL = 'https://cloud-api.yandex.net/v1/disk/public/resources/download?'
TEST_URL = 'https://disk.yandex.ru/d/-kncz6cshtxBlQ'
TEST_URL = 'https://disk.yandex.ru/i/yBRtFPHfjceDxw'
ERRORS = ['WRONG LINK', 'CANT DOWNLOAD', 'FILE IS TOO BIG']
MAX_FILE_SIZE = 52428800

def download_file(url):
    final_url = BASE_URL + urlencode(dict(public_key=url))
    response = requests.get(final_url)
    print(response)
    print(response.json())
    if response.status_code == 200:
        print(response.json())
        filesize = response.json()['href'].split('fsize=')[1].split('&')[0]
        if int(filesize) < MAX_FILE_SIZE:
            print(filesize)
            filename = response.json()['href'].split('&')[1].split('=')[1]
            filename = unquote(filename)
            print(filename)
            download_url = response.json()['href']
            download_response = requests.get(download_url)
            if download_response.status_code == 200:
                print(download_response)
                with open(filename, 'wb') as f:   # Здесь укажите нужный путь к файлу
                    f.write(download_response.content)
                return filename
            else: 
                print('CANT DOWNLOAD')
                return 'CANT DOWNLOAD'
        else:
            print('FILE IS TOO BIG')
            return 'FILE IS TOO BIG'
    else:
        print('WRONG LINK')
        return 'WRONG LINK'

@dp.message(Command(commands=['start']))
async def proccess_start_command(message: Message):
    await message.answer('Приветствую. Вы запустили бот-загрузчик файлов с Яндекс Диска. '
                         'Отправьте мне ссылку на файл находящийся на Яндекс Диске.')
    
@dp.message()
async def send_echo(message: Message):
    filename = download_file(message.text)
    if filename not in ERRORS:
        await message.reply(f'Файл {filename} готов к скачиванию, ожидайте')
        send_file = FSInputFile(filename)
        await message.reply_document(send_file)
    else:
        await message.reply(filename)


if __name__ == '__main__':
    dp.run_polling(bot)
    # download_file(TEST_URL)
