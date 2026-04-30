# 🛒 ShopBot — Telegram Bot для интернет-магазина

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![aiogram](https://img.shields.io/badge/aiogram-3.x-2CA5E0?style=flat-square&logo=telegram&logoColor=white)](https://docs.aiogram.dev)
[![SQLite](https://img.shields.io/badge/SQLite-3-003B57?style=flat-square&logo=sqlite&logoColor=white)](https://sqlite.org)

Демонстрационный Telegram-бот интернет-магазина электроники. Каталог товаров, корзина, оформление заказа — всё через чат.

🤖 **Демо-бот:** [@Portfolio_1_Shop_Bot](https://t.me/Portfolio_1_Shop_Bot)

---

## ✨ Возможности

- 🗂 **Каталог** — товары сгруппированы по категориям с фото и описанием
- 🛒 **Корзина** — добавление, изменение количества, удаление
- 📦 **Оформление заказа** — пошаговый диалог через FSM (имя, телефон, адрес)
- 🔔 **Уведомления** — мгновенное уведомление администратору при новом заказе
- ⌨️ **Inline-кнопки** — навигация без команд, удобный UX

## 🛠 Стек

| Компонент | Технология |
|-----------|------------|
| Язык | Python 3.10+ |
| Фреймворк | aiogram 3.x |
| FSM Storage | MemoryStorage |
| База данных | JSON / SQLite |
| Деплой | VPS / любой хостинг |

## 📁 Структура проекта

```
shopbot/
├── bot.py              # Точка входа, запуск polling
├── config.py           # Токен и настройки
├── data.py             # Товары и категории
├── states.py           # FSM-состояния для оформления заказа
├── handlers/
│   ├── common.py       # /start, главное меню
│   ├── catalog.py      # Просмотр каталога
│   ├── cart.py         # Корзина
│   └── checkout.py     # Оформление заказа
└── requirements.txt
```

## 🚀 Запуск

```bash
git clone https://github.com/Seliaev/ShopBot.git
cd ShopBot
pip install -r requirements.txt
```

Создайте файл `.env` или отредактируйте `config.py`:

```python
BOT_TOKEN = "ваш_токен_от_BotFather"
ADMIN_ID = 123456789  # ваш Telegram ID
```

```bash
python bot.py
```

## 💬 Команды

| Команда | Действие |
|---------|----------|
| `/start` | Главное меню |
| `/catalog` | Каталог товаров |
| `/cart` | Корзина |
| `/help` | Помощь |

## 📸 Демонстрация

Попробуйте бота прямо сейчас: [@Portfolio_1_Shop_Bot](https://t.me/Portfolio_1_Shop_Bot)

---

> Разработано [Denis Seliaev](https://github.com/Seliaev) · [Заказать похожий проект](https://kwork.ru/user/seliaev)
