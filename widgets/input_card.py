from kivymd.uix.boxlayout import MDBoxLayout


class InputCard(MDBoxLayout):

    def get_values(self):

        def value(widget_id):
            text = self.ids[widget_id].text.strip()

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