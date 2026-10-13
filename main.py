# main.py — Kivy-версия
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.properties import StringProperty

from core.generator import PlateGenerator
from core.rarity import total_score, tier_of
from core.pricing import price_of
from core.fatigue import Fatigue


TIER_COLORS = {
    "Common":    (0.7, 0.7, 0.7, 1),
    "Uncommon":  (0.3, 0.8, 0.3, 1),
    "Rare":      (0.2, 0.5, 1.0, 1),
    "Epic":      (0.7, 0.3, 1.0, 1),
    "Legendary": (1.0, 0.7, 0.1, 1),
}


class RootWidget(BoxLayout):
    plate_text = StringProperty("Нажми «Крутить»")
    tier_text = StringProperty("")
    info_text = StringProperty("")
    fatigue_text = StringProperty("Усталость: 0 (0%)")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.padding = 20
        self.spacing = 15
        self.gen = PlateGenerator()
        self.fatigue = Fatigue()
        self.current_plate = None

        self.add_widget(Label(text="CarPlates", font_size=32, size_hint=(1, 0.15)))

        self.plate_label = Label(
            text=self.plate_text,
            font_size=48,
            bold=True,
            size_hint=(1, 0.25),
        )
        self.add_widget(self.plate_label)

        self.tier_label = Label(
            text=self.tier_text,
            font_size=28,
            size_hint=(1, 0.12),
        )
        self.add_widget(self.tier_label)

        self.info_label = Label(
            text=self.info_text,
            font_size=18,
            size_hint=(1, 0.15),
        )
        self.add_widget(self.info_label)

        self.fatigue_label = Label(
            text=self.fatigue_text,
            font_size=16,
            size_hint=(1, 0.1),
        )
        self.add_widget(self.fatigue_label)

        spin_btn = Button(text="Крутить (полный)", font_size=24, size_hint=(1, 0.15))
        spin_btn.bind(on_press=lambda x: self.spin("full"))
        self.add_widget(spin_btn)

        save_btn = Button(text="Сохранить в инвентарь", font_size=24, size_hint=(1, 0.15))
        save_btn.bind(on_press=self.save)
        self.add_widget(save_btn)

    def spin(self, mode="full"):
        plate = self.gen.generate(mode, base=self.current_plate)
        self.current_plate = plate
        self.fatigue.spin()

        rw = self.gen.region_weight(plate["region_code"])
        score = total_score(plate, rw)
        tier = tier_of(score)
        price = price_of(plate, tier, rw)

        self.plate_label.text = plate["display"]
        self.plate_label.color = TIER_COLORS[tier]
        self.tier_label.text = tier
        self.tier_label.color = TIER_COLORS[tier]
        self.info_label.text = f"score: {score:.1f}\nЦена: {price} coins"
        self.fatigue_label.text = f"Усталость: {self.fatigue.value} ({self.fatigue.penalty():.0%})"

    def save(self, instance):
        if self.current_plate:
            self.fatigue.save()
            self.info_label.text = "Сохранено! Усталость сброшена."
            self.fatigue_label.text = f"Усталость: {self.fatigue.value} (0%)"


class CarPlatesApp(App):
    def build(self):
        return RootWidget()


if __name__ == "__main__":
    CarPlatesApp().run()
