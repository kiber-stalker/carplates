# core/pricing.py
from config import BASE_PRICE, TIER_PRICE_MULT


def code_length_mult(code: str) -> float:
    return 1.4 if len(code) == 3 else 1.0


def price_of(plate: dict, tier: str, region_weight: float, market_trend: float = 1.0) -> int:
    mult = TIER_PRICE_MULT[tier]
    region_mult = 1.0 + (region_weight - 1.0) * 0.5
    code_mult = code_length_mult(plate["region_code"])
    return int(BASE_PRICE * mult * region_mult * code_mult * market_trend)