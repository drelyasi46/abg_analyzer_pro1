from kivymd.app import MDApp
from kivy.lang import Builder

from widgets.header_card import HeaderCard
from widgets.input_card import InputCard
from widgets.result_card import ResultCard

Builder.load_file("widgets/header_card.kv")
Builder.load_file("widgets/input_card.kv")
Builder.load_file("widgets/result_card.kv")

class ABGApp(MDApp):
    def build(self):
        return Builder.load_file("main.kv")

if __name__ == "__main__":
    ABGApp().run()
