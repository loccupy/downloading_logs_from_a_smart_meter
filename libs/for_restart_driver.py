import os
import subprocess
import sys
import time
import win32gui
import win32ui
import win32con
import win32api


def find_window(title):
    hwnd = win32gui.FindWindow(None, title)
    if hwnd == 0:
        # print(f"Окно с заголовком '{title}' не найдено.")
        return None
    return hwnd


def click_button(hwnd, button_text):
    button_hwnd = win32gui.FindWindowEx(hwnd, 0, None, button_text)
    if button_hwnd == 0:
        print(f"Кнопка с текстом '{button_text}' не найдена.")
        return
    win32api.SendMessage(button_hwnd, win32con.WM_LBUTTONDOWN, 0, 0)
    win32api.SendMessage(button_hwnd, win32con.WM_LBUTTONUP, 0, 0)


def wait_for_window(title, timeout=10):
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            hwnd = find_window(title)
            if hwnd:
                return hwnd
        except Exception:
            time.sleep(3)
    raise Exception(f"Окно с заголовком '{title}' не найдено за {timeout} секунд")


def close_window(hwnd):
    win32gui.PostMessage(hwnd, win32con.WM_CLOSE, 0, 0)


import os
import sys

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


def install_ch340_windows():
    installer_path = "CH340SER.EXE"
    base_path = resource_path(installer_path)
    print("Запуск установки...")
    result = subprocess.run(["cmd", "/c", base_path], shell=True, creationflags=subprocess.DETACHED_PROCESS)

    # Ждем появления окна и нажимаем INSTALL
    try:
        window_1 = wait_for_window("DriverSetup(X64)")
        click_button(window_1, "INSTALL")
        time.sleep(2)  # Ждем завершения установки

        # Нажимаем OK в окне с сообщением об успешной установке
        window_2 = wait_for_window("DriverSetup")
        click_button(window_2, "ОК")
        print("✅ Драйвер CH340 успешно установлен.")

        close_window(window_1)

    except Exception as e:
        print(f"❌ Ошибка при установке драйвера: {e}")


if __name__ == "__main__":
    install_ch340_windows()

