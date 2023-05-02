Документация:

[![Banner](https://i.imgur.com/3K9yIfK.png)](https://t.me/wantto666)

disnake
=======

<p align="center">
    <a href="https://discord.gg/2ZJxC9E4wm"><img src="https://img.shields.io/discord/808030843078836254?style=flat-square&color=5865f2&logo=discord&logoColor=ffffff&label=discord" alt="Discord server invite" /></a>
</p>

Перед запуском зайдите в файл imports.py и установите каждую библиотеку.

Примечания
------------

- Все Импорты находяться в файле imports.py
- [Disnake](https://docs.disnake.dev/en/stable/)- Синтаксис библиотеки

<sup>Бот написан на синтаксисе библиотеке `disnake 1.7.3`.</sup>

Установка
----------

**Бот был написан на версии Python 3.11.3**

Команды для установки библиотеки:

``` sh
# Linux/macOS
python3 -m pip install -U disnake==1.7.3

# Windows
py -3 -m pip install -U disnake==1.7.3
```

Настройка бота
-------------
Файл конфигурации бота находиться по этому пути: config/config.json

``` json
{
    "TOKEN": "TOKEN",
    "PREFIX": "?"
}
### Файл с импортами: imports.py

``` py
try:
    from urllib.request import urlopen
    import disnake
    from disnake.ext import commands

    from PIL import Image, ImageFilter, ImageDraw, ImageFont, ImageOps
    import sqlite3
    import random
    import json
    from flask import Request
    from io import BytesIO
    from easy_pil import Canvas, Editor, Font
    from urllib.request import Request, urlopen

except ImportError:
    print("Библиотеки не установлены")

```
