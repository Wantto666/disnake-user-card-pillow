from imports import *

with open('config/config.json') as f:
    data = json.load(f)
    token = data["TOKEN"]
    prefix = data["PREFIX"]



intents = disnake.Intents.all()
bot = commands.Bot(command_prefix=prefix, intents=intents, activity=disnake.Game(name="Майнит мир"), status = disnake.Status.idle)


connection = sqlite3.connect('config/server.db')
cursor = connection.cursor()


@bot.event
async def on_ready():
    cursor.execute("""CREATE TABLE IF NOT EXISTS users (
        name TEXT,
        id INT,
        cash BIGINT,
        rep INT,
        lvl INT,
        server_id INT
    )""")
 

    cursor.execute("""CREATE TABLE IF NOT EXISTS shop (
        role_id INT,
        id INT,
        cost BIGINT
    )""")
 

    for guild in bot.guilds:
        for member in guild.members:
            if cursor.execute(f"SELECT id FROM users WHERE id = {member.id}").fetchone() is None:
                cursor.execute(f"INSERT INTO users VALUES ('{member}', {member.id}, 0, 0, 1, {guild.id})")
            else:
                pass
 
    connection.commit()
    print("It`s work!")


@bot.event
async def on_member_join(member):
    if cursor.execute(f"SELECT id FROM users WHERE id = {member.id}").fetchone() is None:
        cursor.execute(f"INSERT INTO users VALUES ('{member}', {member.id}, 0, 0, 1, {member.guild.id})")
        connection.commit()
    else:
        pass


@bot.slash_command(aliases = ['баланс', 'balance'])
async def balance(ctx, member: disnake.Member = None):
    if member is None:
        await ctx.send(embed = disnake.Embed(
            description = f"""Баланс пользователя **{ctx.author}** составляет **{cursor.execute("SELECT cash FROM users WHERE id = {}".format(ctx.author.id)).fetchone()[0]} :leaves:**"""
        ))
        
    else:
        await ctx.send(embed = disnake.Embed(
            description = f"""Баланс пользователя **{member}** составляет **{cursor.execute("SELECT cash FROM users WHERE id = {}".format(member.id)).fetchone()[0]} :leaves:**"""
        ))  


@bot.command()
async def add_user_group(ctx, group):
    with open("data/group.json", "r", encoding="utf8") as json_file:
        a = json.load(json_file)
    a[f"{ctx.author.id}"] = group
    with open("data/group.json", "w", encoding="utf8") as json_file:
        json.dump(a, json_file, ensure_ascii=False, indent=2)


@bot.command()
async def check_group(ctx):
    with open('data/group.json') as f:
        user_date = json.load(f)
        group = user_date[f"{ctx.author.id}"]
    await ctx.send(group)
    
