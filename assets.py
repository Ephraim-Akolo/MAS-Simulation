
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.recycleview import RecycleView
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, StringProperty, BooleanProperty
from parseconfig import LINE_VOLTAGE, MIN_VOLATAGE

class MInput(TextInput):
    pass


class MLabel(Label):
    pass


class NLabel(Label):
    pass


class SourceWidget(NLabel):
    state = BooleanProperty(False)
    agent_attr = NumericProperty(33)
    def on_agent_attr(self, obj, voltage):
        if voltage > LINE_VOLTAGE or voltage < MIN_VOLATAGE:
            self.state = False
        else:
            self.state = True


class Console(RecycleView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.data = []


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
    agent_attr = StringProperty("")
    
    def on_agent_attr(self, obj, value):
        if value == "live":
            self.state = True
        elif value == "broken":
            self.state = False
        else:
            raise(Exception(f"{self} got invalid cb state!"))


class BusWidget(MLabel):
    state = BooleanProperty(True)
    name = StringProperty("")
    agent_attr = NumericProperty(32)
    rotate = NumericProperty(0)
    def on_agent_attr(self, obj, voltage):
        if voltage > LINE_VOLTAGE or voltage < MIN_VOLATAGE:
            self.state = False
            self.parent.broken.append(self.name)
        else:
            self.state = True
            try:
                self.parent.broken.remove(self.name)
            except:
                pass
