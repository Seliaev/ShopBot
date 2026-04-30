"""
handlers/checkout.py — Оформление заказа через FSM.

Шаги диалога:
  1. checkout        — подтверждение состава корзины, переход в CheckoutForm.name
  2. Имя              — свободный ввод (мин. 2 символа), переход в CheckoutForm.phone
  3. Телефон         — валидация regex, переход в CheckoutForm.address
  4. Адрес          — свободный ввод (мин. 10 символов), переход в CheckoutForm.confirm
  5. confirm_order   — подтверждение заказа и сброс FSM/корзины
"""
import re
import random
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from states import CheckoutForm
from handlers.cart import get_cart, save_cart, format_cart_text
from data import format_price

router = Router()

CANCEL_KB = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="❌ Отменить", callback_data="cancel_checkout")]
])


@router.callback_query(F.data == "checkout")
async def cb_checkout_start(callback: CallbackQuery, state: FSMContext) -> None:
    """Запускает FSM-диалог оформления. Проверяет, что корзина не пуста."""
    cart = await get_cart(state)
    if not cart:
        await callback.answer("Корзина пуста!", show_alert=True)
        return

    text, total = format_cart_text(cart)
    await state.set_state(CheckoutForm.name)
    await callback.message.edit_text(
        f"{text}\n\n"
        "━━━━━━━━━━━━━━━━━━\n"
        "📋 <b>Оформление заказа</b>\n\n"
        "Шаг 1/3 — Введите ваше <b>имя и фамилию</b>:",
        reply_markup=CANCEL_KB
    )


@router.message(CheckoutForm.name)
async def checkout_name(message: Message, state: FSMContext) -> None:
    """Принимает имя пользователя (шаг 1/3), переходит к запросу телефона."""
    if len(message.text.strip()) < 2:
        await message.answer("❌ Слишком короткое имя. Попробуйте ещё раз:", reply_markup=CANCEL_KB)
        return

    await state.update_data(name=message.text.strip())
    await state.set_state(CheckoutForm.phone)
    await message.answer(
        f"✅ Имя: <b>{message.text.strip()}</b>\n\n"
        "Шаг 2/3 — Введите номер <b>телефона</b>:\n"
        "Формат: +7 (999) 123-45-67",
        reply_markup=CANCEL_KB
    )


@router.message(CheckoutForm.phone)
async def checkout_phone(message: Message, state: FSMContext) -> None:
    """Принимает телефон (regex-валидация, шаг 2/3), переходит к запросу адреса."""
    phone = message.text.strip()
    # Проверяем формат телефона
    cleaned = re.sub(r"[\s\-\(\)]", "", phone)
    if not re.match(r"^[\+7|8]\d{10}$", cleaned):
        await message.answer(
            "❌ Неверный формат телефона.\n"
            "Пример: +7 999 123-45-67",
            reply_markup=CANCEL_KB
        )
        return

    await state.update_data(phone=phone)
    await state.set_state(CheckoutForm.address)
    await message.answer(
        f"✅ Телефон: <b>{phone}</b>\n\n"
        "Шаг 3/3 — Введите <b>адрес доставки</b>:\n"
        "Например: г. Москва, ул. Тверская, д. 1, кв. 5",
        reply_markup=CANCEL_KB
    )


@router.message(CheckoutForm.address)
async def checkout_address(message: Message, state: FSMContext) -> None:
    """Принимает адрес (шаг 3/3) и выводит экран подтверждения."""
    if len(message.text.strip()) < 10:
        await message.answer(
            "❌ Слишком короткий адрес. Укажите полный адрес:",
            reply_markup=CANCEL_KB
        )
        return

    await state.update_data(address=message.text.strip())
    data = await state.get_data()
    cart = data.get("cart", {})
    _, total = format_cart_text(cart)

    confirm_kb = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="✅ Подтвердить заказ", callback_data="confirm_order"),
            InlineKeyboardButton(text="❌ Отменить", callback_data="cancel_checkout"),
        ]
    ])

    await state.set_state(CheckoutForm.confirm)
    await message.answer(
        "📋 <b>Проверьте данные заказа</b>\n\n"
        f"👤 Имя: <b>{data['name']}</b>\n"
        f"📱 Телефон: <b>{data['phone']}</b>\n"
        f"📍 Адрес: <b>{data['address']}</b>\n"
        f"💰 К оплате: <b>{format_price(total)}</b>\n\n"
        "Всё верно?",
        reply_markup=confirm_kb
    )


@router.callback_query(F.data == "confirm_order", CheckoutForm.confirm)
async def cb_confirm_order(callback: CallbackQuery, state: FSMContext) -> None:
    """Подтверждает заказ: очищает корзину, сбрасывает FSM, показывает экран успеха."""
    order_id = random.randint(10000, 99999)
    data = await state.get_data()

    # Очищаем корзину и состояние
    await save_cart(state, {})
    await state.clear()

    await callback.message.edit_text(
        f"🎉 <b>Заказ #{order_id} оформлен!</b>\n\n"
        f"👤 Получатель: {data['name']}\n"
        f"📱 Телефон: {data['phone']}\n"
        f"📍 Адрес: {data['address']}\n\n"
        "📦 Статус: <b>Принят в обработку</b>\n"
        "🚚 Ожидаемая доставка: 3-5 рабочих дней\n\n"
        "Мы позвоним вам для подтверждения заказа.\n"
        "Спасибо за покупку! ❤️",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🛍 Продолжить покупки", callback_data="catalog")],
            [InlineKeyboardButton(text="🏠 Главная", callback_data="main_menu")],
        ])
    )


@router.callback_query(F.data == "cancel_checkout")
async def cb_cancel_checkout(callback: CallbackQuery, state: FSMContext) -> None:
    """Отменяет оформление заказа, сбрасывает FSM, корзина остаётся нетронутой."""
    await state.clear()
    await callback.message.edit_text(
        "❌ Оформление отменено\n\nВаша корзина сохранена.",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🛒 Корзина", callback_data="cart")],
            [InlineKeyboardButton(text="🏠 Главная", callback_data="main_menu")],
        ])
    )
