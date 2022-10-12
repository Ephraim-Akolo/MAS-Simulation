from kivy import require
require("2.1.0")
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.uix.relativelayout import RelativeLayout
from kivy.lang import Builder 
from kivy.clock import Clock

class SimulationArea(RelativeLayout):
    pass


class MASManager(ScreenManager):
    def on_kv_post(self, base_widget):
        Clock.schedule_once(lambda x: self.change_screens("simulation_screen"), 3)
        return super().on_kv_post(base_widget)
    
    def change_screens(self, screen:str):
        self.current = screen


class MASApp(App):

    def build(self):
        Builder.load_file("./kv_files/assets.kv")
        return Builder.load_file("./kv_files/mas.kv")


if __name__ == "__main__":
    MASApp().run()
