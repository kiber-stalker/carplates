# core/generator.py
import json
import random
from pathlib import Path
from config import ALLOWED_LETTERS


class PlateGenerator:
    def __init__(self, data_path: str = "data/plates_ru.json"):
        self.data = json.loads(Path(data_path).read_text(encoding="utf-8"))
        self.country = "RU"
        self.regions = self.data["RU"]["regions"]

    def _pick_region(self) -> dict:
        weights = [r["weight"] for r in self.regions]
        return random.choices(self.regions, weights=weights, k=1)[0]

    def _pick_region_code(self, region: dict) -> str:
        return random.choice(region["codes"])

    def _pick_letters(self) -> str:
        return "".join(random.choice(ALLOWED_LETTERS) for _ in range(3))

    def _pick_digits(self) -> str:
        return f"{random.randint(0, 999):03d}"

    def _display(self, letters: str, digits: str, code: str) -> str:
        # формат: А123ВС 77
        return f"{letters[0]}{digits}{letters[1]}{letters[2]} {code}"

    def generate(self, mode: str = "full", base: dict | None = None) -> dict:
        """
        mode:
          full    — всё случайно
          letters — фиксируем регион+цифры, крутим буквы
          region  — фиксируем буквы+цифры, крутим регион
          digits  — фиксируем буквы+регион, крутим цифры
        base: предыдущий номер (если нужен для фиксации)
        """
        if base is None:
            region = self._pick_region()
            code = self._pick_region_code(region)
            letters = self._pick_letters()
            digits = self._pick_digits()
        else:
            region_name = base["region_name"]
            region = next(r for r in self.regions if r["name"] == region_name)
            code = base["region_code"]
            letters = base["letters"]
            digits = base["digits"]

            if mode == "letters":
                letters = self._pick_letters()
            elif mode == "region":
                region = self._pick_region()
                code = self._pick_region_code(region)
            elif mode == "digits":
                digits = self._pick_digits()
            elif mode == "full":
                region = self._pick_region()
                code = self._pick_region_code(region)
                letters = self._pick_letters()
                digits = self._pick_digits()

        return {
            "country": self.country,
            "region_name": region["name"],
            "region_code": code,
            "letters": letters,
            "digits": digits,
            "display": self._display(letters, digits, code),
        }

    def region_weight(self, code: str) -> float:
        for r in self.regions:
            if code in r["codes"]:
                return r["weight"]
        return 1.0