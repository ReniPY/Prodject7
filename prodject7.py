import ptbot
import os
from dotenv import load_dotenv
from pytimeparse import parse


load_dotenv()
TG_TOKEN = os.environ['token']
TG_CHAT_ID = os.environ['login']


def render_progressbar(
        total,
        iteration,
        prefix='',
        suffix='',
        length=30,
        fill='█',
        zfill='░'):
    iteration = min(total, iteration)
    percent = "{0:.1f}"
    percent = percent.format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    pbar = fill * filled_length + zfill * (length - filled_length)
    return '{0} |{1}| {2}% {3}'.format(prefix, pbar, percent, suffix)


def notify_progress(secs_left, message_id, chat_id, start_seconds):
    stop_seconds = start_seconds - secs_left
    message = f'Осталось {secs_left} секунд(ы).\n'
    progressbar = render_progressbar(start_seconds, stop_seconds)
    update_message = message + progressbar
    bot.update_message(chat_id, message_id, update_message)


def notify(chat_id, text):
    bot.send_message(chat_id, "Время вышло")


def reply(chat_id, text):
    chat_messange = parse(text)
    message = f"Таймер запущен на {chat_messange} секунд!"
    message_id = bot.send_message(chat_id, message)
    bot.create_countdown(
        chat_messange,
        notify_progress,
        message_id=message_id,
        chat_id=chat_id,
        start_seconds=chat_messange
    )
    bot.create_timer(chat_messange, notify, chat_id=chat_id, text=text)


if __name__ == "__main__":
    bot = ptbot.Bot(TG_TOKEN)
    bot.reply_on_message(reply)
    bot.run_bot()
