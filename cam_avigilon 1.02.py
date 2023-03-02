''' Модуль предназначен для корректного добавления камер Avigilon 3.0C-H4A-D1-IR в видеорегистраторы с операционной
системой Trassir OS. Камера подключается к регистратору по протоколу Onvif. На камере есть трансфокатор
(моторизированное изменение фокусного расстояния (приближение - удаление)). Модуль позволяет исправить проблему
автофокуса после того, как оператор системы видеонаблюдения выполнит команды для работы трансфокатора (приближения -
удаления). Без модуля после приближения и удаления не наводился фокус на объект наблюдения, изображение было размыто.
Модуль отслеживает активность событий для камер Avigilon, при обнаружении событий связанных с трансфокатором,
подключается и авторизуется к камере по http и направляет принудительную команду автофокуса.

'''

import urllib
import urllib2

cam1 = object("Cam1-PTZ")
cam2 = object("Cam2-PTZ")
# Имена камер в Trassir OS. Эта команда получает события из Trassir OS

url1 = "http://10.87.75.101/"
url2 = "http://10.87.75.102/"
# ip адреса камер

username1 = "admin"
password1 = "admin"
# Данные для авторизации для камеры cam1

username2 = "admin"
password2 = "admin"
# Данные для авторизации для камеры cam2

realm1 = "101711155225"
realm2 = "101711155399"
# Строка ответа камеры. Уникальна для каждой камеры. Ее можно получить из консоли отладки в Trassir OS 

data = {'focusSingleShot': 1}
# команда для отправки автофокуса в камеру в http запросе


class DigestAuth():
    ''' Класс для подключения и авторизации к камерам и формирования НТТР запроса.   '''

    def __init__(self, user, passwd, base_url, realm=''):
        self.user = user
        self.passwd = passwd
        self.base_url = base_url
        self.realm = realm
        self.prepare_urllib()

    def prepare_urllib(self):
        authhandler = urllib2.HTTPDigestAuthHandler()
        authhandler.add_password(self.realm, self.base_url, self.user, self.passwd)
        opener = urllib2.build_opener(authhandler)
        urllib2.install_opener(opener)

    def get_response(self, request, data=None):
        if data:
            response = urllib2.urlopen(self.base_url + request, urllib.urlencode(data))
        else:
            response = urllib2.urlopen(self.base_url + request)
        content = response.read()
        response.close()
        return content


control_cam1 = DigestAuth(username1, password1, url1, realm1)
control_cam2 = DigestAuth(username2, password2, url2, realm2)
# Объекты для работы с классом DigestAuth


def delayed_start1():
    ''' Вызов метода автофокуса для камеры Cam1. '''

    control_cam1.get_response("cgi-x/focus", data)


def delayed_start2():
    ''' Вызов метода автофокуса для камеры Cam2. '''

    control_cam2.get_response("cgi-x/focus", data)


# Функции F2 и F3 задают условие. Условие камера и событие PTZ по камере
def response_to_an_event(event):
    ''' Отслеживание команд управления приближением и удалением (PTZ) для камер cam1,cam2. Подача команд автофокуса. '''

    if event.type == "PTZ/STOP" and cam1.guid == event.channel:
        # Ожидаем команду завершения управления трансфокатором камеры 1 и посылаем команду автофокуса через 0.5 секунды.
        timeout(500, delayed_start1)

    if event.type == "PTZ/STOP" and cam2.guid == event.channel:
        # Ожидаем команду завершения управления трансфокатором камеры 2 и посылаем команду автофокуса через 0.5 секунды.
        timeout(500, delayed_start2)


if __name__ == "__main__":
    activate_on_ptz_events(response_to_an_event)

    # В некоторых версиях ПО Trassir нужно удалить конструкцию "if __name__ == '__main__':", камеры при старте скрипта
    # получат принудительно команду на автофокус.
