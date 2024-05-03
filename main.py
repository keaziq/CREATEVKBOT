from geopy import Location
from vkbottle import Keyboard, KeyboardButtonColor, Text, template_gen, TemplateElement, BaseStateGroup, CtxStorage, \
    OpenLink, Location
from vkbottle.bot import Bot, Message

from config import *

bot = Bot(token=token)
ctx = CtxStorage()

hello = ["Привет","привет", 'start', 'Хай','хай', 'Ку-ку', 'здарова','Здарова',
         'Здраствуйте','здраствуйте', 'Здраствуй','здраствуй']

class Database(BaseStateGroup):

    NAME = 0
    AGE = 1
    ABOUT = 2

@bot.on.message(text=hello)
@bot.on.message(payload={"cmd": "hello"})
async def message_welcome(message: Message):
    keyboard = Keyboard(inline=True)
    keyboard.add(Text(f"Меню", {"cmd": "menu"}), color=KeyboardButtonColor.PRIMARY)
    # keyboard.add(Text(f"Оформить заказ", {"cmd": "zakaz"}), color=KeyboardButtonColor.PRIMARY)
    # keyboard.row()
    # keyboard.row()
    # keyboard.add(Text("Задать вопрос", {"cmd": "Задать вопрос"}), color=KeyboardButtonColor.SECONDARY)
    user = await bot.api.users.get(message.from_id)
    await message.answer(f" Здраствуйте  , {user[0].first_name}."
                         f" Что вы хотите сделать сегодня?", keyboard=keyboard)

@bot.on.message(text="меню")
@bot.on.message(payload={"cmd": "menu"})
async def menu(message: Message):
    keyboard = Keyboard(one_time=True)

    keyboard.add(Text(f"Посмотреть ассортимент товаров", {"cmd": "assortment"}), color=KeyboardButtonColor.PRIMARY)
    keyboard.row()
    keyboard.add(Text("Развлечение", {"cmd": "Развлечение"}), color=KeyboardButtonColor.SECONDARY)
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





@bot.on.message(payload={"cmd": "assortment"})
async def carousel_handler(message: Message):

    keyboard = Keyboard().add(Text("Подробнее", {"cmd": "shoes"}), color=KeyboardButtonColor.SECONDARY)
    keyboard2 = Keyboard().add(Text("Подробнее", {"cmd": "shoes"}), color=KeyboardButtonColor.SECONDARY)
    keyboard3 = Keyboard().add(Text("Подробнее", {"cmd": "shoes"}), color=KeyboardButtonColor.NEGATIVE)

    carousel = template_gen(
        TemplateElement(
            "Наш ассортимент обуви",
            "Просмотрите бренды обуви",
            "-224358783_456239163",
            keyboard.get_json()
        ),
        TemplateElement(
            "Товар-2",
            "1250 Р",
            "-224358783_456239163",
            keyboard2.get_json()
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
    keyboard.add(Text("Назад", {"cmd": "menu"}), color=KeyboardButtonColor.NEGATIVE)
    await message.answer(keyboard=keyboard)

@bot.on.message(payload={"cmd": "shoes"})
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

@bot.on.message(payload={"brand": "NewBalance"})
async def newbalance_handler(message: Message):

    keyboard = Keyboard().add(Text("Оформить заказ", {"cmd": "zakaz"}), color=KeyboardButtonColor.NEGATIVE)

    carousel = template_gen(
        TemplateElement(
            "New Balance 327",
            "Стильная и удобная обувь для ежедневной носки",
            "-224358783_456239163",
            keyboard.get_json(),

        ),
        TemplateElement(
            "New Balance 574",
            "Классическая обувь для спорта и активного отдыха",
            "-224358783_456239163",
            keyboard.get_json()
        )
    )
    await message.answer("Вы можете ознакомиться с брендом обуви NEW BALANCE. ", template=carousel)

@bot.on.message(payload={"brand": "Nike"})
async def newbalance_handler(message: Message):

    keyboard = Keyboard().add(Text("Оформить заказ", {"cmd": "zakaz"}), color=KeyboardButtonColor.NEGATIVE)

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
bot.run_forever()
