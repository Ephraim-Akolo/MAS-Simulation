from os import name as _OS_Name_
if _OS_Name_ == 'nt':
    from os import environ
    environ['KIVY_GL_BACKEND'] = 'angle_sdl2'
from kivy import require
require("2.1.0")
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.uix.relativelayout import RelativeLayout
from kivy.lang import Builder 
from kivy.clock import Clock
from kivy.factory import Factory
from threading import Thread
from kivy.properties import NumericProperty, BooleanProperty
from assets import *
from mas_lib.agent import AgentCB, AgentB, AgentDG, AgentSource
from parseconfig import MyParser

_HOST = ""
_PORT = 10001

class SimulationArea(RelativeLayout):

    def __init__(self, **kw):
        super().__init__(**kw)
        self.app = App.get_running_app()
        self.broken = []
    
    def create_connect(self, _HOST=_HOST, _PORT=_PORT):
        self.source = AgentSource('SOURCE33V', _HOST, _PORT, broadcast_channel=self.comm_channel)
        self.dg = [
            AgentDG("DG1", _HOST, _PORT, non_blocking_callback=self._agent_state_callback),
            AgentDG("DG2", _HOST, _PORT, non_blocking_callback=self._agent_state_callback)
        ]
        self.cb = [
            AgentCB("CB1A", _HOST, _PORT, non_blocking_callback=self._agent_state_callback),
            AgentCB("CB1B", _HOST, _PORT, non_blocking_callback=self._agent_state_callback),
            AgentCB("CB2A", _HOST, _PORT, non_blocking_callback=self._agent_state_callback),
            AgentCB("CB2B", _HOST, _PORT, non_blocking_callback=self._agent_state_callback),
            AgentCB("CB3A", _HOST, _PORT, non_blocking_callback=self._agent_state_callback),
            AgentCB("CB4A", _HOST, _PORT, non_blocking_callback=self._agent_state_callback),
            AgentCB("CB4B", _HOST, _PORT, non_blocking_callback=self._agent_state_callback),
            AgentCB("CB5A", _HOST, _PORT, non_blocking_callback=self._agent_state_callback),
            AgentCB("CB6A", _HOST, _PORT, non_blocking_callback=self._agent_state_callback),
            AgentCB("CB7A", _HOST, _PORT, non_blocking_callback=self._agent_state_callback),
            AgentCB("CB7B", _HOST, _PORT, non_blocking_callback=self._agent_state_callback),
            AgentCB("CB8A", _HOST, _PORT, non_blocking_callback=self._agent_state_callback),
            AgentCB("CB9A", _HOST, _PORT, non_blocking_callback=self._agent_state_callback),
            AgentCB("CB9B", _HOST, _PORT, non_blocking_callback=self._agent_state_callback),
            AgentCB("CB10A", _HOST, _PORT, non_blocking_callback=self._agent_state_callback)
            ]
        self.b =[
            AgentB("B1", _HOST, _PORT, non_blocking_callback=self._agent_state_callback),
            AgentB("B2", _HOST, _PORT, non_blocking_callback=self._agent_state_callback),
            AgentB("B3", _HOST, _PORT, non_blocking_callback=self._agent_state_callback),
            AgentB("B4", _HOST, _PORT, non_blocking_callback=self._agent_state_callback),
            AgentB("B5", _HOST, _PORT, non_blocking_callback=self._agent_state_callback),
            AgentB("B6", _HOST, _PORT, non_blocking_callback=self._agent_state_callback),
            AgentB("B7", _HOST, _PORT, non_blocking_callback=self._agent_state_callback),
            AgentB("B8", _HOST, _PORT, non_blocking_callback=self._agent_state_callback),
            AgentB("B9", _HOST, _PORT, non_blocking_callback=self._agent_state_callback),
            AgentB("B10", _HOST, _PORT, non_blocking_callback=self._agent_state_callback)
        ]
    
    def _agent_state_callback(self, name, state):
        Clock.schedule_once(lambda x: self._set_agent_state(name, state))

    def _set_agent_state(self, name, state):
        obj = self.ids[name]
        if state == getattr(obj, "agent_attr"):
            return
        # print(obj,name,  state)
        setattr(obj, "agent_attr", state)
    
    def simulate_bus(self, bus_name, voltage):
        t = 2
        if len(bus_name) == 0 :
            m = Factory.Message()
            m.ids.msg.text = "Bus name cannot be empty!"
            m.open()
            Clock.schedule_once(lambda x: m.dismiss(), t)
            return
        if len(voltage) == 0:
            m = Factory.Message()
            m.ids.msg.text = "Voltage cannot be empty!"
            m.open()
            Clock.schedule_once(lambda x: m.dismiss(), t)
            return
        if MyParser.its_B(bus_name) == None:
            m = Factory.Message()
            m.ids.msg.text = "Name entered is not a valid bus name!"
            m.open()
            Clock.schedule_once(lambda x: m.dismiss(), t)
            return
        if not (voltage.isdigit() or voltage.isdecimal()):
            m = Factory.Message()
            m.ids.msg.text = "Volatage must be a number!"
            m.open()
            Clock.schedule_once(lambda x: m.dismiss(), t)
            return
        if bus_name in self.broken:
            m = Factory.Message()
            m.ids.msg.text = f"{bus_name} is already down!"
            m.open()
            Clock.schedule_once(lambda x: m.dismiss(), t)
            return
        Thread(name="simulate_bus", target=self._simulate_bus, args=[bus_name, voltage], daemon=True).start()
    
    def _simulate_bus(self, name, voltage):
        for bus in self.b:
            if bus.name == name:
                bus.broken = True
                bus.voltage = float(voltage)
    
    def refresh(self):
        self.broken = []
        Thread(name="simulation canvas refresh", target= self.source.reset_network, daemon=True).start()
    
    def comm_channel(self, name, state):
        console = self.app.root.ids.sexy_console
        Clock.schedule_once(lambda x: self._comm_channel(name, state, console))
    
    def _comm_channel(self, name, state, console):
        d = console.data[:]
        if len(d) > 100:
            d.pop(0)
        d.append({"text": f"{name}: {state}"})
        console.data = d
        

class MASManager(ScreenManager):
    
    def change_screens(self, screen:str, host, port):
        try:
            self.ids.simulation_canvas.create_connect(host, int(port))
            self.current = screen
        except Exception as e:
            print(e)


class MASApp(App):

    def build(self):
        Builder.load_file("./kv_files/assets.kv")
        return Builder.load_file("./kv_files/mas.kv")

if __name__ == "__main__":
    MASApp().run()
