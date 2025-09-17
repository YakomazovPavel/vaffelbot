import uuid
from aiogram import Bot as TGBot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode, MenuButtonType
from aiogram.types import (
    Message,
    InlineQueryResultArticle,
    InputTextMessageContent,
    InlineQueryResultsButton,
    WebAppInfo,
    MenuButtonWebApp,
    InlineQueryResultPhoto,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from aiogram.types.inline_query import InlineQuery
from aiogram.filters.command import Command
from aiogram.methods.set_chat_menu_button import SetChatMenuButton
import asyncio
from os import getenv
from dotenv import load_dotenv
from aiogram.client.session.aiohttp import AiohttpSession

# from aiogram.methods import SavePreparedInlineMessage
import os
from storage import storage

PHOTO_URL = "https://raw.githubusercontent.com/YakomazovPavel/YakomazovPavel.github.io/main/public/assets/"
BASKET_URL = "https://t.me/vaffel2_bot/vaffel?startapp="
BOT_URL = "https://t.me/vaffel2_bot/vaffel"

# baskets = [
#     {
#         "id": "1",
#         "name": "Посиделки 2 ноября",
#         "photo": "https://raw.githubusercontent.com/YakomazovPavel/YakomazovPavel.github.io/main/public/assets/1.jpg",
#         "link": "https://t.me/vaffel2_bot/vaffel?startapp=1",  # "https://t.me/vaffel2_bot/start?startapp=123",
#     },
#     {
#         "id": "2",
#         "name": "Хеллоуин",
#         "photo": "https://raw.githubusercontent.com/YakomazovPavel/YakomazovPavel.github.io/main/public/assets/2.jpg",
#         "link": "https://t.me/vaffel2_bot/vaffel?startapp=1",  # Рабочая ссылка на приложение
#     },
#     {
#         "id": "3",
#         "name": "Тыквенный спас",
#         "photo": "https://raw.githubusercontent.com/YakomazovPavel/YakomazovPavel.github.io/main/public/assets/3.jpg",
#         "link": "https://t.me/vaffel2_bot/vaffel?startapp=1",
#     },
#     {
#         "id": "19",
#         "name": "Отчаяние",
#         "photo": "https://raw.githubusercontent.com/YakomazovPavel/YakomazovPavel.github.io/main/public/assets/4.jpg",
#         "link": "https://t.me/vaffel2_bot/vaffel?startapp=1",
#     },
# ]

photo_bota = "https://raw.githubusercontent.com/YakomazovPavel/YakomazovPavel.github.io/main/public/assets/icon.jpg"

# https://yakomazovpavel.github.io/vaffel/dist/index.html


# photo_url = "https://photos.app.goo.gl/eLKpTjxezmHXAcWQA"
# photo_url = "https://img.freepik.com/free-photo/shopping-basket-on-white_93675-130677.jpg?size=626&ext=jpg"
# photo_url =


bot_self_link = "https://t.me/yakomazov_bot?profile"
bot_self_link_start = "https://t.me/vaffel2_bot/start?startapp=123"


class Bot:
    def __init__(self, token: str, url: str, session) -> None:
        self.bot = TGBot(
            token=token,
            default=DefaultBotProperties(parse_mode=ParseMode.HTML),
            session=session,
        )

        self.dp = Dispatcher()
        self.url = url

        @self.dp.inline_query()
        async def inline_handler(query: InlineQuery):
            print("query", query)

            baskets = storage.get_inline_baskets(
                telegram_id=query.from_user.id,
                basket_name=query.query,
            )

            photos = [
                InlineQueryResultPhoto(
                    id=str(basket.id),
                    photo_url=PHOTO_URL + str(basket.photo_url),
                    thumbnail_url=PHOTO_URL + str(basket.photo_url),
                    title=basket.name,
                    # description=str(basket.id),
                    caption=f'Добавляйте свои вафли в совместную корзину "{basket.name}"',
                    reply_markup=InlineKeyboardMarkup(
                        inline_keyboard=[
                            [
                                InlineKeyboardButton(
                                    text="Добавить",
                                    url=BASKET_URL + str(basket.id),
                                )
                            ]
                        ]
                    ),
                )
                for basket in baskets
            ]

            article = InlineQueryResultArticle(
                id="0",
                title="Поделиться ботом",
                thumbnail_url=photo_bota,
                description="Пригласите друзей с помощью реферальной ссылки",
                input_message_content=InputTextMessageContent(
                    message_text="Переходи в бота, чтобы создавать, делиться и заказывать свои корзины с вафлями от vaffel.ru"
                ),
                reply_markup=InlineKeyboardMarkup(
                    inline_keyboard=[
                        [
                            InlineKeyboardButton(
                                text="Добавить",
                                url=BOT_URL,
                            )
                        ]
                    ]
                ),
            )

            # photos = [
            #     InlineQueryResultPhoto(
            #         id=basket.get("id"),
            #         photo_url=basket.get("photo"),
            #         thumbnail_url=basket.get("photo"),
            #         title=basket.get("name"),
            #         description=basket.get("id"),
            #         caption="Добавляем свои вафельки сюда",
            #         reply_markup=InlineKeyboardMarkup(
            #             inline_keyboard=[
            #                 [
            #                     InlineKeyboardButton(
            #                         text="Добавить",
            #                         url=basket.get("link"),
            #                     )
            #                 ]
            #             ]
            #         ),
            #     )
            #     for basket in baskets
            # ]

            # photo = InlineQueryResultPhoto(
            #     id="1",
            #     photo_url=photo_url,
            #     # photo_url="http://192.168.1.9/1.jpg",
            #     # thumbnail_url="https://img.freepik.com/free-photo/shopping-basket-on-white_93675-130677.jpg?size=626&ext=jpg",
            #     thumbnail_url=photo_url,
            #     title="Посиделки 2 ноября",
            #     description="#1",
            #     # caption="Добавляем свои вафельки сюда!\nhttps://t.me/yakomazov_bot/start?startapp=123",
            #     caption=f"Добавляем свои вафельки сюда!\n{bot_self_link}",
            #     reply_markup=InlineKeyboardMarkup(
            #         inline_keyboard=[
            #             [
            #                 InlineKeyboardButton(
            #                     text="Добавить вафель",
            #                     url=bot_self_link_start,
            #                     # login_url=LoginUrl(
            #                     #     url=BOT_DOMAIN,
            #                     # )
            #                     # web_app=WebAppInfo(url=WEB_APP_URL)
            #                 )
            #             ]
            #         ]
            #     ),
            #     # photo_width
            #     # photo_height
            # )

            button = InlineQueryResultsButton(
                # start_parameter="123",
                text="Создать корзину",
                web_app=WebAppInfo(url=self.url),
            )

            await query.answer(
                results=[*photos, article],
                button=button,
                cache_time=1,
                is_personal=True,
                # results=photos, button=button, cache_time=1, is_personal=True
            )

        @self.dp.message(Command("start"))
        async def start(message: Message) -> None:
            print("user", message.from_user)
            await self.bot(
                SetChatMenuButton(
                    chat_id=message.chat.id,
                    menu_button=MenuButtonWebApp(
                        type=MenuButtonType.WEB_APP,
                        text="Меню",
                        web_app=WebAppInfo(url=self.url),
                    ),
                )
            )

            await message.answer(
                f'Привет, {message.from_user.full_name}!  \nПереходи в меню, чтобы создавать, делиться и заказывать свои корзины с вафлями от <a href="https://vaffel.ru/">vaffel.ru</a>',
                parse_mode="HTML",
            )

        @self.dp.message(Command("prepare"))
        async def prepare(message: Message) -> None:
            print(f"user_id {message.from_user.id}")
            res = await self.bot.save_prepared_inline_message(
                user_id=message.from_user.id,
                result=InlineQueryResultPhoto(
                    id=str(uuid.uuid4()),
                    photo_url="https://raw.githubusercontent.com/YakomazovPavel/YakomazovPavel.github.io/main/public/assets/2.jpg",
                    thumbnail_url="https://raw.githubusercontent.com/YakomazovPavel/YakomazovPavel.github.io/main/public/assets/2.jpg",
                    title="title",
                    description="description",
                    caption="Добавляем свои вафельки сюда",
                    reply_markup=InlineKeyboardMarkup(
                        inline_keyboard=[
                            [
                                InlineKeyboardButton(
                                    text="Добавить",
                                    url="https://t.me/vaffel2_bot/vaffel?startapp=1",
                                )
                            ]
                        ]
                    ),
                ),
                #
                allow_bot_chats=True,
                allow_channel_chats=True,
                allow_group_chats=True,
                allow_user_chats=True,
            )

            print(res)
            await message.answer("prepare создан")

    async def start(self) -> None:
        print("start bot")
        # await self.bot.set_my_name(name="Vaffel")
        # # await bot.set_my_short_description(short_description="my_short_description")
        # await self.bot.set_my_description(
        #     description="Создавайте и делитесь корзинами, для совместного заказа норвежских вафель от Vaffel"
        # )
        await self.dp.start_polling(self.bot, skip_updates=True)


directory, filename = os.path.split(os.path.abspath(__file__))
PATH_TO_ENV = os.path.join(directory, ".env")

load_dotenv(PATH_TO_ENV)
TELEGRAM_BOT_TOKEN = getenv("TELEGRAM_BOT_TOKEN")
WEB_APP_URL = getenv("WEB_APP_URL")
HTTP_PROXY = getenv("http_proxy")

print(f"""
========================================================================================================================

PATH_TO_ENV         {PATH_TO_ENV}
TELEGRAM_BOT_TOKEN  {TELEGRAM_BOT_TOKEN}
WEB_APP_URL         {WEB_APP_URL}
HTTP_PROXY          {HTTP_PROXY}

========================================================================================================================
""")


session = None
if HTTP_PROXY:
    session = AiohttpSession(proxy=HTTP_PROXY)
bot = Bot(token=TELEGRAM_BOT_TOKEN, url=WEB_APP_URL, session=session)

if __name__ == "__main__":

    async def main():
        await bot.start()

    asyncio.run(main())
