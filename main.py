from vkbottle import Keyboard, Text, BaseStateGroup, CtxStorage, VKPay, KeyboardButtonColor
from vkbottle.tools import PhotoMessageUploader
from vkbottle.bot import Bot, Message
import psycopg2
import json

token = "vk1.a.hHMpk86LD-qDpLrscN9vz-NV5gYnf5QIU3Cz5-tJAdZdqKP92B2c_XfAtRF5M3rcyUVtr3dl2OG0MPLEwKD0tbj2fcVYF56HCcQx7ZbMBXc8yIWhJSPb_BrJutS6wk0iWRr1_PJalVlp2QveywAdugnYmc6cVZrcfyaPtCWecyoGLGEToTioN-J8Nxc8q4Duy8mlUK--NtZxH24R7v3xxA"
bot = Bot(token=token)
conn = psycopg2.connect(user="postgres", password="fhdSazpUWPRSkixFiundluYnsWGRtTbl", host="roundhouse.proxy.rlwy.net",
port="37551", database="railway")

cursor = conn.cursor()
ctx = CtxStorage()

class Delete(BaseStateGroup):
    goods_id = 0
class Goods(BaseStateGroup):
    good = 0
    size = 1
    amount = 2
    address = 3
class Add(BaseStateGroup):
    name = 0
    type = 1
    company = 2
    color = 3
    description = 4
    price = 5
    photo_id = 6

@bot.on.private_message(text=["привет", "/start", "start"])
async def greetings(message: Message):
    if message.from_id != 225254274:
        keyboard = Keyboard(inline=True)
        keyboard.add(Text("Купить", {"option": "buy"}))
        keyboard.add(Text("Корзина", {"option": "cart"}))
    else:
        keyboard = Keyboard(inline=True)
        keyboard.add(Text("Купить", {"option": "buy"}))
        keyboard.add(Text("Корзина", {"option": "cart"}))
        keyboard.row()
        keyboard.add(Text("Добавить товар", {"option": "add"}))
        keyboard.add(Text("Удалить товар", {"option": "delete"}))
    await message.answer("Выберите что-то из списка", keyboard=keyboard)

@bot.on.private_message(payload={"option": "delete"})
async def delete_goods(message: Message):
    await bot.state_dispenser.set(message.peer_id, Delete.goods_id)
    return "Введите id товара"


@bot.on.private_message(state=Delete.goods_id)
async def add_name(message: Message):
    ctx.set("goods_id", message.text)
    try:
        cursor.execute(f"DELETE FROM goods where id = {int(message.text)}")
        conn.commit()

    except:
        await message.answer("Товар не удален")
        await bot.state_dispenser.delete(message.peer_id)

    else:
        await message.answer("Товар удален")
        await bot.state_dispenser.delete(message.peer_id)

@bot.on.private_message(payload={"option": "add"})
async def add_goods(message: Message):
    await bot.state_dispenser.set(message.peer_id, Add.name)
    return "Введите название товара"


@bot.on.private_message(state=Add.name)
async def add_name(message: Message):
    ctx.set("name", message.text)
    await bot.state_dispenser.set(message.peer_id, Add.type)
    return "Введите тип продукта"


@bot.on.private_message(state=Add.type)
async def add_type(message: Message):
    ctx.set("type", message.text)
    await bot.state_dispenser.set(message.peer_id, Add.company)
    return "Введите компанию продукта"
@bot.on.private_message(state=Add.company)
async def add_company(message: Message):
    ctx.set("company", message.text)
    await bot.state_dispenser.set(message.peer_id, Add.color)
    return "Введите цвет продукта"


@bot.on.private_message(state=Add.color)
async def add_color(message: Message):
    ctx.set("color", message.text)
    await bot.state_dispenser.set(message.peer_id, Add.description)
    return "Введите описание продукта"


@bot.on.private_message(state=Add.description)
async def add_description(message: Message):
    ctx.set("description", message.text)
    await bot.state_dispenser.set(message.peer_id, Add.price)
    return "Введите цену продукта"


@bot.on.private_message(state=Add.price)
async def add_price(message: Message):
    ctx.set("price", message.text)
    await bot.state_dispenser.set(message.peer_id, Add.photo_id)
    return "Введите id фотографии"


@bot.on.private_message(state=Add.photo_id)
async def add_photo_id(message: Message):
    name = ctx.get("name")
    goods_type = ctx.get("type")
    company = ctx.get("company")
    color = ctx.get("color")
    description = ctx.get("description")
    price = ctx.get("price")
    photo_id = message.text
    try:
        cursor.execute(f"insert into goods (name, type, company, color, description, price, photo_id)"
                       f" values('{str(name)}', '{str(goods_type)}', '{str(company)}', '{str(color)}',"
                       f" '{str(description)}', {int(price)}, '{str(photo_id)}')")
        conn.commit()
    except:
        await message.answer("Товар не был занесен в бд")
        await bot.state_dispenser.delete(message.peer_id)
    else:
        await message.answer("Товар успешно добавлен в бд!")

        await bot.state_dispenser.delete(message.peer_id)

