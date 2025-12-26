from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.core.window import Window

class Root(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.add_widget(Label(text="Hello! Try closing the window."))
        Window.bind(on_request_close=self.on_request_close)

    def on_request_close(self, *args):
        popup = Popup(
            title='Confirm Exit',
            size_hint=(0.5, 0.3),
            auto_dismiss=False
        )
        box = BoxLayout(orientation='vertical', spacing=10, padding=10)
        box.add_widget(Label(text='Are you sure you want to exit?'))
        btns = BoxLayout(size_hint_y=0.3, spacing=10)
        btn_yes = Button(text='Yes')
        btn_no = Button(text='No')
        btns.add_widget(btn_yes)
        btns.add_widget(btn_no)
        box.add_widget(btns)
        popup.content = box

        def do_exit(*a):
            popup.dismiss()
            App.get_running_app().stop()  # This will close the app

        def do_cancel(*a):
            popup.dismiss()

        btn_yes.bind(on_release=do_exit)
        btn_no.bind(on_release=do_cancel)
        popup.open()
        return True 
class TestApp(App):
    def build(self):
        return Root()

if __name__ == '__main__':
    TestApp().run()
