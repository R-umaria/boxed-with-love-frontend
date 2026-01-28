from __future__ import annotations

from typing import List, Optional

from .data_store import PRODUCTS, Product


SORT_OPTIONS = {
    "popular": lambda product: (-product.rating, product.price),
    "price_low": lambda product: product.price,
    "new": lambda product: product.id,
}


def list_products(search: str | None = None, sort: str | None = None) -> List[Product]:
    results = PRODUCTS
    if search:
        lowered = search.lower()
        results = [p for p in results if lowered in p.name.lower() or lowered in p.description.lower()]
    if sort in SORT_OPTIONS:
        results = sorted(results, key=SORT_OPTIONS[sort])
    return results


def get_product(product_id: int) -> Optional[Product]:
    return next((p for p in PRODUCTS if p.id == product_id), None)
