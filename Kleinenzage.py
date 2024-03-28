import asyncio
import logging
import time
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from bs4 import BeautifulSoup
import urllib.request
import sqlite3 as sq

def bases():
    db = sq.connect('db.db')
    cur = db.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS slots(link TEXT, description TEXT)')
    db.commit()
    db.close()

def add_slotss(link, description):
    db = sq.connect('db.db')
    cur = db.cursor()
    cur.execute('INSERT INTO slots (link, description) VALUES (?, ?)',
                (link, description))
    db.commit()
    time.sleep(0.01)
    db.close()

def ifs(link):
    db = sq.connect('db.db')
    cur = db.cursor()
    cur.execute('SELECT * FROM slots WHERE link = ?', (link,))
    row = cur.fetchone()
    db.close()
    return row

bases()

ADMINS = [1356524924, 1916071797]
logging.basicConfig(level=logging.INFO)
bot = Bot(token="6002813414:AAFFoTpEURzy1aFz6E7i9PPmXHoLN_uJPRI")
dp = Dispatcher()

@dp.message(CommandStart())
async def chat(message: types.message):
    user_id = message.from_user.id
    await bot.send_message(user_id, text=f"Bot active")

async def site():
    global s
    while True:

        url = 'https://www.kleinanzeigen.de/s-zu-verschenken-tauschen/memmingen/c272l7277r5'

        request = urllib.request.Request(url)
        user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:87.0) Gecko/20100101 Firefox/87.0'
        request.add_header('User-Agent', user_agent)
        response = urllib.request.urlopen(request)

        soup = BeautifulSoup(response, 'lxml')
        print('Log in to the site!')

        alle = soup.find('div', class_='position-relative').find_all('div', class_='aditem-image')

        i = 0

        for all in alle:
            i += 1
            url = all.find_next('a').get('href')
            img = all.find_next("img").get('src')
            link = f'https://www.kleinanzeigen.de/{url}'
            row = ifs(link)
            if row:
                pass
            else:
                print(f'{link}')
                for ADMIN in ADMINS:
                    await bot.send_photo(chat_id=ADMIN, photo=img, caption=f'Ссылка: {link}')
                add_slotss(link, img)
        print('Expectation...')
        time.sleep(180)

async def main():
    asyncio.create_task(site())
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())