@bot.command()
async def server(ctx, member: disnake.Member = None):
    if member is None:
        with open('data/group.json') as f:
            user_date = json.load(f)
            group = user_date[f"{ctx.author.id}"]

        name_avatar = ctx.author
        name_file = ctx.author.id
        user_data = { 
        "name": f"{ctx.message.author.display_name}", 
        "xp": cursor.execute("SELECT cash FROM users WHERE id = {}".format(ctx.author.id)).fetchone()[0],
        "next_level_xp": 1450,
        "level": group,
        "percentage": 45,
        }

        try:
            url = ctx.author.avatar.url
            req = Request(url, headers={'User-Agent': 'Mozilla/5.0'}) 
            resource = urlopen(req)                                   
            avatar = open(f"cache/{name_avatar}.png", 'wb')                             
            avatar.write(resource.read())
            avatar.close()                                             

            background = Editor(Canvas((900, 300), color="#23272A"))
            profile = Editor(f"cache/{name_avatar}.png").resize((150, 150)).circle_image()
        except:
            photo = ['assets/pfp.png',
                         'assets/pfp_red.png',
                         'assets/pfp_blue.png'
                         ]
            randrom_avatar = random.choice(photo)

            background = Editor(Canvas((900, 300), color="#23272A"))
            profile = Editor(randrom_avatar).resize((150, 150)).circle_image()

        poppins = Font.poppins(size=40)
        poppins_small = Font.poppins(size=30)

        card_right_shape = [(600, 0), (750, 300), (900, 300), (900, 0)]

        background.polygon(card_right_shape, "#2C2F33")
        background.paste(profile, (30, 30))

        background.rectangle(
            (30, 220), width=650, height=40, fill="#494b4f", radius=20
        )

        money = cursor.execute("SELECT cash FROM users WHERE id = {}".format(ctx.author.id)).fetchone()[0]
        if money > 1450:
            limit = 1450
            money = limit

        if cursor.execute("SELECT cash FROM users WHERE id = {}".format(ctx.author.id)).fetchone()[0] + 0:
            background.bar(
                (30, 220),
                max_width= money,
                height=40,
                percentage=user_data["percentage"],
                fill="#3db374",
                radius=20,
            )

            
        background.text((200, 40), user_data["name"], font=poppins, color="white")

        background.rectangle((200, 100), width=350, height=2, fill="#17F3F6")
        background.text(
            (200, 130),
            f"Group : {user_data['level']} "
            + f" Balance : {user_data['xp']} / {user_data['next_level_xp']}",
            font=poppins_small,
            color="white",
        )

        background.save(f"cache/{name_file}.png")

        await ctx.send(file = disnake.File(f"cache/{name_file}.png"))
    else:
        try:
            with open('data/group.json') as f:
                user_date = json.load(f)
                group = user_date[f"{member.id}"]
        except:
            group = "None"

        name_avatar = member.name
        name_file = member.id
        user_data = { 
        "name": f"{member.name}", 
        "xp": cursor.execute("SELECT cash FROM users WHERE id = {}".format(member.id)).fetchone()[0],
        "next_level_xp": 1450,
        "level": group,
        "percentage": 45,
        }

        try:
            url = member.avatar.url
            req = Request(url, headers={'User-Agent': 'Mozilla/5.0'}) 
            resource = urlopen(req)                                   
            avatar = open(f"cache/{name_avatar}.png", 'wb')                             
            avatar.write(resource.read())
            avatar.close()                                           

            background = Editor(Canvas((900, 300), color="#23272A"))
            profile = Editor(f"cache/{name_avatar}.png").resize((150, 150)).circle_image()
        except:                                          
            photo = ['assets/pfp.png',
                         'assets/pfp_red.png',
                         'assets/pfp_blue.png'
                         ]
            randrom_avatar = random.choice(photo)

            background = Editor(Canvas((900, 300), color="#23272A"))
            profile = Editor(randrom_avatar).resize((150, 150)).circle_image()

        poppins = Font.poppins(size=40)
        poppins_small = Font.poppins(size=30)

        card_right_shape = [(600, 0), (750, 300), (900, 300), (900, 0)]

        background.polygon(card_right_shape, "#2C2F33")
        background.paste(profile, (30, 30))

        background.rectangle(
            (30, 220), width=650, height=40, fill="#494b4f", radius=20
        )

        money = cursor.execute("SELECT cash FROM users WHERE id = {}".format(member.id)).fetchone()[0]
        if money > 1450:
            limit = 1450
            money = limit

        if cursor.execute("SELECT cash FROM users WHERE id = {}".format(member.id)).fetchone()[0] + 0:
            background.bar(
                (30, 220),
                max_width= money,
                height=40,
                percentage=user_data["percentage"],
                fill="#3db374",
                radius=20,
            )

            
        background.text((200, 40), user_data["name"], font=poppins, color="white")

        background.rectangle((200, 100), width=350, height=2, fill="#17F3F6")
        background.text(
            (200, 130),
            f"Group : {user_data['level']} "
            + f" Balance : {user_data['xp']} / {user_data['next_level_xp']}",
            font=poppins_small,
            color="white",
        )

        background.save(f"cache/{name_file}.png")

        await ctx.send(file = disnake.File(f"cache/{name_file}.png"))


@bot.command(aliases = ['award'])
async def __award(ctx, member: disnake.Member = None, amount: int = None):
    if member is None:
        await ctx.send(f"**{ctx.author}**, укажите пользователя, которому желаете выдать определенную сумму")
    else:
        if amount is None:
            await ctx.send(f"**{ctx.author}**, укажите сумму, которую желаете начислить на счет пользователя")
        elif amount < 1:
            await ctx.send(f"**{ctx.author}**, укажите сумму больше 1 :leaves:")
        else:
            cursor.execute("UPDATE users SET cash = cash + {} WHERE id = {}".format(amount, member.id))
            connection.commit()
 
            await ctx.message.add_reaction('✅')


@bot.command(aliases = ['take'])
async def __take(ctx, member: disnake.Member = None, amount = None):
    if member is None:
        await ctx.send(f"**{ctx.author}**, укажите пользователя, у которого желаете отнять сумму денег")
    else:
        if amount is None:
            await ctx.send(f"**{ctx.author}**, укажите сумму, которую желаете отнять у счета пользователя")
        elif amount == 'all':
            cursor.execute("UPDATE users SET cash = {} WHERE id = {}".format(0, member.id))
            connection.commit()
 
            await ctx.message.add_reaction('✅')
        elif int(amount) < 1:
            await ctx.send(f"**{ctx.author}**, укажите сумму больше 1 :leaves:")
        else:
            cursor.execute("UPDATE users SET cash = cash - {} WHERE id = {}".format(int(amount), member.id))
            connection.commit()
 
            await ctx.message.add_reaction('✅')

bot.run(token)