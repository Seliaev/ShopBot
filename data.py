"""Данные каталога магазина"""

CATEGORIES = {
    "smartphones": "📱 Смартфоны",
    "laptops": "💻 Ноутбуки",
    "audio": "🎧 Аудио",
    "accessories": "🔌 Аксессуары",
}

PRODUCTS: dict[str, list[dict]] = {
    "smartphones": [
        {
            "id": "s1",
            "name": "iPhone 15 Pro",
            "price": 129_990,
            "desc": "Чип A17 Pro · 48 Мпикс · 256 ГБ · Титановый корпус",
            "emoji": "🍎",
            "rating": 4.9,
            "stock": 5,
        },
        {
            "id": "s2",
            "name": "Samsung Galaxy S24 Ultra",
            "price": 119_990,
            "desc": "Snapdragon 8 Gen 3 · 200 Мпикс · S Pen · 512 ГБ",
            "emoji": "🌌",
            "rating": 4.8,
            "stock": 8,
        },
        {
            "id": "s3",
            "name": "Google Pixel 9 Pro",
            "price": 89_990,
            "desc": "Чип Tensor G4 · Лучшая камера 2024 · 7 лет обновлений",
            "emoji": "🔵",
            "rating": 4.7,
            "stock": 12,
        },
        {
            "id": "s4",
            "name": "Xiaomi 14 Ultra",
            "price": 99_990,
            "desc": "Snapdragon 8 Gen 3 · Leica камера · 90W зарядка",
            "emoji": "🔴",
            "rating": 4.6,
            "stock": 6,
        },
    ],
    "laptops": [
        {
            "id": "l1",
            "name": "MacBook Pro 14\" M4",
            "price": 199_990,
            "desc": "Чип M4 Pro · 24 ГБ RAM · 512 ГБ SSD · Liquid Retina XDR",
            "emoji": "🖥",
            "rating": 4.9,
            "stock": 3,
        },
        {
            "id": "l2",
            "name": "ASUS ROG Zephyrus G16",
            "price": 159_990,
            "desc": "RTX 4080 · Intel i9 · 32 ГБ RAM · 240 Гц OLED",
            "emoji": "🎮",
            "rating": 4.7,
            "stock": 4,
        },
        {
            "id": "l3",
            "name": "Dell XPS 15",
            "price": 149_990,
            "desc": "Intel Core Ultra 9 · 32 ГБ · OLED 3.5K · RTX 4070",
            "emoji": "💼",
            "rating": 4.6,
            "stock": 7,
        },
        {
            "id": "l4",
            "name": "Lenovo ThinkPad X1 Carbon",
            "price": 139_990,
            "desc": "Intel Ultra 7 · 32 ГБ · 1 кг · Военный стандарт прочности",
            "emoji": "🛡",
            "rating": 4.8,
            "stock": 5,
        },
    ],
    "audio": [
        {
            "id": "a1",
            "name": "Sony WH-1000XM5",
            "price": 29_990,
            "desc": "Лучший ANC 2024 · 30ч работы · LDAC · Multipoint",
            "emoji": "🎵",
            "rating": 4.9,
            "stock": 15,
        },
        {
            "id": "a2",
            "name": "Apple AirPods Pro 2",
            "price": 24_990,
            "desc": "H2 чип · Адаптивный ANC · MagSafe · 6ч + 24ч кейс",
            "emoji": "🍎",
            "rating": 4.8,
            "stock": 20,
        },
        {
            "id": "a3",
            "name": "Bose QuietComfort 45",
            "price": 27_990,
            "desc": "TriPort акустика · 24ч · Режим Aware · Складная конструкция",
            "emoji": "🔊",
            "rating": 4.7,
            "stock": 10,
        },
        {
            "id": "a4",
            "name": "JBL Flip 7",
            "price": 12_990,
            "desc": "IP68 · 12ч · PartyBoost · Bass Boost · USB-C",
            "emoji": "💧",
            "rating": 4.6,
            "stock": 25,
        },
    ],
    "accessories": [
        {
            "id": "ac1",
            "name": "Anker 140W GaN Charger",
            "price": 5_990,
            "desc": "3 порта USB-C + USB-A · GaN технология · Компактный",
            "emoji": "⚡",
            "rating": 4.8,
            "stock": 30,
        },
        {
            "id": "ac2",
            "name": "Samsung T9 SSD 2TB",
            "price": 14_990,
            "desc": "2000 МБ/с · IP65 · USB 3.2 Gen 2×2 · Ударопрочный",
            "emoji": "💾",
            "rating": 4.9,
            "stock": 12,
        },
        {
            "id": "ac3",
            "name": "Logitech MX Master 3S",
            "price": 9_990,
            "desc": "8000 DPI · Тихие клики · MagSpeed скролл · 70 дней работы",
            "emoji": "🖱",
            "rating": 4.9,
            "stock": 18,
        },
        {
            "id": "ac4",
            "name": "Apple MagSafe Charger 25W",
            "price": 4_990,
            "desc": "25W быстрая зарядка · Магнитное соединение · USB-C",
            "emoji": "🧲",
            "rating": 4.7,
            "stock": 40,
        },
    ],
}


def get_product_by_id(product_id: str) -> dict | None:
    for products in PRODUCTS.values():
        for product in products:
            if product["id"] == product_id:
                return product
    return None


def format_price(price: int) -> str:
    return f"{price:,}".replace(",", " ") + " ₽"
