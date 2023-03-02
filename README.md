Модуль **[Сam_avigilon 1.02](https://github.com/yarimov/Modul_cam_avigilon_in_trassir/blob/main/cam_avigilon%201.02.py "cam_avigilon 1.02.py")**  предназначен для корректного добавления камер 
Avigilon 3.0C-H4A-D1-IR в видеорегистраторы с операционной  системой Trassir OS. 
Модуль позволяет исправить проблему автофокуса после того, как оператор системы видеонаблюдения выполнит команды для работы трансфокатора (приближения - удаления). 

Камера подключается к регистратору по протоколу Onvif. Это не нативный протокол для подключения камер. В связи с этим наблюдается проблема работы с автофокусом на камерах Avigilon 3.0C-H4A-D1-IR. 

**Описание проблемы:**
На камере есть трансфокатор - это моторизированное изменение фокусного расстояния (приближение - удаление).  После приближения и удаления не наводился фокус на объект наблюдения, изображение размыто. 

**Решение:**
Модуль отслеживает активность событий для камер Avigilon, при обнаружении событий связанных с трансфокатором,  подключается и авторизуется к камере по http и направляет принудительную команду автофокуса.

## Лицензия

Не для коммерческого использования.

## Платформы

Сam_avigilon 1.02 доступен для следующих платформ :
- [Trassit OS] *(TRASSIR-Server 4.x)*

[Trassir OS]: https://trassir.ru/support/soft/
