from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel


class HeaderCard(MDCard):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.orientation = "vertical"
        self.padding = "16dp"
        self.spacing = "4dp"
        self.radius = [16, 16, 16, 16]
        self.elevation = 2

        self.add_widget(
            MDLabel(
                text="ABG Analyzer Pro",
                halign="center",
                size_hint_y=None,
                height="40dp",
            )
        )

        self.add_widget(
            MDLabel(
                text="Arterial Blood Gas Analysis",
                halign="center",
                size_hint_y=None,
                height="28dp",
            )
        )
