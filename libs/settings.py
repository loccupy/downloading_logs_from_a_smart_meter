"""
Централизованный конфигурационный файл приложения.
Содержит все жестко закодированные значения: пароли, токены, таймеры, расписание.
"""

# === Подключение к счётчикам ===
PASSWORD = '1234567898765432'
AUTHENTICATION = "High"
CLIENT_ADDRESS = 48

# (hour, minute) — время запуска задач
METER_SURVEY_START_TIME = (11, 54)   # Опрос счётчиков
LOG_EXPORT_START_TIME = (16, 10)    # Выгрузка журналов

# === Telegram уведомления ===
TELEGRAM_BOT_TOKEN = '7938367301:AAFXCHUuNB3VCuB1Xl7BAISUY7kLpMXAp7o'
TELEGRAM_CHAT_ID_BOT_REPORT = 218940403
TELEGRAM_PROXY_URL = "http://192.168.0.107:8080"  # Прокси для Telegram (VPN не нужен)

# === Email уведомления ===
SMTP_SERVER = "smtp.mail.ru"
SMTP_PORT = 465
EMAIL_SENDER = "as.nikitin@promenergo-rt.ru"
EMAIL_PASSWORD = "iuIdEw7pgBI0xdaRJ6oL"  # App password для Gmail   u29292fNZkgy7pM49mMn   UeO1DUyr1ou_
EMAIL_RECEIVER = "as.nikitin@promenergo-rt.ru"


# === Пути ===
DATA_COPY_DESTINATION = r'O:/12.Отдел разработки/Отдел тестирования/Отдел тестирования/Опрос и Выгрузка'
