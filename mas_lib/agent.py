from mas_lib.communications import ComBase
from parseconfig import MyParser
from time import sleep

LINE_VOLTAGE = 33

MIN_VOLATAGE = 10


class AgentCB(ComBase):

    _callback = None

    _state = None

    switch = {0: "broken", 1: "live"}

    neighbors = None

    buses_volatage_rule = {"min": MIN_VOLATAGE, "max": LINE_VOLTAGE}

    id = None

    _agents_states = {}

    supply_line:str = None

    def __init__(self, name:str, host:str="", port:int=10001, state:int=1, non_blocking_callback=None) -> None:
        super().__init__(name, host, port)
        self._state:str = self.switch[state]
        id = self.its_CB(name)
        if not id:
            raise(Exception("Not a valid CircuitBreaker Name!"))
        if not self.schedule_attr_broadcast("_state", 1): # make sure dependent variables are initialized before Threads start broadcasting them!
            raise(Exception("Error Scheduling broadcast"))
        self.id = id
        self.neighbors = MyParser.get_neighbors(name)
        self.supply_line = MyParser.get_all_agents_from_source(name)
        self._callback = non_blocking_callback
        
    
    def broadcast(self, name, state):
        self._agents_states[name] = state
        if self.its_SOURCE(name) and state == 'r':
            self._reset()
        elif self.neighbors and name in self.neighbors and self.its_B(name) != None:
            self._affected_action(name, state)

    def broadcast_message(self, message: str):
        return super().broadcast_message(message)
    
    def _affected_action(self, name, state):
        voltage = float(state)
        if voltage < self.buses_volatage_rule['min'] or voltage > self.buses_volatage_rule["max"]:
            if self._around_first_bus():
                self.state = 0
            else:
                self.state = 1
            # implement what happens on second breakage from generator. (circuit breaker needs to break to kill buses from dg source)
        
    def _around_first_bus(self):
        # If a circuit breaker around a bus in the supply line is broken, return true else return false.
        for agent in self.supply_line:
            if id:=self.its_B(agent) and float(self._agents_states[agent]) == 0:
                return id == self.id
        # for the circuit breakers that are before their buses... they will escape the above conditions so handle them seperatly.
        try:
            if not float(self._agents_states[f"B{self.id}"]):
                return True
        except:
            pass
        return False # otherwise return false

    def _reset(self):
        self.state = 1
        self.buses_volatage_rule = {"min": MIN_VOLATAGE, "max": LINE_VOLTAGE}
        for key in self._agents_states.keys():
            if self.its_B(key):
                self._agents_states[key] = str(LINE_VOLTAGE)
            elif self.its_CB(key):
                self._agents_states[key] = AgentCB.switch[1]
            elif self.its_DG(key):
                self._agents_states[key] = str(0)
            elif self.its_SOURCE(key):
                self._agents_states[key] = str(LINE_VOLTAGE)
    
    @property
    def state(self):
        return self._state
    
    @state.setter
    def state(self, value):
        if value == 0 or value == 1:
            self._state = self.switch[value]


class AgentPower(ComBase):

    _voltage = None

    def __init__(self, name:str, host:str="", port:int=10001, voltage:float=LINE_VOLTAGE) -> None:
        super().__init__(name, host, port)
        self.voltage = voltage
    
    @property
    def voltage(self):
        return self._state
    
    @voltage.setter
    def voltage(self, value):
        if value >= 0 or value <= LINE_VOLTAGE:
            self._state = value


