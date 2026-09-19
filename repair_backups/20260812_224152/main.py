from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.resources import resource_add_path
import os

from core.abg_engine import ABGEngine

from widgets.header_card import HeaderCard
from widgets.input_card import InputCard
from widgets.result_card import ResultCard


class ABGApp(MDApp):

    def build(self):
        self.title = "ABG Analyzer Pro"

        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.primary_hue = "700"
        self.theme_cls.theme_style = "Light"

        self.engine = ABGEngine()

        # Android-safe KV loading
        app_dir = os.path.dirname(os.path.abspath(__file__))
        resource_add_path(app_dir)

        Builder.load_file(
            os.path.join(app_dir, "widgets/header_card.kv")
        )

        Builder.load_file(
            os.path.join(app_dir, "widgets/input_card.kv")
        )

        Builder.load_file(
            os.path.join(app_dir, "widgets/result_card.kv")
        )

        return Builder.load_file(
            os.path.join(app_dir, "main.kv")
        )


    def analyze(self):

        print(">>> Analyze button pressed")

        try:
            values = self.root.ids.input_card.get_values()

            print("Input Values:")
            print(values)

            if (
                values["ph"] is None or
                values["pco2"] is None or
                values["hco3"] is None
            ):
                self.root.ids.result_card.set_report(
                    "Please enter pH, PaCO2 and HCO3."
                )
                return

            report = self.engine.analyze(**values)

            print("Engine Output:")
            print(report)

            self.root.ids.result_card.set_report(
                report["report"]
            )


        except ValueError:

            self.root.ids.result_card.set_report(
                "Invalid numeric input."
            )


        except Exception as e:

            import traceback
            traceback.print_exc()

            self.root.ids.result_card.set_report(
                f"Unexpected Error:\n\n{e}"
            )


if __name__ == "__main__":
    ABGApp().run()
