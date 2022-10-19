
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.recycleview import RecycleView
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, StringProperty, BooleanProperty

class MInput(TextInput):
    pass


class MLabel(Label):
    pass


class NLabel(Label):
    pass


class SourceWidget(NLabel):
    state = BooleanProperty(False)


class Console(RecycleView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.data = [{'text': str(x)} for x in range(100)]


class DashBoard(RecycleView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.data = [{'text': str(x)} for x in range(100)]


class LineWidget(Widget):
    horizontal = BooleanProperty(True)
    line_a = NumericProperty(0)
    line_b = NumericProperty(0)
    line_c = NumericProperty(0)
    line_d = NumericProperty(0)

    def on_size(self, obj, size):
        self._adjust_line()
    
    def on_pos(self, obj, pos):
        self._adjust_line()

    def _adjust_line(self):
        if self.horizontal:
            self.line_a = self.x
            self.line_c = self.x + self.width
            self.line_b = self.line_d= self.y + self.height//2
        else:
            self.line_a = self.line_c = self.x + self.width//2
            self.line_b = self.y
            self.line_d = self.y + self.height


class CBWidget(Widget):
    state = BooleanProperty(True)


class BusWidget(MLabel):
    state = BooleanProperty(True)
    name = StringProperty("")
    voltage = NumericProperty(33)
    rotate = NumericProperty(0)