class AgentB(AgentPower):

    _voltage:float = None

    id = None

    main_line = []

    dg_line = []

    broken = True

    _agents_states = {}

    neighboring_sources:tuple = {None}

    _m = True

    def __init__(self, name: str, host: str = "", port: int = 10001, voltage: float = LINE_VOLTAGE) -> None:
        super().__init__(name, host, port, voltage)
        id = self.its_B(name)
        if not id:
            raise(Exception("Not a valid Bus Name!"))
        if not self.schedule_attr_broadcast("voltage", 1):
            raise(Exception("Error Scheduling broadcast"))
        self.id = id
        self.main_line = MyParser.get_all_agents_from_source(name)
        self.dg_line = MyParser.get_all_agents_from_source(name, False)
        self.neighboring_sources = MyParser.get_pri_sec_sources(name)
        

    def broadcast(self, name: str, state: str):
        self._agents_states[name] = state
        if self.its_SOURCE(name) and state == 'r':
            self._reset()
        elif not self.broken:
            if self._no_breakage_from_source():
                self.voltage = LINE_VOLTAGE
            else:
                self.voltage = 0
    
    def _no_breakage_from_source(self) -> bool:
        n = self._no_breakage_from_line(True)
        self._m = m = self._no_breakage_from_line()
        if m and n:
            raise(Exception("Power from Generator on while Source is active!!!"))
        elif m or n:
            return True
        else:
            return False
    
    def _no_breakage_from_line(self, dg_line=False):
        _line = self.dg_line[:-1] if dg_line else self.main_line[:-1]
        for agent in _line:
            try:
                if self.its_CB(agent) and self._agents_states[agent] == AgentCB.switch[0]:# do not use AgentCB class
                    return False
                # elif self.its_B(agent) and float(self._agents_states[agent]) == 0:
                #     return False
                elif self.its_SOURCE(agent) and float(self._agents_states[agent]) == 0:
                    return False
                elif self.its_DG(agent) and float(self._agents_states[agent])== 0:
                    return False
            except Exception as e:
                print(e)
                pass
        return True
    
    
    def _reset(self):
        self.broken = False
        self._m = True
        self.voltage = LINE_VOLTAGE
        for key in self._agents_states.keys():
            if self.its_B(key):
                self._agents_states[key] = str(LINE_VOLTAGE)
            elif self.its_CB(key):
                self._agents_states[key] = AgentCB.switch[1]
            elif self.its_DG(key):
                self._agents_states[key] = str(0)
            elif self.its_SOURCE(key):
                self._agents_states[key] = str(LINE_VOLTAGE)


class AgentSource(AgentPower):

    id = None

    def __init__(self, name: str, host: str = "", port: int = 10001, voltage: float = LINE_VOLTAGE) -> None:
        super().__init__(name, host, port, voltage)
        id = self.its_SOURCE(name)
        if not id:
            raise(Exception("Not a valid Source Name!"))
        if not self.schedule_attr_broadcast("voltage", 1):
            raise(Exception("Error Scheduling broadcast"))
        self.id = id
        
    
    def reset_network(self):
        for i in range(10):
            self.broadcast_message(str("r"))
            sleep(0.1)


class AgentDG(AgentPower):

    _designations:list = None

    _response_time:float = None

    _cb_around_b:set = None

    broken_buses:list = None

    id = None

    def __init__(self, name: str, host: str = "", port: int = 10001, voltage: float = 0, response_time=0.0) -> None:
        super().__init__(name, host, port, voltage)
        id = self.its_DG(name)
        if not id:
            raise(Exception("Not a valid Generator Name!"))
        if not self.schedule_attr_broadcast("voltage", 1):
            raise(Exception("Error Scheduling broadcast"))
        self.id = id
        self._designations = MyParser.get_dg_designations(name)
        self._response_time = response_time
        self.broken_buses = []
        cb = []
        for bus in self._designations:
            cb += MyParser.get_neighbors(bus)
        self._cb_around_b = set(cb)
        
    
    def broadcast(self, name: str, state: str):
        if self.its_SOURCE(name) and state == 'r':
            self._reset()
            return
        dg = self.its_DG(name)
        if self._designations:
            if name in self._cb_around_b and state == AgentCB.switch[0] and self.voltage == 0: # AgentCB should not be here and class should be independent of other agents.
                # line is broken
                self._affected_action_1(name, 0)
            elif dg and dg < self.id and float(state) == float(LINE_VOLTAGE):
                # DG behind is on, means breakage and must therefore be on too
                self._affected_action_2()
            elif dg and dg < self.id and float(state) == 0 and len(self.broken_buses) == 0:
                # DG behind is off and no broken buses, turn off.
                self._affected_action_3()
            elif name in self.broken_buses and state == AgentCB.switch[1] and self.voltage == LINE_VOLTAGE:
                # Circuit breaker is restored (Assuming after bus is fixed)
                self._affected_action_1(name, 1)
    
    def _affected_action_1(self, name, state):
        if state:
            self.broken_buses.remove(name)
            self.voltage = 0
        else:
            if name not in self.broken_buses:
                self.broken_buses.append(name)
            sleep(self._response_time)
            self.voltage = LINE_VOLTAGE
    
    def _affected_action_2(self):
        # sleep(self._response_time)
        self.voltage = LINE_VOLTAGE
    
    def _affected_action_3(self):
        self.voltage = 0
    
    def _reset(self):
        self.voltage = 0
        self.broken_buses = []


if __name__ == "__main__":
    print(AgentCB('B7'))
