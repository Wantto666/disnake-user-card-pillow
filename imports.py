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
