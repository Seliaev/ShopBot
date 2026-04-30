"""
handlers/cart.py — Корзина пользователя ShopBot.

Данные корзины хранятся в FSMContext под ключом CART_KEY.
Структура: {product_id: quantity}.
"""
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from data import get_product_by_id, format_price

router = Router()

# Корзина хранится в FSMContext (state data)
CART_KEY = "cart"


async def get_cart(state: FSMContext) -> dict[str, int]:
    """Извлекает текущую корзину из FSMContext.

    Returns:
        Словарь {product_id: quantity} или пустой dict, если корзина пуста.
    """
    data = await state.get_data()
    return data.get(CART_KEY, {})


async def save_cart(state: FSMContext, cart: dict[str, int]) -> None:
    """Сохраняет корзину в FSMContext.

    Args:
        state: Текущий FSM-контекст пользователя.
        cart: Словарь {product_id: quantity}.
    """
    await state.update_data({CART_KEY: cart})


def cart_kb(cart: dict[str, int]) -> InlineKeyboardMarkup:
    """Генерирует клавиатуру корзины: кнопка удаления для каждого товара, очистка и оформление."""
    buttons = []
    for product_id in cart:
        product = get_product_by_id(product_id)
        if product:
            buttons.append([
                InlineKeyboardButton(
                    text=f"❌ {product['name']}",
                    callback_data=f"remove_{product_id}"
                )
            ])
    buttons.append([
        InlineKeyboardButton(text="🗑 Очистить", callback_data="clear_cart"),
        InlineKeyboardButton(text="✅ Оформить", callback_data="checkout"),
    ])
    buttons.append([InlineKeyboardButton(text="📦 Каталог", callback_data="catalog")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def format_cart_text(cart: dict[str, int]) -> tuple[str, int]:
    """Возвращает (текст корзины, итого)"""
    if not cart:
        return "🛒 Ваша корзина пуста\n\nПерейдите в каталог, чтобы добавить товары!", 0

    lines = ["🛒 <b>Ваша корзина</b>\n"]
    total = 0
    for product_id, qty in cart.items():
        product = get_product_by_id(product_id)
        if product:
            subtotal = product["price"] * qty
            total += subtotal
            lines.append(
                f"{product['emoji']} {product['name']}\n"
                f"   {qty} × {format_price(product['price'])} = {format_price(subtotal)}"
            )

    lines.append(f"\n💰 <b>Итого: {format_price(total)}</b>")
    lines.append("🚚 Доставка рассчитывается при оформлении")
    return "\n".join(lines), total


@router.message(Command("cart"))
async def cmd_cart(message: Message, state: FSMContext) -> None:
    """Обрабатывает команду /cart — показывает содержимое корзины."""
    cart = await get_cart(state)
    text, total = format_cart_text(cart)
    if cart:
        await message.answer(text, reply_markup=cart_kb(cart))
    else:
        await message.answer(
            text,
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="📦 В каталог", callback_data="catalog")]
            ])
        )


@router.callback_query(F.data == "cart")
async def cb_cart(callback: CallbackQuery, state: FSMContext) -> None:
    """Отображает корзину через inline-кнопку."""
    cart = await get_cart(state)
    text, total = format_cart_text(cart)
    if cart:
        await callback.message.edit_text(text, reply_markup=cart_kb(cart))
    else:
        await callback.message.edit_text(
            text,
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="📦 В каталог", callback_data="catalog")],
                [InlineKeyboardButton(text="🏠 Главная", callback_data="main_menu")],
            ])
        )


@router.callback_query(F.data.startswith("add_"))
async def cb_add_to_cart(callback: CallbackQuery, state: FSMContext) -> None:
    """Добавляет товар в корзину (callback: add_<product_id>). Проверяет наличие."""
    product_id = callback.data[4:]
    product = get_product_by_id(product_id)
    if not product:
        await callback.answer("Товар не найден", show_alert=True)
        return
    if product["stock"] == 0:
        await callback.answer("❌ Товар закончился!", show_alert=True)
        return

    cart = await get_cart(state)
    cart[product_id] = cart.get(product_id, 0) + 1
    await save_cart(state, cart)

    total_items = sum(cart.values())
    await callback.answer(
        f"✅ {product['name']} добавлен в корзину!\nВ корзине: {total_items} товаров",
        show_alert=True
    )


@router.callback_query(F.data.startswith("remove_"))
async def cb_remove_from_cart(callback: CallbackQuery, state: FSMContext) -> None:
    """Удаляет позицию из корзины (callback: remove_<product_id>)."""
    product_id = callback.data[7:]
    cart = await get_cart(state)

    if product_id in cart:
        del cart[product_id]
        await save_cart(state, cart)

    text, total = format_cart_text(cart)
    if cart:
        await callback.message.edit_text(text, reply_markup=cart_kb(cart))
    else:
        await callback.message.edit_text(
            text,
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="📦 В каталог", callback_data="catalog")],
                [InlineKeyboardButton(text="🏠 Главная", callback_data="main_menu")],
            ])
        )


@router.callback_query(F.data == "clear_cart")
async def cb_clear_cart(callback: CallbackQuery, state: FSMContext) -> None:
    """Полностью очищает корзину."""
    await save_cart(state, {})
    await callback.message.edit_text(
        "🗑 Корзина очищена",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="📦 В каталог", callback_data="catalog")],
            [InlineKeyboardButton(text="🏠 Главная", callback_data="main_menu")],
        ])
    )
