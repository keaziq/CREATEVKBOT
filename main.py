from geopy import Location
from vkbottle import Keyboard, KeyboardButtonColor, Text, template_gen, TemplateElement, BaseStateGroup, CtxStorage, \
    OpenLink, Location
from vkbottle.bot import Bot, Message



bot = Bot(token = "vk1.a.hHMpk86LD-qDpLrscN9vz-NV5gYnf5QIU3Cz5-tJAdZdqKP92B2c_XfAtRF5M3rcyUVtr3dl2OG0MPLEwKD0tbj2fcVYF56HCcQx7ZbMBXc8yIWhJSPb_BrJutS6wk0iWRr1_PJalVlp2QveywAdugnYmc6cVZrcfyaPtCWecyoGLGEToTioN-J8Nxc8q4Duy8mlUK--NtZxH24R7v3xxA")

ctx = CtxStorage()

conn = psycopg2.connect(user="postgres", password="mvzXJObZmoogeViIsPWNvEHIaVSVLrZs", host="monorail.proxy.rlwy.net",
                        port="10139", database="railway")
cursor = conn.cursor()


hello = ["Привет","привет", 'start', 'Хай','хай', 'Ку-ку', 'здарова','Здарова',
         'Здраствуйте','здраствуйте', 'Здраствуй','здраствуй']

class Database(BaseStateGroup):

    NAME = 0
    AGE = 1
    ABOUT = 2

@bot.on.message(text=hello)
@bot.on.message(payload={"brand": "hello"})
async def message_welcome(message: Message):
    keyboard = Keyboard(inline=True)
    keyboard.add(Text(f"Меню", {"brand": "menu"}), color=KeyboardButtonColor.PRIMARY)
    # keyboard.add(Text(f"Оформить заказ", {"cmd": "zakaz"}), color=KeyboardButtonColor.PRIMARY)
    # keyboard.row()
    # keyboard.row()
    # keyboard.add(Text("Задать вопрос", {"cmd": "Задать вопрос"}), color=KeyboardButtonColor.SECONDARY)
    user = await bot.api.users.get(message.from_id)
    await message.answer(f" Здраствуйте  , {user[0].first_name}."
                         f" Что вы хотите сделать сегодня?", keyboard=keyboard)

@bot.on.message(text="меню")
@bot.on.message(payload={"brand": "menu"})
async def menu(message: Message):
    keyboard = Keyboard(one_time=True)

    keyboard.add(Text(f"Посмотреть ассортимент товаров", {"brand": "assortment"}), color=KeyboardButtonColor.PRIMARY)
    keyboard.row()
    keyboard.add(Text("Развлечение", {"brand": "Развлечение"}), color=KeyboardButtonColor.SECONDARY)
    keyboard.row()
    keyboard.add(Location())
    keyboard.row()
    keyboard.add(OpenLink("https://vk.com/club224358783", "Группа сообщества"))

    await message.answer(message="Выберай что тебе надо", keyboard=keyboard)
# @bot.on.message(lev="/reg")
# async def reg_handler(message: Message):
# 	await bot.state_dispenser.set(message.peer_id, Database.NAME)
# 	return "Введите ваше имя"
#
# @bot.on.message(state=Database.NAME)
# async def name_handler(message: Message):
# 	ctx.set("name", message.text)
# 	await bot.state_dispenser.set(message.peer_id, Database.AGE)
# 	return "Введите ваш возраст"
#
# @bot.on.message(state=Database.AGE)
# async def age_handler(message: Message):
# 	ctx.set("age", message.text)
# 	await bot.state_dispenser.set(message.peer_id, Database.ABOUT)
# 	return "Введите ваш адрес"
#
# @bot.on.message(state=Database.ABOUT)
# async def about_handler(message: Message):
# 	name = ctx.get("name")
# 	age = ctx.get("age")
# 	about = message.text
#
# 	await message.answer(f"{name}\n{age}\n{about}")
# 	return "Регистрация прошла успешно"





