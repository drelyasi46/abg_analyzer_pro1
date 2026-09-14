from kivymd.uix.boxlayout import MDBoxLayout
from kivy.clock import Clock


class ResultCard(MDBoxLayout):

    def set_report(self, report):

        if not report:
            report = "Ready for analysis..."

        def update(dt):
            self.ids.report.text = report
            self.ids.report.texture_update()
            self.ids.report.height = self.ids.report.texture_size[1]

        Clock.schedule_once(update, 0)

    def clear(self):
        self.set_report("Ready for analysis...")