@bot.on.private_message(payload={"option": "cart"})
async def cart_options(message: Message):
    cursor.execute(f"SELECT * from cart inner join goods on cart.goods_id = goods.id and cart.user_id = {message.from_id}")
    carts = cursor.fetchall()
    if cursor.rowcount > 0:
        for i in carts:
            payload = {"delete": f"{i[0]}"}
            payload2 = json.dumps(payload)
            carousel = {
                "type": "carousel",
                "elements": [{
                    "title": f"{i[9]} - {i[7]}\n {i[12]}₽",
                    "description": f"Цвет: {i[10]}\n{i[11]}",
                    "photo_id": f"{i[13]}",
                    "buttons": [{
                        "action": {
                            "type": "text",
                            "label": "Купить",
                            "payload": "{\"test\": \"1\"}"
                        }
                    },
                        {
                            "action": {
                                "type": "text",
                                "label": "Удалить из корзины",
                                "payload": payload2
                            }
                        }]
                }]
            }
            answer = json.dumps(carousel)
            await message.answer("Товар", template=answer)
    else:
        await message.answer("Корзина пуста")


@bot.on.private_message(text="Удалить из корзины")
async def delete_from_cart(message: Message):
    payload = message.payload
    payload = json.loads(payload)
    g_id = payload["delete"]
    try:
        cursor.execute(f"Delete from cart where (id = {g_id})")
        conn.commit()
    except:
        await message.answer("Товар не был удален")
    else:
        await message.answer("Товар успешно удален из корзины!")


@bot.on.private_message(payload={"option": "buy"})
async def buy_options(message: Message):
    keyboard = Keyboard(inline=True)
    keyboard.add(Text("Обувь", {"type": "shoes"}))
    keyboard.add(Text("Одежда", {"type": "clothing"}))
    await message.answer("Выберите что-то из списка", keyboard=keyboard)


@bot.on.private_message(text=["Обувь", "Одежда"])
async def name_function(message: Message):
    payload = message.payload
    payload = json.loads(payload)
    buy_type = payload["type"]
    keyboard = Keyboard(one_time=True)
    cursor.execute(f"SELECT name from company where (type = '{buy_type}')")
    name_and_company = cursor.fetchall()
    a = 1
    for i in name_and_company:
        if a % 4:
            if a != len(name_and_company):
                keyboard.add(Text(f"Посмотреть {i[0]}", {"type_of": f"{buy_type}"}), color=KeyboardButtonColor.POSITIVE)
                keyboard.row()
        else:
            if a != len(name_and_company):
                keyboard.add(Text(f"Посмотреть {i[0]}", {"type_of": f"{buy_type}"}), color=KeyboardButtonColor.POSITIVE)
                keyboard.row()
        if a == len(name_and_company):
            keyboard.add(Text(f"Посмотреть {i[0]}", {"type_of": f"{buy_type}"}), color=KeyboardButtonColor.POSITIVE)
        a += 1
    await message.answer("Компании", keyboard=keyboard)


@bot.on.private_message(text=f"Посмотреть <company>")
async def shoes(message: Message, company: str):
    payload = message.payload
    payload = json.loads(payload)
    type_of = payload["type_of"]

    cursor.execute(f"SELECT * from goods where (company = '{company}' and type = '{type_of}')")
    goods = cursor.fetchall()
    conn.commit()
    carousel = {
        "type": "carousel",
        "elements": []
    }
    a = 0
    for i in goods:
        a += 1
        payload = {"cart": f"{i[0]}"}
        payload2 = json.dumps(payload)
        carousel["elements"].append({
            "title": f"{i[3]} - {i[1]}\n {i[6]}₽",
            "description": f"Цвет: {i[4]}\n{i[5]}",
            "photo_id": f"{i[7]}",
            "buttons": [{
                "action": {
                    "type": "text",
                    "label": "Добавить в корзину",
                    "payload": payload2
                }
            }]
        })

    answer = json.dumps(carousel)

    await message.answer(f"Вы можете ознакомиться с брендом одежды {company}.", template=answer)


@bot.on.private_message(text="Добавить в корзину")
async def cart_add(message: Message):
    payload = message.payload
    payload = json.loads(payload)
    g_id = payload["cart"][0]
    ctx.set("good", g_id)
    await bot.state_dispenser.set(message.peer_id, Goods.size)
    return "Введите размер"


@bot.on.private_message(state=Goods.size)
async def size_handler(message: Message):
    size = message.text
    ctx.set("size", size)
    await bot.state_dispenser.set(message.peer_id, Goods.amount)
    return "Введите количество"


@bot.on.private_message(state=Goods.amount)
async def amount_handler(message: Message):
    amount = message.text
    ctx.set("amount", amount)
    await bot.state_dispenser.set(message.peer_id, Goods.address)
    return "Введите адрес"


@bot.on.private_message(state=Goods.address)
async def address_handler(message: Message):
    good = ctx.get("good")
    size = ctx.get("size")
    amount = ctx.get("amount")
    address = str(message.text)
    try:
        cursor.execute(f"insert into cart (user_id, goods_id, size, amount, address)"
                       f" values({message.from_id}, {int(good)}, {int(size)}, {int(amount)}, '{str(address)}')")
        conn.commit()
    except:
        await message.answer("Товар не был добавлен")
    else:
        await message.answer("Товар успешно добавлен в корзину!")

bot.run_forever()
