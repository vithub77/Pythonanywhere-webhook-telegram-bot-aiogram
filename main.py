from aiogram import Bot, Dispatcher, types
from flask import Flask, request
import asyncio
import requests


token = '' # tg token
web_hook = 'https://your_namename.pythonanywhere.com' # url web pythonanywhere
secret_val = '' # random value

# disconnect if webhook created
requests.get(f'https://api.telegram.org/bot{token}/deleteWebhook?url={web_hook}/{secret_val}')

# init flask
app = Flask(__name__)

# init bot
bot = Bot(token=token, proxy="http://proxy.server:3128")
Bot.set_current(bot)
dp = Dispatcher(bot)


# connect webhook
requests.get(f'https://api.telegram.org/bot{token}/setWebhook?url={web_hook}/{secret_val}')



# creat asyncio event loop to interact with aiogram
loop = asyncio.get_event_loop()

# simple echo bot
@dp.message_handler()
async def send_welcome(message: types.Message):
    name = ''
    if message.from_user.username:
        name = message.from_user.username
    await message.reply(f"Привет {name}! Я Эхо бот!")

# update data in class instance Dispatcher(dp)
async def myupdate(upd):
    update = types.Update(**upd)
    await dp.process_updates([update])

# catch webhooks from telegram
@app.route(f'/{secret_val}', methods=['POST'])
def hello_world():
    if request.method == "POST":
        request_data = request.get_json()
        tasks = [loop.create_task(myupdate(request_data))]
        wait_tasks = asyncio.wait(tasks)
        loop.run_until_complete(wait_tasks)
    return 'ok', 200
