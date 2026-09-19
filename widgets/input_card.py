from kivymd.uix.card import MDCard
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.boxlayout import MDBoxLayout


class InputCard(MDCard):

    def __init__(self, analyze_callback=None, **kwargs):
        super().__init__(
            orientation="vertical",
            padding=["16dp", "16dp", "16dp", "16dp"],
            spacing="8dp",
            radius=[16, 16, 16, 16],
            elevation=2,
            **kwargs
        )

        self.analyze_callback = analyze_callback
        self.fields = {}

        layout = MDBoxLayout(
            orientation="vertical",
            spacing="8dp",
            size_hint_y=None,
        )

        layout.bind(minimum_height=layout.setter("height"))

        definitions = [
            ("ph", "pH"),
            ("pco2", "PaCO2"),
            ("hco3", "HCO3-"),
            ("na", "Na+"),
            ("k", "K+"),
            ("cl", "Cl-"),
            ("albumin", "Albumin"),
            ("lactate", "Lactate"),
        ]

        for key, label in definitions:
            field = MDTextField(
                hint_text=label,
                mode="rectangle",
                padding=["12dp", "20dp", "12dp", "6dp"],
                size_hint_y=None,
                height="52dp",
                input_filter="float",
            )

            self.fields[key] = field
            layout.add_widget(field)

        button = MDRaisedButton(
            text="ANALYZE ABG",
            size_hint_y=None,
            height="48dp",
            pos_hint={"center_x": 0.5},
        )

        button.bind(on_release=self._analyze)
        layout.add_widget(button)

        self.add_widget(layout)

        layout.bind(height=self._update_card_height)
        self._update_card_height(layout, layout.height)

    def _update_card_height(self, layout, height):
        self.height = height + self.padding[1] + self.padding[3]

    def _analyze(self, *args):
        if self.analyze_callback:
            try:
                self.analyze_callback(self.get_values())
            except Exception as e:
                print(f"Input error: {type(e).__name__}: {e}")

    def get_values(self):
        def value(key):
            text = self.fields[key].text.strip()

            if text == "":
                return None

            return float(text)

        return {
            "ph": value("ph"),
            "pco2": value("pco2"),
            "hco3": value("hco3"),
            "na": value("na"),
            "k": value("k"),
            "cl": value("cl"),
            "albumin": value("albumin"),
            "lactate": value("lactate"),
        }