@bot.on.message(payload={"brand": "assortment"})
async def carousel_handler(message: Message):

    keyboard_shoes = Keyboard().add(Text("Подробнее", {"brand": "shoes"}), color=KeyboardButtonColor.SECONDARY)
    keyboard_clothes = Keyboard().add(Text("Подробнее", {"brand": "clothes"}), color=KeyboardButtonColor.SECONDARY)
    keyboard3 = Keyboard().add(Text("Подробнее", {"brand": "shoes"}), color=KeyboardButtonColor.NEGATIVE)

    carousel = template_gen(
        TemplateElement(
            "Наш ассортимент обуви",
            "Чтобы продолжить нажми 'Подробнее' ",
            "-224358783_456239163",
            keyboard_shoes.get_json()
        ),
        TemplateElement(
            "Наш ассортимент одежды",
            "Чтобы продолжить нажми 'Подробнее'",
            "-224358783_456239163",
            keyboard_clothes.get_json()
        ),
        TemplateElement(
            "Товар-3",
            "2250 Р",
            "-224358783_456239163",
            keyboard3.get_json()
        )
    )

    await message.answer("Тут вы можете ознакомиться с ассортиментом предложенных нами товаров. ", template=carousel)

async def carouselback_handler(message: Message):
    keyboard = Keyboard(one_time=True)
    keyboard.add(Text("Назад", {"brand": "menu"}), color=KeyboardButtonColor.NEGATIVE)
    await message.answer(keyboard=keyboard)

@bot.on.message(payload={"brand": "shoes"})
async def shoes_handler(message: Message):
    keyboard = Keyboard(one_time=True)

    keyboard.add(Text("NewBalance", {"brand": "NewBalance"}), color=KeyboardButtonColor.PRIMARY)
    keyboard.row()
    keyboard.add(Text("Nike", {"brand": "Nike"}), color=KeyboardButtonColor.PRIMARY)
    keyboard.row()
    keyboard.add(Text("Adidas", {"brand": "Adidas"}), color=KeyboardButtonColor.PRIMARY)
    keyboard.row()
    keyboard.add(Text("Puma", {"brand": "Puma"}), color=KeyboardButtonColor.PRIMARY)
    keyboard.row()
    keyboard.add(Text("Reebok", {"brand": "Reebok"}), color=KeyboardButtonColor.PRIMARY)


    await message.answer("Выберите бренд:", keyboard=keyboard)

@bot.on.message(payload={"brand": "clothes"})
async def shoes_handler(message: Message):
    keyboard = Keyboard(one_time=True)

    keyboard.add(Text("Худи", {"brand": "NewBalance"}), color=KeyboardButtonColor.PRIMARY)
    keyboard.row()
    keyboard.add(Text("Футболки", {"brand": "Nike"}), color=KeyboardButtonColor.PRIMARY)
    keyboard.row()
    keyboard.add(Text("Свитеры", {"brand": "Adidas"}), color=KeyboardButtonColor.PRIMARY)
    keyboard.row()
    keyboard.add(Text("Кофты", {"brand": "Puma"}), color=KeyboardButtonColor.PRIMARY)
    keyboard.row()
    keyboard.add(Text("Куртки", {"brand": "Reebok"}), color=KeyboardButtonColor.PRIMARY)


    await message.answer("Выберите бренд:", keyboard=keyboard)

@bot.on.message(payload={"brand": "NewBalance"})
async def newbalance_handler(message: Message):

    keyboard574 = Keyboard().add(Text("Выбрать расцветку пары", {"brand": "colornb574"}), color=KeyboardButtonColor.NEGATIVE)
    keyboard327 = Keyboard().add(Text("Выбрать расцветку пары", {"brand": "сolornb327"}), color=KeyboardButtonColor.NEGATIVE)
    carousel = template_gen(
        TemplateElement(
            "New Balance 574",
            "Классическая обувь для спорта и активного отдыха",
            "-224358783_456239167",
            keyboard574.get_json()
        ),
        TemplateElement(
            "New Balance 327",
            "Для повседневного использования, не предназначены для спортивных целей.",
            "-224358783_456239169",
            keyboard327.get_json()
        )

    )
    await message.answer("Вы можете ознакомиться с брендом обуви NEW BALANCE. ", template=carousel)



