from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel

from core.abg_engine import ABGEngine
from widgets.input_card import InputCard
from widgets.result_card import ResultCard


class ABGApp(MDApp):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.engine = ABGEngine()

    def build(self):
        self.title = "ABG Analyzer Pro"

        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Blue"

        screen = MDScreen()

        scroll = MDScrollView(
            do_scroll_x=False,
            do_scroll_y=True,
        )

        layout = MDBoxLayout(
            orientation="vertical",
            padding="12dp",
            spacing="12dp",
            size_hint_y=None,
        )

        layout.bind(minimum_height=layout.setter("height"))

        header = MDCard(
            orientation="vertical",
            padding=["16dp", "12dp", "16dp", "12dp"],
            spacing="2dp",
            size_hint_y=None,
            height="76dp",
            radius=[16, 16, 16, 16],
            elevation=0,
        )

        header.add_widget(
            MDLabel(
                text="ABG Analyzer Pro",
                halign="center",
                valign="middle",
                size_hint_y=None,
                height="36dp",
            )
        )

        header.add_widget(
            MDLabel(
                text="Arterial Blood Gas Analysis",
                halign="center",
                valign="middle",
                size_hint_y=None,
                height="28dp",
            )
        )

        self.input_card = InputCard(
            size_hint_y=None,
            
        )
        self.input_card.analyze_callback = self.analyze

        self.result_card = ResultCard(
            size_hint_y=None,
            height="420dp",
        )

        layout.add_widget(header)
        layout.add_widget(self.input_card)
        layout.add_widget(self.result_card)

        scroll.add_widget(layout)
        screen.add_widget(scroll)

        return screen

    def analyze(self, values):
        try:
            report = self.engine.analyze(**values)
            self.result_card.set_report(report["report"])

        except Exception as e:
            self.result_card.set_report(
                f"Unexpected Error:\n\n{type(e).__name__}: {e}"
            )


if __name__ == "__main__":
    ABGApp().run()
