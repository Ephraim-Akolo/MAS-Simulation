
from kivy.uix.textinput import TextInput
from kivy.uix.recycleview import RecycleView

class MInput(TextInput):
    pass


class Console(RecycleView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.data = [{'text': str(x)} for x in range(100)]

class DashBoard(RecycleView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.data = [{'text': str(x)} for x in range(100)]