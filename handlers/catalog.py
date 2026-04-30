"""
handlers/catalog.py — Каталог товаров ShopBot.

Обрабатывает команду /catalog и inline-callback-и:
  cat_<key>   — список товаров выбранной категории
  prod_<id>   — карточка конкретного товара
  cat_back_<id> — возврат к категории из карточки товара
"""
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from data import CATEGORIES, PRODUCTS, get_product_by_id, format_price

router = Router()


def categories_kb() -> InlineKeyboardMarkup:
    """Клавиатура со списком всех категорий каталога."""
    buttons = [
        [InlineKeyboardButton(text=name, callback_data=f"cat_{key}")]
        for key, name in CATEGORIES.items()
    ]
    buttons.append([InlineKeyboardButton(text="🏠 Главная", callback_data="main_menu")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def products_kb(category: str, products: list[dict]) -> InlineKeyboardMarkup:
    """Клавиатура со списком товаров заданной категории.

    Args:
        category: Ключ категории (используется для формирования callback_data).
        products: Список словарей товаров из data.PRODUCTS.
    """
    buttons = [
        [InlineKeyboardButton(
            text=f"{p['emoji']} {p['name']} — {format_price(p['price'])}",
            callback_data=f"prod_{p['id']}"
        )]
        for p in products
    ]
    buttons.append([InlineKeyboardButton(text="◀️ Категории", callback_data="catalog")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def product_kb(product_id: str) -> InlineKeyboardMarkup:
    """Клавиатура карточки товара: добавить в корзину, назад, главная.

    Args:
        product_id: Уникальный идентификатор товара.
    """
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="🛒 Добавить в корзину", callback_data=f"add_{product_id}"),
        ],
        [
            InlineKeyboardButton(text="◀️ Назад", callback_data=f"cat_back_{product_id}"),
            InlineKeyboardButton(text="🏠 Главная", callback_data="main_menu"),
        ],
    ])


def _get_category_for_product(product_id: str) -> str | None:
    """Находит ключ категории, к которой принадлежит товар.

    Args:
        product_id: Уникальный идентификатор товара.

    Returns:
        Ключ категории из PRODUCTS или None, если товар не найден.
    """
    for cat_key, products in PRODUCTS.items():
        for p in products:
            if p["id"] == product_id:
                return cat_key
    return None


@router.message(Command("catalog"))
async def cmd_catalog(message: Message) -> None:
    """Обрабатывает команду /catalog — открывает список категорий."""
    await message.answer(
        "📦 <b>Каталог товаров</b>\n\nВыберите категорию:",
        reply_markup=categories_kb()
    )


@router.callback_query(F.data == "catalog")
async def cb_catalog(callback: CallbackQuery) -> None:
    """Возврат к списку категорий через inline-кнопку."""
    await callback.message.edit_text(
        "📦 <b>Каталог товаров</b>\n\nВыберите категорию:",
        reply_markup=categories_kb()
    )


@router.callback_query(F.data.startswith("cat_") & ~F.data.startswith("cat_back_"))
async def cb_category(callback: CallbackQuery) -> None:
    """Показывает товары выбранной категории (callback: cat_<key>)."""
    category = callback.data[4:]  # убираем "cat_"
    if category not in PRODUCTS:
        await callback.answer("Категория не найдена")
        return
    products = PRODUCTS[category]
    cat_name = CATEGORIES[category]
    await callback.message.edit_text(
        f"{cat_name}\n\n"
        f"Найдено товаров: <b>{len(products)}</b>\n"
        "Нажмите на товар для подробностей 👇",
        reply_markup=products_kb(category, products)
    )


@router.callback_query(F.data.startswith("prod_"))
async def cb_product(callback: CallbackQuery) -> None:
    """Показывает карточку товара (callback: prod_<id>)."""
    product_id = callback.data[5:]
    product = get_product_by_id(product_id)
    if not product:
        await callback.answer("Товар не найден")
        return

    stars = "⭐" * int(product["rating"]) + ("½" if product["rating"] % 1 >= 0.5 else "")
    stock_text = f"✅ В наличии ({product['stock']} шт.)" if product["stock"] > 0 else "❌ Нет в наличии"

    text = (
        f"{product['emoji']} <b>{product['name']}</b>\n\n"
        f"📝 {product['desc']}\n\n"
        f"💰 Цена: <b>{format_price(product['price'])}</b>\n"
        f"⭐ Рейтинг: {product['rating']} / 5.0\n"
        f"📦 {stock_text}"
    )
    await callback.message.edit_text(text, reply_markup=product_kb(product_id))


@router.callback_query(F.data.startswith("cat_back_"))
async def cb_back_to_category(callback: CallbackQuery) -> None:
    """Возврат к списку товаров категории из карточки товара (callback: cat_back_<id>)."""
    product_id = callback.data[9:]
    category = _get_category_for_product(product_id)
    if not category:
        await callback.answer("Ошибка")
        return
    products = PRODUCTS[category]
    cat_name = CATEGORIES[category]
    await callback.message.edit_text(
        f"{cat_name}\n\nНайдено товаров: <b>{len(products)}</b>",
        reply_markup=products_kb(category, products)
    )
