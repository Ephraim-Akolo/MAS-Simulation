from mas_lib.communications import ComBase
from parseconfig import MyParser
from time import sleep


class AgentCB(ComBase):
    _callback = None
    _state = None
    switch = {0: "broken", 1: "live"}
    neighbors = None
    buses_volatage_rule = {"min": 10, "max": 33}
    def __init__(self, name:str, host:str="", port:int=10001, state:int=1, non_blocking_callback=None) -> None:
        super().__init__(name, host, port)
        self.neighbors = MyParser().get_neighbors(name)
        self._state = self.switch[state]
        self._callback = non_blocking_callback
    
    def broadcast(self, name, state):
        if self.neighbors:
            if name in self.neighbors:
                self._affected_action(name, state)
    
    def broadcast_message(self, message: str):
        return super().broadcast_message(message)
    
    def _affected_action(self, name, state):
        if len(name) == 2 and name[0] == "B":
            voltage = float(state)
            if voltage < self.buses_volatage_rule['min'] or voltage > self.buses_volatage_rule["max"]:
                self.state = 0
                while True:
                    try:
                        self.broadcast_message(self._state)
                    except:
                        print("Failed to broadcast current state!!!")
                        while not self._connect_to_network():
                            sleep(5)
                    else:
                        break
    
    @property
    def state(self):
        return self._state
    
    @state.setter
    def state(self, value):
        if value == 0 or value == 1:
            print(self.name, "changing to ", self.switch[value])
            self._state = self.switch[value]
            if self._callback:
                self._callback(value)
        else:
            print("state can either be '1' or '0'")

class AgentB(ComBase):
    _voltage = None
    def __init__(self, name:str, host:str="", port:int=10001, voltage:float=33) -> None:
        super().__init__(name, host, port)
        self.voltage = voltage
        if not self.schedule_attr_broadcast("voltage", 1):
            raise(Exception("Error Scheduling broadcast"))
    
    @property
    def voltage(self):
        return self._state
    
    @voltage.setter
    def voltage(self, value):
        if value >= 0:
            print(self.name, "changing to ", value)
            self._state = value
        else:
            print("voltage cannot be negative")




if __name__ == "__main__":
    print(AgentCB('B7'))
