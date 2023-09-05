# import app
import datetime
import getpass
import json
import math
import platform
import socket
import time
import uuid

import psutil
import requests

# URL удаленного сервера
mainDomain = 'https://stats.lineclub.ru/'
interval = 10


class Main:
    def __init__(self, mainDomain, interval):
        self.mainDomain = mainDomain
        self.Interval = interval
        self.mainURL = self.mainDomain + "hostname.php"

    def getSystemVars(self):
        # Получаем имя компьютера и его локальный и внешний IP-адресы
        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)

        # Получаем информацию о ОС
        os_name = platform.system()
        os_release = platform.release()
        os_version = platform.version()

        # Получаем информацию о процессоре
        processor_name = platform.processor()
        processor_usage = psutil.cpu_percent(interval=1)

        # Получаем список всех дисков
        disk_partitions = psutil.disk_partitions()

        # Получаем информацию о памяти (в байтах)
        mem = psutil.virtual_memory()

        # Время работы
        boot_time = psutil.boot_time()
        boot_time_converted = datetime.datetime.fromtimestamp(boot_time)
        uptime = datetime.datetime.now() - boot_time_converted
        uptime_minutes = int(uptime.total_seconds() / 60)
        hours, minutes = divmod(uptime_minutes, 60)
        # Получить имя машины
        hostname = socket.gethostname()

        # имя пользователя
        username = getpass.getuser()

        # MAC-адрес
        mac_address = ':'.join(format(c, '02x') for c in uuid.getnode().to_bytes(6, 'big'))

        # Параметры запроса
        params = {
            "hostname": hostname,
            "ip": ip_address,
            "os_version": os_version,
            "os_name": os_name,
            "os_release": os_release,
            "cpu": processor_name,
            "cpu_usage": str(processor_usage),
            "memory": str(math.ceil(mem.total // (2 ** 20))),
            "memory_used": str(math.ceil(mem.used / 1024 / 1024)),
            "memory_avail": str(math.ceil(mem.available / 1024 / 1024)),
            "boot_time": boot_time_converted,
            "uptime": uptime,
            "username": username,
            "mac_address": mac_address
        }
        self.makeRequest(params)

    def makeRequest(self, params):
        # Отправить GET-запрос на сервер
        response = requests.get(self.mainURL, params=params).text
        data = json.loads(response)
        params["sessionID"] = data["session"]["value"]

        self.makeCycle(params)

    def makeCycle(self, params):
        # отправлять с интервалом
        while True:
            response = requests.get(self.mainURL, params=params).text
            data = json.loads(response)
            text = "{}: {}.\n{}: {}.\n{}: {}.\n{}: {}.\n{}: {}.\n{}: {}.\n{}: {}.\n{}: {}.\n{}: {} МБ.\n{}: {} МБ.\n{}: {} МБ.\n{}: {}.\n{}: {}.\n{}: {}.\n{}: {}.\n".format(
                data["session"]["title"], data["session"]["value"],
                data["hostname"]["title"], data["hostname"]["value"],
                data["ip"]["title"], data["ip"]["value"],
                data["os_version"]["title"], data["os_version"]["value"],
                data["os_name"]["title"], data["os_name"]["value"],
                data["os_release"]["title"], data["os_release"]["value"],
                data["cpu"]["title"], data["cpu"]["value"],
                data["cpu_usage"]["title"], data["cpu_usage"]["value"],
                data["memory"]["title"], data["memory"]["value"],
                data["memory_used"]["title"], data["memory_used"]["value"],
                data["memory_avail"]["title"], data["memory_avail"]["value"],
                data["boot_time"]["title"], data["boot_time"]["value"],
                data["uptime"]["title"], data["uptime"]["value"],
                data["username"]["title"], data["username"]["value"],
                data["mac_address"]["title"], data["mac_address"]["value"]
            )
            print(text)
            time.sleep(self.Interval)


main = Main(
    mainDomain,
    interval
)
getSystemVars = main.getSystemVars()
