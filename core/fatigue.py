# core/fatigue.py
from config import FATIGUE_STEP, FATIGUE_MAX


class Fatigue:
    def __init__(self):
        self.value = 0

    def spin(self):
        self.value += 1

    def save(self):
        self.value = 0

    def penalty(self) -> float:
        return min(self.value * FATIGUE_STEP, FATIGUE_MAX)

    def apply(self, base_chance: float) -> float:
        return base_chance * (1.0 - self.penalty())