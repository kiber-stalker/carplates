# core/rarity.py
from config import RARITY_TIERS, MAIN_REGION_CODES

DIGIT_PATTERNS = {
    # топ
    "777": 250, "001": 200, "666": 200, "999": 170,
    # последовательности
    "123": 120, "321": 120, "234": 100, "456": 100, "789": 100,
    # тройные
    "111": 110, "222": 110, "333": 110, "444": 110,
    "555": 110, "888": 110,
    # парные
    "110": 25, "112": 25, "113": 25, "114": 25,
    "220": 25, "221": 25, "223": 25, "224": 25,
    "330": 25, "331": 25, "332": 25, "334": 25,
    "440": 25, "441": 25, "442": 25, "443": 25,
    "550": 25, "551": 25, "552": 25, "553": 25, "554": 25,
    "660": 25, "661": 25, "662": 25, "663": 25, "664": 25, "665": 25,
    "880": 25, "881": 25, "882": 25, "883": 25, "884": 25, "885": 25, "886": 25, "887": 25,
    "900": 25, "990": 25, "909": 25, "919": 25, "929": 25,
}

LETTER_SERIES = ("АМР", "АМП", "ЕКХ", "СММ", "МММ", "ООО", "ААА")


def score_region_code(code: str) -> float:
    if code in MAIN_REGION_CODES:
        return 20.0
    if len(code) == 2:
        return 35.0
    return 60.0


def score_region(code: str, region_weight: float) -> float:
    base = score_region_code(code)
    return base * (1.0 + (region_weight - 1.0) * 0.5)


def score_letters(letters: str) -> float:
    score = 0.0
    if letters[0] == letters[1] == letters[2]:
        score += 200
    elif letters[0] == letters[1] or letters[1] == letters[2] or letters[0] == letters[2]:
        score += 35
    if letters in LETTER_SERIES:
        score += 400
    return score


def score_digits(digits: str) -> float:
    return DIGIT_PATTERNS.get(digits, 0)


def total_score(plate: dict, region_weight: float) -> float:
    return (
        score_region(plate["region_code"], region_weight)
        + score_letters(plate["letters"])
        + score_digits(plate["digits"])
    )


def tier_of(score: float) -> str:
    for name, lo, hi in RARITY_TIERS:
        if lo <= score < hi:
            return name
    return "Legendary"