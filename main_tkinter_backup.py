from abg_engine import ABGEngine
import tkinter as tk

print("PROGRAM STARTED")


class ABGApp:

    def __init__(self, root):
        self.root = root
        self.engine = ABGEngine()

        self.root.title("ABG Analyzer Pro - ICU")
        self.root.geometry("700x600")
        self.root.configure(bg="#1e1e1e")

        tk.Label(root, text="ABG ICU Analyzer", fg="white", bg="#1e1e1e",
                 font=("Arial", 20, "bold")).pack(pady=10)

        self.ph = self.make_input("pH")
        self.pco2 = self.make_input("PaCO2")
        self.hco3 = self.make_input("HCO3")
        self.na = self.make_input("Na")
        self.cl = self.make_input("Cl")

        tk.Button(root, text="ANALYZE", bg="green", fg="white",
                  command=self.analyze).pack(pady=10)

        self.output = tk.Text(root, height=18, bg="black", fg="white")
        self.output.pack()

    def make_input(self, label):
        frame = tk.Frame(self.root, bg="#1e1e1e")
        frame.pack()

        tk.Label(frame, text=label, fg="white", bg="#1e1e1e", width=8).pack(side=tk.LEFT)
        entry = tk.Entry(frame)
        entry.pack(side=tk.LEFT)

        return entry

    def analyze(self):

        try:
            result = self.engine.analyze(
                float(self.ph.get()),
                float(self.pco2.get()),
                float(self.hco3.get()),
                float(self.na.get()) if self.na.get() else None,
                float(self.cl.get()) if self.cl.get() else None
            )

            self.output.delete("1.0", tk.END)
            self.output.insert(tk.END, "\n".join(result))

        except Exception as e:
            self.output.delete("1.0", tk.END)
            self.output.insert(tk.END, str(e))


if __name__ == "__main__":
    root = tk.Tk()
    app = ABGApp(root)
    root.mainloop()