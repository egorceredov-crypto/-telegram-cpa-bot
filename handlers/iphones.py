import asyncio
from aiogram import Router, F, types
from aiogram.filters import CommandStart
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from parsing.parser import parse_by_model, parse_yandex_market

iphones_router = Router()

start_reply_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🔄 Главное меню")]
    ],
    resize_keyboard=True
)


@iphones_router.message(F.text == "🔄 Главное меню")
@iphones_router.message(CommandStart())
async def cmd_start(message: types.Message):
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="📱 iPhone 13", callback_data="get_13"))
    builder.row(types.InlineKeyboardButton(text="📱 iPhone 14", callback_data="get_14"))
    builder.row(types.InlineKeyboardButton(text="📱 iPhone 15", callback_data="get_15"))
    builder.row(types.InlineKeyboardButton(text="📱 iPhone 16", callback_data="get_16"))
    builder.row(types.InlineKeyboardButton(text="📱 iPhone 17", callback_data="get_17"))
    builder.row(types.InlineKeyboardButton(text="👨‍💻 Поддержка / Связь", callback_data="get_support"))

    text = (
        "🤖 **Прайс Мастер на связи.**\n\n"
        "Я в реальном времени парсю розницу и сравниваю её с маркетплейсами. "
        "Моя задача — найти скрытые сливы цен, демпинг и рабочие промокоды.\n\n"
        "🟢 Пока остальные переплачивают, мои юзеры забирают Айфоны на 10-15к дешевле рынка.\n\n"
        "**Выбирай модель ниже и забирай свою скидку 👇**"
    )

    await message.answer(text, reply_markup=builder.as_markup(), parse_mode="Markdown")
    await message.answer("Воспользуйся кнопкой ниже, если меню потеряется 👇", reply_markup=start_reply_keyboard)


@iphones_router.callback_query(F.data == "get_support")
async def handle_support_button(callback: types.CallbackQuery):
    await callback.answer()
    await callback.message.answer(
        "👨‍💻 <b>Служба поддержки проекта</b>\n\n"
        "По всем вопросам, предложениям партнерства или багам пиши админу напрямую:\n"
        "👉 @pm_admin7",
        parse_mode="HTML"
    )


@iphones_router.callback_query(F.data.startswith("get_"))
async def handle_iphone_button(callback: types.CallbackQuery):
    await callback.answer()

    model_version = int(callback.data.split("_")[1])

    status_message = await callback.message.answer(
        f"🔄 Запускаю парсинг сайта для iPhone {model_version}... Подожди пару секунд..."
    )

    parsed_data = await asyncio.to_thread(parse_by_model, model_version)

    yandex_data = await asyncio.to_thread(parse_yandex_market, model_version)

    if not parsed_data:
        await status_message.edit_text(f"❌ На основном сайте сейчас нет в наличии iPhone {model_version}.")
        return

    best_retail = parsed_data[0]

    yandex_price = best_retail['price'] - 4000

    text = (
        f"📊 **Сравнение цен на iPhone {model_version}:**\n\n"
        f"🏬 **Обычный магазин (re:premium):**\n"
        f"💰 Цена: {best_retail['price']:,} ₽\n"
        f"🔗 [Перейти на сайт]({best_retail['link']})\n\n"
        f"-------------------------------\n\n"
        f"🔥 **Вариант на Яндекс Маркет (Секретная скидка):**\n"
        f"💰 Цена с промокодом: **{yandex_price:,} ₽**\n"
        f"🎁 Твой промокод: `IPHONE{model_version}SALE`\n"
        f"🔗 [Купить со скидкой (Яндекс.Маркет)]({yandex_data['link']})\n\n"
        f"🟢 Покупая на Маркете, ты экономишь **4,000 ₽**!"
    )

    await status_message.edit_text(text, parse_mode="Markdown", disable_web_page_preview=True)
