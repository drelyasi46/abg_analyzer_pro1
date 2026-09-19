#!/usr/bin/env bash
set -e

PROJECT="$HOME/abg_analyzer_pro"
cd "$PROJECT"

echo "============================================================"
echo "ABG ANALYZER PRO — CLEAN UI BUILD"
echo "============================================================"

# ------------------------------------------------------------
# 1. SAFETY: VERIFY ENGINE FREEZE
# ------------------------------------------------------------
echo
echo "===== STEP 1 — VERIFY ENGINE FREEZE ====="

if [ ! -f freeze/ABG_ENGINE_FREEZE.tar.gz ] || \
   [ ! -f freeze/ABG_ENGINE_FREEZE.sha256 ]; then
    echo "ERROR: ENGINE FREEZE NOT FOUND"
    exit 1
fi

sha256sum -c freeze/ABG_ENGINE_FREEZE.sha256

# ------------------------------------------------------------
# 2. VERIFY ACTIVE CORE STILL COMPILES
# ------------------------------------------------------------
echo
echo "===== STEP 2 — VERIFY CORE ====="

find core -type d -name "__pycache__" -exec rm -rf {} +

python3 -m compileall -q core

python3 - <<'PY'
from core.abg_engine import ABGEngine

print("CORE IMPORT: PASS")
print("ENGINE:", ABGEngine)
PY

# ------------------------------------------------------------
# 3. CREATE UI DIRECTORIES
# ------------------------------------------------------------
echo
echo "===== STEP 3 — CREATE UI ====="

mkdir -p widgets

# ------------------------------------------------------------
# 4. HEADER CARD
# ------------------------------------------------------------
cat > widgets/header_card.py <<'PY'
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel


class HeaderCard(MDCard):

    def __init__(self, **kwargs):
        super().__init__(
            orientation="vertical",
            padding="16dp",
            spacing="4dp",
            radius=[16, 16, 16, 16],
            elevation=2,
            **kwargs
        )

        self.add_widget(
            MDLabel(
                text="ABG Analyzer Pro",
                font_style="H5",
                halign="center",
                size_hint_y=None,
                height="40dp",
            )
        )

        self.add_widget(
            MDLabel(
                text="Arterial Blood Gas Analysis",
                halign="center",
                theme_text_color="Secondary",
                size_hint_y=None,
                height="28dp",
            )
        )
PY

# ------------------------------------------------------------
# 5. INPUT CARD
# ------------------------------------------------------------
cat > widgets/input_card.py <<'PY'
from kivymd.uix.card import MDCard
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.boxlayout import MDBoxLayout


class InputCard(MDCard):

    def __init__(self, analyze_callback=None, **kwargs):
        super().__init__(
            orientation="vertical",
            padding="16dp",
            spacing="10dp",
            radius=[16, 16, 16, 16],
            elevation=2,
            **kwargs
        )

        self.analyze_callback = analyze_callback

        self.fields = {}

        layout = MDBoxLayout(
            orientation="vertical",
            spacing="10dp"
        )

        definitions = [
            ("ph", "pH"),
            ("pco2", "PaCO₂"),
            ("hco3", "HCO₃⁻"),
            ("na", "Na⁺"),
            ("cl", "Cl⁻"),
        ]

        for key, label in definitions:
            field = MDTextField(
                hint_text=label,
                mode="rectangle",
                size_hint_y=None,
                height="52dp",
                input_filter="float",
            )
            self.fields[key] = field
            layout.add_widget(field)

        button = MDRaisedButton(
            text="ANALYZE ABG",
            size_hint_y=None,
            height="48dp",
            pos_hint={"center_x": 0.5},
        )

        button.bind(on_release=self._analyze)

        layout.add_widget(button)

        self.add_widget(layout)

    def _analyze(self, *args):
        if self.analyze_callback:
            self.analyze_callback(self.get_values())

    def get_values(self):
        values = {}

        for key, field in self.fields.items():
            text = field.text.strip()

            if not text:
                raise ValueError(f"Missing value: {key}")

            values[key] = float(text)

        return values
PY

# ------------------------------------------------------------
# 6. RESULT CARD
# ------------------------------------------------------------
cat > widgets/result_card.py <<'PY'
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
PY

