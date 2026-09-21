from kivymd.uix.boxlayout import MDBoxLayout
from kivy.properties import NumericProperty, BooleanProperty, StringProperty


class NumberStepper(MDBoxLayout):

    label = StringProperty("")
    value = NumericProperty(0)
    has_value = BooleanProperty(False)

    increment_step = NumericProperty(1)
    decrement_step = NumericProperty(1)

    start_value = NumericProperty(0)
    min_value = NumericProperty(0)
    max_value = NumericProperty(999)

    def increase(self):
        if not self.has_value:
            self.value = self.start_value
            self.has_value = True
            return

        new_value = self.value + self.increment_step

        if new_value <= self.max_value:
            self.value = round(new_value, 2)

    def decrease(self):
        if not self.has_value:
            return

        new_value = self.value - self.decrement_step

        if new_value < self.min_value:
            self.clear()
            return

        self.value = round(new_value, 2)

    def clear(self):
        self.has_value = False
        self.value = self.start_value


class InputCard(MDBoxLayout):

    def get_values(self):

        def value(widget_id):
            widget = self.ids[widget_id]

            if not widget.has_value:
                return None

            return float(widget.value)

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

    def clear_all(self):
        for widget_id in (
            "ph",
            "pco2",
            "hco3",
            "na",
            "k",
            "cl",
            "albumin",
            "lactate",
        ):
            self.ids[widget_id].clear()
