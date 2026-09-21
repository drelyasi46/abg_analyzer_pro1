from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivy.clock import Clock
from kivy.metrics import dp


class ResultCard(MDBoxLayout):

    SECTION_TITLES = {
        "CLINICAL INTERPRETATION",
        "TRIPLE DISORDER",
        "MIXED DISORDER",
        "COMPENSATION",
        "ANION GAP",
        "DELTA RATIO",
        "SEVERITY",
        "CLINICAL ALERTS",
        "CLINICAL RECOMMENDATIONS",
    }

    SECTION_COLORS = {
        "CLINICAL INTERPRETATION": (0.90, 0.95, 1.00, 1),
        "COMPENSATION": (0.90, 0.98, 0.92, 1),
        "ANION GAP": (0.95, 0.91, 1.00, 1),
        "DELTA RATIO": (0.88, 0.97, 0.97, 1),
        "MIXED DISORDER": (1.00, 0.95, 0.84, 1),
        "TRIPLE DISORDER": (1.00, 0.88, 0.86, 1),
        "SEVERITY": (1.00, 0.94, 0.80, 1),
        "CLINICAL ALERTS": (1.00, 0.88, 0.88, 1),
        "CLINICAL RECOMMENDATIONS": (0.90, 0.94, 1.00, 1),
        "ABG REPORT": (0.95, 0.95, 0.97, 1),
    }

    def set_report(self, report):

        if not report:
            report = "Ready for analysis..."

        def update(dt):
            container = self.ids.report_container
            container.clear_widgets()

            lines = [
                line.strip()
                for line in str(report).splitlines()
                if line.strip()
            ]

            sections = []
            title = "ABG REPORT"
            content = []

            for line in lines:
                if line == "ABG ANALYZER PRO":
                    continue

                if line in self.SECTION_TITLES:
                    if content:
                        sections.append((title, content))
                    title = line
                    content = []
                else:
                    content.append(line)

            if content:
                sections.append((title, content))

            if not sections:
                sections = [
                    ("ABG REPORT", ["Ready for analysis..."])
                ]

            for title, content in sections:

                card = MDCard(
                    orientation="vertical",
                    size_hint_y=None,
                    padding=dp(12),
                    spacing=dp(5),
                    radius=[dp(16), dp(16), dp(16), dp(16)],
                    elevation=5,
                    md_bg_color=self.SECTION_COLORS.get(
                        title,
                        (0.95, 0.95, 0.95, 1)
                    ),
                )

                title_colors = {
                    "SEVERITY": (0.75, 0.35, 0.00, 1),
                    "CLINICAL ALERTS": (0.80, 0.05, 0.05, 1),
                    "TRIPLE DISORDER": (0.75, 0.15, 0.05, 1),
                    "MIXED DISORDER": (0.75, 0.35, 0.00, 1),
                }

                title_label = MDLabel(
                    text=title,
                    bold=True,
                    font_size="17sp" if title in title_colors else "16sp",
                    size_hint_y=None,
                    height=dp(32),
                    theme_text_color="Custom" if title in title_colors else "Primary",
                    text_color=title_colors.get(
                        title,
                        (0.10, 0.10, 0.15, 1)
                    ),
                )

                card.add_widget(title_label)

                body = "\n".join(content)

                body_size = {
                    "SEVERITY": "15sp",
                    "CLINICAL ALERTS": "15sp",
                    "CLINICAL RECOMMENDATIONS": "14sp",
                }.get(title, "14sp")

                body_label = MDLabel(
                    text=body,
                    font_size=body_size,
                    size_hint_y=None,
                    halign="left",
                    valign="top",
                    theme_text_color="Primary",
                    bold=title in (
                        "SEVERITY",
                        "CLINICAL ALERTS",
                    ),
                )

                body_label.text_size = (dp(300), None)
                body_label.texture_update()
                body_label.height = body_label.texture_size[1] + dp(10)

                card.add_widget(body_label)

                card.height = (
                    title_label.height
                    + body_label.height
                    + dp(30)
                )

                container.add_widget(card)

            container.height = container.minimum_height

        Clock.schedule_once(update, 0)

    def clear(self):
        self.set_report("Ready for analysis...")
