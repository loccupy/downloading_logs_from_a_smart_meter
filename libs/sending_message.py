from notifiers import get_notifier

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
                        token='7938367301:AAFXCHUuNB3VCuB1Xl7BAISUY7kLpMXAp7o',
                        chat_id=218940403)

        # Отправить в чат Тестировочная
        # telegram = get_notifier('telegram')
        # telegram.notify(message=string,
        #                 token='7938367301:AAFXCHUuNB3VCuB1Xl7BAISUY7kLpMXAp7o',
        #                 chat_id=-1003021280639)

    except Exception as e:
        print(f"Невозможно отправить сообщение в телегу, ошибка {e.args}")