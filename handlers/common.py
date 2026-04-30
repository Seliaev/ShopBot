"""Хендлеры: /start, /help, главное меню"""
from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

router = Router()

MAIN_MENU_KB = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="📦 Каталог", callback_data="catalog"),
        InlineKeyboardButton(text="🛒 Корзина", callback_data="cart"),
    ],
    [
        InlineKeyboardButton(text="ℹ️ О магазине", callback_data="about"),
        InlineKeyboardButton(text="📞 Поддержка", callback_data="support"),
    ],
])

WELCOME_TEXT = (
    "👋 Добро пожаловать в <b>⚡ TechStore</b>!\n\n"
    "Здесь вы найдёте топовую электронику по лучшим ценам:\n"
    "• 📱 Смартфоны\n"
    "• 💻 Ноутбуки\n"
    "• 🎧 Аудио\n"
    "• 🔌 Аксессуары\n\n"
    "Выберите раздел ниже 👇"
)


@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(WELCOME_TEXT, reply_markup=MAIN_MENU_KB)


@router.message(Command("help"))
async def cmd_help(message: Message):
    await message.answer(
        "🆘 <b>Помощь</b>\n\n"
        "Команды:\n"
        "/start — главное меню\n"
        "/catalog — каталог товаров\n"
        "/cart — ваша корзина\n"
        "/help — эта справка\n\n"
        "По вопросам: @techstore_support",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🏠 На главную", callback_data="main_menu")]
        ])
    )


@router.callback_query(F.data == "main_menu")
async def cb_main_menu(callback: CallbackQuery):
    await callback.message.edit_text(WELCOME_TEXT, reply_markup=MAIN_MENU_KB)


@router.callback_query(F.data == "about")
async def cb_about(callback: CallbackQuery):
    await callback.message.edit_text(
        "ℹ️ <b>О магазине TechStore</b>\n\n"
        "🏪 Работаем с 2020 года\n"
        "📦 Более 500 товаров в наличии\n"
        "🚚 Доставка по всей России 2-5 дней\n"
        "🔄 Возврат в течение 14 дней\n"
        "⭐ Гарантия 1 год на все товары\n\n"
        "📍 Офис: Москва, ул. Тверская, 1\n"
        "🕒 Пн–Пт 10:00–20:00",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="◀️ Назад", callback_data="main_menu")]
        ])
    )


@router.callback_query(F.data == "support")
async def cb_support(callback: CallbackQuery):
    await callback.message.edit_text(
        "📞 <b>Поддержка</b>\n\n"
        "Мы всегда готовы помочь!\n\n"
        "💬 Telegram: @techstore_support\n"
        "📧 Email: support@techstore.ru\n"
        "📱 Телефон: +7 (800) 555-35-35\n"
        "🕒 Время работы: 9:00–21:00\n\n"
        "Среднее время ответа: <b>15 минут</b>",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="◀️ Назад", callback_data="main_menu")]
        ])
    )
