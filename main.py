from kivymd.app import MDApp
from kivy.lang import Builder

from core.abg_engine import ABGEngine
from widgets.header_card import HeaderCard
from widgets.input_card import InputCard
from widgets.result_card import ResultCard

Builder.load_file("widgets/header_card.kv")
Builder.load_file("widgets/input_card.kv")
Builder.load_file("widgets/result_card.kv")


class ABGApp(MDApp):

    def build(self):
        return Builder.load_file("main.kv")

    def analyze(self):
        try:
            values = self.root.ids.input_card.get_values()
            result = ABGEngine.analyze(**values)
            self.root.ids.result_card.set_report(result["report"])
        except Exception as e:
            self.root.ids.result_card.set_report(
                f"Error: {type(e).__name__}: {e}"
            )


if __name__ == "__main__":
    ABGApp().run()
