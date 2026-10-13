# config.py

ALLOWED_LETTERS = ["А", "В", "Е", "К", "М", "Н", "О", "Р", "С", "Т", "У", "Х"]

RARITY_TIERS = [
    ("Common",    0,    100),
    ("Uncommon",  100,  220),
    ("Rare",      220,  450),
    ("Epic",      450,  750),
    ("Legendary", 750,  999999),
]

TIER_PRICE_MULT = {
    "Common":    1.0,
    "Uncommon":  3.0,
    "Rare":      12.0,
    "Epic":      60.0,
    "Legendary": 500.0,
}

BASE_PRICE = 1000

FATIGUE_STEP = 0.01
FATIGUE_MAX = 0.70

MAIN_REGION_CODES = {
    "77","99","50","78","23","66","16","47","90","98"
}