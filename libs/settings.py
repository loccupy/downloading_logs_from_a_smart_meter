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
LOG_EXPORT_START_TIME = (11, 10)    # Выгрузка журналов

# === Telegram уведомления ===
TELEGRAM_BOT_TOKEN = '7938367301:AAFXCHUuNB3VCuB1Xl7BAISUY7kLpMXAp7o'
TELEGRAM_CHAT_ID_BOT_REPORT = 218940403
# TELEGRAM_CHAT_ID_TESTING = -1003021280639
# TELEGRAM_CHAT_ID_REPORT = -4886311338


# === Пути ===
DATA_COPY_DESTINATION = r'O:/12.Отдел разработки/Отдел тестирования/Отдел тестирования/Опрос и Выгрузка'
