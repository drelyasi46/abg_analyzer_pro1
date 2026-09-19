from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.scrollview import MDScrollView


class ResultCard(MDCard):

    def __init__(self, **kwargs):
        super().__init__(
            orientation="vertical",
            padding="12dp",
            radius=[16, 16, 16, 16],
            elevation=2,
            **kwargs
        )

        scroll = MDScrollView(
            do_scroll_x=False,
            do_scroll_y=True,
            bar_width="4dp",
        )

        self.label = MDLabel(
            text="Enter ABG values and press ANALYZE ABG.",
            halign="left",
            valign="top",
            size_hint_y=None,
            markup=False,
            padding=("4dp", "4dp"),
            line_height=1.3,
        )

        self.label.bind(
            width=self._update_width
        )

        self.label.bind(
            texture_size=self._update_height
        )

        scroll.add_widget(self.label)
        self.add_widget(scroll)

    def _update_width(self, instance, width):
        instance.text_size = (max(width - 8, 1), None)

    def _update_height(self, instance, texture_size):
        instance.height = max(texture_size[1] + 8, 80)

    def set_report(self, report):
        self.label.text = str(report)
