
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton

class RAULIMobileApp(MDApp):
    def build(self):
        layout = MDBoxLayout(orientation='vertical', padding=20, spacing=10)
        
        # Header
        header = MDLabel(
            text="🤖 RAULI Mobile",
            theme_text_color="Primary",
            size_hint_y=None,
            height=50,
            font_style="H4"
        )
        layout.add_widget(header)
        
        # Status
        status = MDLabel(
            text="🟢 Conectado con RAULI Core",
            theme_text_color="Secondary",
            size_hint_y=None,
            height=30
        )
        layout.add_widget(status)
        
        # Buttons
        chat_btn = MDRaisedButton(
            text="💬 Chat con RAULI",
            on_press=self.open_chat,
            size_hint_y=None,
            height=50
        )
        layout.add_widget(chat_btn)
        
        voice_btn = MDRaisedButton(
            text="🎤 Comando de Voz",
            on_press=self.voice_command,
            size_hint_y=None,
            height=50
        )
        layout.add_widget(voice_btn)
        
        camera_btn = MDRaisedButton(
            text="📷 Cámara",
            on_press=self.open_camera,
            size_hint_y=None,
            height=50
        )
        layout.add_widget(camera_btn)
        
        return layout
    
    def open_chat(self, instance):
        print("💬 Abriendo chat con RAULI...")
    
    def voice_command(self, instance):
        print("🎤 Activando comando de voz...")
    
    def open_camera(self, instance):
        print("📷 Abriendo cámara...")

if __name__ == "__main__":
    RAULIMobileApp().run()