# ------------------------------------------------------------
# 7. MAIN APPLICATION
# ------------------------------------------------------------
cat > main.py <<'PY'
from kivy.lang import Builder
from kivymd.app import MDApp

from core.abg_engine import ABGEngine
from widgets.header_card import HeaderCard
from widgets.input_card import InputCard
from widgets.result_card import ResultCard


KV = """
MDScreen:
    md_bg_color: app.theme_cls.backgroundColor

    MDBoxLayout:
        orientation: "vertical"
        padding: "12dp"
        spacing: "12dp"

        ScrollView:
            do_scroll_x: False

            MDBoxLayout:
                orientation: "vertical"
                spacing: "12dp"
                size_hint_y: None
                height: self.minimum_height

                HeaderCard:
                    size_hint_y: None
                    height: "110dp"

                InputCard:
                    id: input_card
                    size_hint_y: None
                    height: "430dp"

                ResultCard:
                    id: result_card
                    size_hint_y: None
                    height: "420dp"
"""


class ABGApp(MDApp):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.engine = ABGEngine()

    def build(self):
        self.title = "ABG Analyzer Pro"

        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Blue"

        root = Builder.load_string(KV)

        root.ids.input_card.analyze_callback = self.analyze

        return root

    def analyze(self, values):
        try:
            report = self.engine.analyze(**values)

            self.root.ids.result_card.set_report(report)

        except Exception as e:
            self.root.ids.result_card.set_report(
                f"Unexpected Error:\n\n{type(e).__name__}: {e}"
            )


if __name__ == "__main__":
    ABGApp().run()
PY

# ------------------------------------------------------------
# 8. INIT FILE
# ------------------------------------------------------------
cat > widgets/__init__.py <<'PY'
PY

# ------------------------------------------------------------
# 9. COMPILE TEST
# ------------------------------------------------------------
echo
echo "===== STEP 4 — COMPILE UI ====="

python3 -m compileall -q main.py widgets core

echo "UI COMPILE: PASS"

# ------------------------------------------------------------
# 10. IMPORT TEST
# ------------------------------------------------------------
echo
echo "===== STEP 5 — IMPORT UI ====="

python3 - <<'PY'
from core.abg_engine import ABGEngine
from widgets.header_card import HeaderCard
from widgets.input_card import InputCard
from widgets.result_card import ResultCard

print("ABGEngine: PASS")
print("HeaderCard: PASS")
print("InputCard: PASS")
print("ResultCard: PASS")
PY

echo
echo "===== STEP 6 — MAIN IMPORT ====="

python3 - <<'PY'
import main
print("MAIN IMPORT: PASS")
print("ABGApp:", main.ABGApp)
PY

# ------------------------------------------------------------
# 11. CLINICAL ENGINE REGRESSION
# ------------------------------------------------------------
echo
echo "===== STEP 7 — CLINICAL REGRESSION ====="

python3 - <<'PY'
from core.abg_engine import ABGEngine

r = ABGEngine.analyze(
    ph=7.50,
    pco2=25,
    hco3=30,
    na=140,
    cl=90
)

assert r["primary_disorder"] == "Metabolic Alkalosis"
assert r["triple_disorder"]["triple_disorder"] is True
assert r["severity"]["severity"] == "HIGH"
assert "Triple acid-base disorder detected." in \
       r["interpretation"]["clinical_report"]

print("CLINICAL REGRESSION: PASS")
print("PRIMARY :", r["primary_disorder"])
print("TRIPLE  :", r["triple_disorder"])
print("SEVERITY:", r["severity"])
PY

# ------------------------------------------------------------
# 12. FINAL STATUS
# ------------------------------------------------------------
echo
echo "============================================================"
echo "CLEAN UI BUILD COMPLETE"
echo "============================================================"
echo "CORE:              PASS"
echo "UI COMPILE:        PASS"
echo "UI IMPORT:         PASS"
echo "MAIN IMPORT:       PASS"
echo "CLINICAL ENGINE:   PASS"
echo
echo "FILES CREATED:"
find widgets -maxdepth 1 -type f -printf "  %p\n" | sort
echo "  main.py"
echo
echo "ENGINE WAS NOT MODIFIED."
echo "============================================================"
