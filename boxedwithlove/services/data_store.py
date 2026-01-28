from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List
from uuid import uuid4


@dataclass
class Product:
    id: int
    name: str
    description: str
    price: float
    rating: float
    category: str
    whats_inside: List[str]


@dataclass
class CartItem:
    id: str
    product_id: int
    quantity: int


@dataclass
class Cart:
    id: str
    items: List[CartItem] = field(default_factory=list)


@dataclass
class PaymentMethod:
    id: str
    brand: str
    last4: str
    expiry: str


@dataclass
class Order:
    id: str
    user_id: str
    items: List[CartItem]
    total: float
    status: str
    created_at: datetime
    shipping: Dict[str, str]


@dataclass
class User:
    id: str
    email: str
    name: str


PRODUCTS: List[Product] = [
    Product(
        id=1,
        name="Cozy Comfort Box",
        description="A warm hug in a box with artisan tea and a plush throw.",
        price=58.0,
        rating=4.8,
        category="Cozy",
        whats_inside=["Herbal tea", "Plush throw", "Soy candle"],
    ),
    Product(
        id=2,
        name="Sweet Celebration",
        description="Celebrate with gourmet treats and sparkling joy.",
        price=72.0,
        rating=4.6,
        category="Celebration",
        whats_inside=["Gourmet chocolates", "Sparkling cider", "Confetti pop"],
    ),
    Product(
        id=3,
        name="Self-Care Sunday",
        description="Calming essentials for a restorative reset.",
        price=64.0,
        rating=4.9,
        category="Wellness",
        whats_inside=["Bath soak", "Body butter", "Mindfulness journal"],
    ),
    Product(
        id=4,
        name="Little Sunshine",
        description="Brighten their day with cheerful surprises.",
        price=49.0,
        rating=4.5,
        category="Cheer",
        whats_inside=["Sunshine mug", "Citrus candies", "Mini bouquet"],
    ),
]

CARTS: Dict[str, Cart] = {}
PAYMENT_METHODS: Dict[str, List[PaymentMethod]] = {}
ORDERS: Dict[str, List[Order]] = {}
USERS: Dict[str, User] = {}


def new_id() -> str:
    return uuid4().hex
