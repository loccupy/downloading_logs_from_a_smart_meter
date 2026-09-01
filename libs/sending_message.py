from notifiers import get_notifier

from libs.settings import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID_BOT_REPORT

global_list = []
global_message = []


def add_to_global_list(item):
    global_list.append(item)


def clear_global_list():
    global_list.clear()


def add_to_global_message(item):
    global_message.append(item)


def clear_global_message():
    global_message.clear()


def message_in_out(string):
    try:
        # Отправить в бот Отчет
        telegram = get_notifier('telegram')
        telegram.notify(message=string,
                        token=TELEGRAM_BOT_TOKEN,
                        chat_id=TELEGRAM_CHAT_ID_BOT_REPORT)
    except Exception as e:
        print(f"Невозможно отправить сообщение в телегу, ошибка >> {e}")
