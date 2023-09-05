import json
import math
import platform
import socket
import tkinter as tk

import psutil
import requests

# Получаем имя компьютера и его IP-адрес
hostname = socket.gethostname()
ip_address = socket.gethostbyname(hostname)

# Получаем информацию о ОС
os_name = platform.system()
os_release = platform.release()

# Получаем информацию о процессоре
processor_name = platform.processor()

# Получаем список всех дисков
disk_partitions = psutil.disk_partitions()

# Получаем информацию о памяти (в байтах)
mem = psutil.virtual_memory()

# Получить имя машины
hostname = socket.gethostname()

# URL удаленного сервера
url = "https://stats.lineclub.ru/hostname.php"

# Параметры запроса
params = {
    "hostname": hostname,
    "ip": ip_address,
    "os": os_release,
    "cpu": processor_name,
    "memory": mem.total // (2 ** 20)
}

# Отправить GET-запрос на сервер
response = requests.get(url, params=params).text

# json_data=json.dumps(response)
data = json.loads(response)

# with open(response, 'r') as f:
#     data=json.load(f)

# Вывести ответ сервера
print(data["hostname"]["title"] + ": " + data["hostname"]["value"])
print(data["ip"]["title"] + ": " + data["ip"]["value"])
print(data["os"]["title"] + ": " + data["os"]["value"])
print(data["cpu"]["title"] + ": " + data["cpu"]["value"])
print(data["memory"]["title"] + ": " + data["memory"]["value"] + "МБ")

text = "{}: {}.".format(data["hostname"]["title"], data["hostname"]["value"])
print(text)


def show_dialog(text, width: 800, height=600):
    # Создаем новое окно
    dialog = tk.Tk()

    # Вычисляем координаты окна для размещения его по центру экрана
    screen_width = dialog.winfo_screenwidth()
    screen_height = dialog.winfo_screenheight()
    x = math.ceil((screen_width - width) / 2)
    y = math.ceil((screen_height - height) / 2)

    # Задаем заголовок окна
    dialog.title("Диалог")

    # Задаем текст в окне
    label = tk.Label(dialog, text=text)
    label.pack()

    # Выводим окно на экран
    dialog.mainloop()


# Показываем диалог с текстом
show_dialog(text, width=400, height=300)

# # Выводим все полученные данные
# print("Имя компьютера:", hostname)
# print("IP-адрес:", ip_address)
# print("ОС:", os_name, os_release)
# print("Процессор:", processor_name)
# # print("Диски:")
# # for partition in disk_partitions:
# #     print(partition.device, "(", partition.fstype, ")", "вместимость", \
# #           psutil.disk_usage(partition.mountpoint).total // (2 ** 30), "ГБ")
# print("Всего памяти:", mem.total // (2 ** 20), "МБ")
