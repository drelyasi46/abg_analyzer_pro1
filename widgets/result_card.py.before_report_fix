from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.scrollview import MDScrollView


class ResultCard(MDCard):

    def __init__(self, **kwargs):
        super().__init__(
            orientation="vertical",
            padding="16dp",
            radius=[16, 16, 16, 16],
            elevation=2,
            **kwargs
        )

        self.label = MDLabel(
            text="Enter ABG values and press ANALYZE ABG.",
            halign="left",
            valign="top",
            size_hint_y=None,
            markup=False,
        )

        self.label.bind(texture_size=self._update_height)

        scroll = MDScrollView()
        scroll.add_widget(self.label)

        self.add_widget(scroll)

    def _update_height(self, instance, value):
        instance.height = max(value[1], 200)

    def set_report(self, report):
        self.label.text = str(report)
