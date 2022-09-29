from mas_lib.communications import ComBase
from parseconfig import MyParser
from time import sleep


class AgentCB(ComBase):
    _extras = None
    _state = None
    switch = {0: "broken", 1: "live"}
    neighbors = None
    buses_volatage_rule = {"min": 0, "max": 33}
    def __init__(self, name:str, host:str="", port:int=10001, state:int=1, extras:dict=None) -> None:
        super().__init__(name, host, port)
        self.neighbors = MyParser().get_neighbors(name)
        self._state = self.switch[state]
    
    def broadcast(self, name, state):
        if self.neighbors:
            if name in self.neighbors:
                self._affected_action(name, state)
    
    def broadcast_message(self, message: str):
        return super().broadcast_message(message)
    
    def _affected_action(self, name, state):
        if len(name) == 2 and name[0] == "B":
            voltage = int(state)
            if voltage < self.buses_volatage_rule['min'] or voltage > self.buses_volatage_rule["max"]:
                self._state = self.switch[0]
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
        else:
            print("state can either be '1' or '0'")




if __name__ == "__main__":
    print(AgentCB('B7'))