@bot.on.message(payload={"brand": "Nike"})
async def nike_handler(message: Message):

    keyboard = Keyboard().add(Text("Оформить заказ", {"brand": "zakaz"}), color=KeyboardButtonColor.NEGATIVE)

    carousel = template_gen(
        TemplateElement(
            "Nike",
            "Стильная и удобная обувь для ежедневной носки",
            "-224358783_456239163",
            keyboard.get_json(),

        ),
        TemplateElement(
            "Nike",
            "Классическая обувь для спорта и активного отдыха",
            "-224358783_456239163",
            keyboard.get_json()
        )
    )
    await message.answer("Вы можете ознакомиться с брендом обуви NIKE. ", template=carousel)

# NEWBALANCE #

@bot.on.message(payload={"brand": "colornb574"})
async def newbalance_color_handler_574(message: Message):
    keyboard = Keyboard().add(Text("Перейти к выбору размера", {"brand": "size"}), color=KeyboardButtonColor.NEGATIVE)

    carousel = template_gen(
        TemplateElement(
            "New Balance 574",
            "Brown with royal blue",
            "-224358783_456239167",
            keyboard.get_json()
        ),
        TemplateElement(
            "New Balance 574",
            "Navy with green",
            "-224358783_456239168",
            keyboard.get_json()
        ),
        TemplateElement(
            "New Balance 574",
            "Black with grey",
            "-224358783_456239166",
            keyboard.get_json()
        )
    )

    await message.answer("В наличии находятся ниже представленные пары NEW BALANCE. ", template=carousel)

@bot.on.message(payload={"brand": "сolornb327"})
async def newbalance_color_handler_327(message: Message):
    keyboard = Keyboard().add(Text("Перейти к выбору размера", {"brand": "size"}), color=KeyboardButtonColor.NEGATIVE)



    carousel = template_gen(
        TemplateElement(
            "New Balance 327",
            "Brighton grey with slate grey",
            "-224358783_456239169",
            keyboard.get_json()
        ),
        TemplateElement(
            "New Balance 327",
            "Sea salt with moonrock",
            "-224358783_456239170",
            keyboard.get_json()
        ),
        TemplateElement(
            "New Balance 327",
            "Chrome blue with light chrome blue",
            "-224358783_456239171",
            keyboard.get_json()
        )
    )

    await message.answer("В наличии находятся ниже представленные пары NEW BALANCE 327. ", template=carousel)

@bot.on.message(payload={"brand": "size"})
async def size_handler(message: Message):
    keyboard = Keyboard(one_time=True)

    keyboard.add(Text("36-36.5", {"brand": "basket"}), color=KeyboardButtonColor.PRIMARY)
    keyboard.row()
    keyboard.add(Text("37-37.5", {"brand": "basket"}), color=KeyboardButtonColor.PRIMARY)
    keyboard.row()
    keyboard.add(Text("38-38.5", {"brand": "basket"}), color=KeyboardButtonColor.PRIMARY)
    keyboard.row()
    keyboard.add(Text("39-39.5", {"brand": "basket"}), color=KeyboardButtonColor.PRIMARY)
    keyboard.row()
    keyboard.add(Text("40-40.5", {"brand": "basket"}), color=KeyboardButtonColor.PRIMARY)
    keyboard.row()
    keyboard.add(Text("41-41.5", {"brand": "basket"}), color=KeyboardButtonColor.PRIMARY)
    keyboard.row()
    keyboard.add(Text("42-42.5", {"brand": "basket"}), color=KeyboardButtonColor.PRIMARY)
    keyboard.row()
    keyboard.add(Text("44-44.5", {"brand": "basket"}), color=KeyboardButtonColor.PRIMARY)

    await message.answer("Выберите размер:", keyboard=keyboard)

@bot.on.message(payload={"brand": "basket"})
async def basket(message: Message):
    keyboard = Keyboard(one_time=True)

    await message.answer("Удачно добавленно в корзину", keyboard=keyboard)



bot.run_forever()

