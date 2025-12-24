import os
import sys
import subprocess
import webbrowser

from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.image import Image
from kivy.uix.screenmanager import ScreenManager, Screen

# Optional: Markdown conversion (desktop-friendly, APK-friendly if you vendor the module)
def md_to_html(md_text):
    try:
        import markdown
        return markdown.markdown(md_text, extensions=['fenced_code', 'tables'])
    except Exception:
        # Minimal fallback: wrap in <pre> to preserve formatting
        return f"<html><head><meta charset='utf-8'><style>body{{background:#111;color:#eee;font-family:Arial;}} pre{{white-space:pre-wrap;line-height:1.4}}</style></head><body><pre>{md_text}</pre></body></html>"

def write_html_from_readme():
    readme_path = os.path.join(os.getcwd(), "README.md")
    if not os.path.exists(readme_path):
        return None
    with open(readme_path, "r", encoding="utf-8") as f:
        md = f.read()
    html = md_to_html(md)
    out_path = os.path.join(os.getcwd(), "README.html")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html)
    return out_path

class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super(HomeScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', spacing=15, padding=20)

        self.status = Label(text="Welcome! Select an action.", size_hint=(1, 0.1))
        layout.add_widget(self.status)

        btn1 = Button(text="Process Sample Images", background_color=(0.2, 0.6, 0.9, 1))
        btn1.bind(on_press=self.process_images)
        layout.add_widget(btn1)

        btn2 = Button(text="Export to PDF", background_color=(0.3, 0.8, 0.4, 1))
        btn2.bind(on_press=self.export_pdf)
        layout.add_widget(btn2)

        btn3 = Button(text="View PDF", background_color=(0.9, 0.5, 0.2, 1))
        btn3.bind(on_press=self.view_pdf)
        layout.add_widget(btn3)

        btn4 = Button(text="Open Gallery", background_color=(0.7, 0.3, 0.9, 1))
        btn4.bind(on_press=self.go_gallery)
        layout.add_widget(btn4)

        # Notebook-style README (HTML)
        btn5 = Button(text="Open README (Notebook view)", background_color=(0.9, 0.8, 0.2, 1))
        btn5.bind(on_press=self.open_readme_notebook)
        layout.add_widget(btn5)

        self.add_widget(layout)

    def go_gallery(self, instance):
        self.manager.current = 'gallery'

    def process_images(self, instance):
        subprocess.run([sys.executable, "replicate.py"])
        self.status.text = "✅ Images processed and saved to /processed"

    def export_pdf(self, instance):
        subprocess.run([sys.executable, "pdf_export.py"])
        self.status.text = "✅ PDF exported to /output/finger_scans.pdf"

    def view_pdf(self, instance):
        pdf_path = os.path.join("output", "finger_scans.pdf")
        if os.path.exists(pdf_path):
            if sys.platform.startswith("win"):
                os.startfile(pdf_path)
            elif sys.platform.startswith("darwin"):
                subprocess.run(["open", pdf_path])
            else:
                subprocess.run(["xdg-open", pdf_path])
            self.status.text = "📄 Opening PDF..."
        else:
            self.status.text = "⚠️ PDF not found. Export first!"

    def open_readme_notebook(self, instance):
        html_path = write_html_from_readme()
        if not html_path:
            self.status.text = "⚠️ README.md not found."
            return
        # Open in default browser (works on desktop; on Android opens external browser)
        webbrowser.open(f"file:///{html_path}")
        self.status.text = "📘 Opening README in notebook view..."

class GalleryScreen(Screen):
    def on_enter(self):
        self.clear_widgets()
        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)

        back_btn = Button(text="⬅ Back to Home", size_hint=(1, 0.1), background_color=(0.8, 0.2, 0.2, 1))
        back_btn.bind(on_press=lambda x: setattr(self.manager, 'current', 'home'))
        layout.add_widget(back_btn)

        scroll = ScrollView(size_hint=(1, 0.9))
        inner = BoxLayout(orientation='vertical', size_hint_y=None, spacing=10)
        inner.bind(minimum_height=inner.setter('height'))

        processed_dir = os.path.join(os.getcwd(), "processed")
        if os.path.isdir(processed_dir):
            for file in sorted(os.listdir(processed_dir)):
                if file.lower().endswith((".png", ".jpg", ".jpeg")):
                    inner.add_widget(Image(source=os.path.join(processed_dir, file), size_hint_y=None, height=300))
        else:
            inner.add_widget(Label(text="No processed images found.", size_hint_y=None, height=40))

        scroll.add_widget(inner)
        layout.add_widget(scroll)
        self.add_widget(layout)

class FingerApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(HomeScreen(name='home'))
        sm.add_widget(GalleryScreen(name='gallery'))
        return sm

if __name__ == "__main__":
    FingerApp().run()






