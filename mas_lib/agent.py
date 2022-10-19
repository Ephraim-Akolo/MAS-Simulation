from mas_lib.communications import ComBase
from parseconfig import MyParser, LINE_VOLTAGE, MIN_VOLATAGE, state_broken_, state_live_
from time import sleep

refresh_time = 1

class AgentCB(ComBase):

    _state = None

    switch = {0: state_broken_, 1: state_live_}

    neighbors = None

    buses_volatage_rule = {"min": MIN_VOLATAGE, "max": LINE_VOLTAGE}

    id = None

    _agents_states = {}

    _dg_boundary = None

    supply_line:str = None

    _supply_is_DG = 0

    def __init__(self, name:str, host:str="", port:int=10001, state:int=1, non_blocking_callback=None) -> None:
        self._state:str = self.switch[state]
        id = self.its_CB(name)
        if not id:
            raise(Exception("Not a valid CircuitBreaker Name!"))
        if n:=MyParser.i_am_boundary_cb(name):
            self._dg_boundary = n
        self.id = id
        self.neighbors = MyParser.get_neighbors(name)
        self.supply_line = MyParser.get_all_agents_from_source(name)
        self._agents_states = MyParser.init_agent_dict()
        self._callback = non_blocking_callback
        super().__init__(name, host, port)
        if not self.schedule_attr_broadcast("_state", refresh_time): # make sure dependent variables are initialized before Threads start broadcasting them!
            raise(Exception("Error Scheduling broadcast"))
        
    
    def broadcast(self, name, state):
        self._agents_states[name] = state
        if self.its_SOURCE(name) and state == 'r':
            self._reset()
        elif self._dg_boundary and self._both_dg_on():
            self.state = 0
        elif self.neighbors and name in self.neighbors and self.its_B(name) != None:
            self._affected_action(name, state)

    def broadcast_message(self, message: str):
        return super().broadcast_message(message)
    
    def _affected_action(self, name, state):
        voltage = float(state)
        if voltage < self.buses_volatage_rule['min'] or voltage > self.buses_volatage_rule["max"]:
            if self._supply_is_DG > 3:
                self.state = 0
                self._supply_is_DG = 1000
                return
            if self._around_first_bus():
                self.state = 0
            else:
                self.state = 1
                self._supply_is_DG += 1
        
    def _both_dg_on(self) -> bool:
        if self._dg_boundary and float(self._agents_states[self._dg_boundary[0]]) and float(self._agents_states[self._dg_boundary[1]]):
            return True
        return False

    def _around_first_bus(self):
        # If a circuit breaker around a bus in the supply line is broken, return true else return false.
        for agent in self.supply_line:
            id = self.its_B(agent) 
            if id and float(self._agents_states[agent]) == 0:
                return id == self.id 
        # for the circuit breakers that are before their buses... they will escape the above conditions so handle them seperatly.
        if not float(self._agents_states[f"B{self.id}"]):
            return True
        return False # otherwise return false

    def _reset(self):
        self.state = 1
        self._supply_is_DG = 0
        self.buses_volatage_rule = {"min": MIN_VOLATAGE, "max": LINE_VOLTAGE}
        for key in self._agents_states.keys():
            self._agents_states[key] = MyParser.get_r_val(key)
    
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

    broken = False

    _agents_states = {}

    neighboring_sources:tuple = {None}

    _m = False

    def __init__(self, name: str, host: str = "", port: int = 10001, voltage: float = LINE_VOLTAGE, non_blocking_callback=None) -> None:
        id = self.its_B(name)
        if not id:
            raise(Exception("Not a valid Bus Name!"))
        self.id = id
        self._callback = non_blocking_callback
        self.main_line = MyParser.get_all_agents_from_source(name)
        self.dg_line = MyParser.get_all_agents_from_source(name, False)
        self.neighboring_sources = MyParser.get_pri_sec_sources(name)
        self._agents_states = MyParser.init_agent_dict()
        super().__init__(name, host, port, voltage)
        if not self.schedule_attr_broadcast("voltage", refresh_time):
            raise(Exception("Error Scheduling broadcast"))

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
            raise(Exception(f"Power from Generator on while Source is active!!!"))
        elif m or n:
            return True
        else:
            return False
    
    def _no_breakage_from_line(self, dg_line=False):
        _line = self.dg_line[:-1] if dg_line else self.main_line[:-1]
        for agent in _line:
            if self.its_CB(agent) and self._agents_states[agent] == AgentCB.switch[0]:# do not use AgentCB class
                return False
            # elif self.its_B(agent) and float(self._agents_states[agent]) == 0:
            #     return False
            elif self.its_SOURCE(agent) and float(self._agents_states[agent]) == 0:
                return False
            elif self.its_DG(agent) and float(self._agents_states[agent])== 0:
                return False
        return True
    
    
    def _reset(self):
        self.broken = False
        self._m = False
        self.voltage = LINE_VOLTAGE
        for key in self._agents_states.keys():
            self._agents_states[key] = MyParser.get_r_val(key)

class AgentSource(AgentPower):

    id = None

    def __init__(self, name: str, host: str = "", port: int = 10001, voltage: float = LINE_VOLTAGE, non_blocking_callback=None) -> None:
        id = self.its_SOURCE(name)
        if not id:
            raise(Exception("Not a valid Source Name!"))
        self.id = id
        self._callback = non_blocking_callback
        super().__init__(name, host, port, voltage)
        # if not self.schedule_attr_broadcast("voltage", refresh_time):
        #     raise(Exception("Error Scheduling broadcast"))
    
    def broadcast(self, name:str, state:str): # Override function
        # if state.isnumeric() and float(state) == 0:
        #     print(name, state)
        # elif name[:2] == "DG" or (name[:2] == "CB" and state== "broken") :
        #     print(name, state)
        pass
        
    
    def reset_network(self):
        for _ in range(5):
            self.broadcast_message(str("r"))
            sleep(refresh_time/5)


class AgentDG(AgentPower):

    _designations:list = None

    _after_designations:list = None

    _response_time:float = None

    _cb_around_b:set = None

    broken_buses:list = None

    _agents_states = {}

    main_line = None

    id = None

    _first_cb = None

    ss2d = []

    def __init__(self, name: str, host: str = "", port: int = 10001, voltage: float = 0, response_time=0.0, non_blocking_callback=None) -> None:
        id = self.its_DG(name)
        if not id:
            raise(Exception("Not a valid Generator Name!"))
        self.id = id
        self._designations = MyParser.get_dg_designations(name)
        self._after_designations = [self.its_B(i) for i in MyParser.get_after_dg_designations(name)]
        self.main_line = MyParser.get_all_agents_from_source(name)
        self.ss2d = [i for i in self.main_line[1:-1] if (i not in self._designations) and self.its_B(i)]
        self._first_cb = MyParser.get_dg_first_cb(name)
        self._agents_states = MyParser.init_agent_dict()
        self._callback = non_blocking_callback
        self._response_time = response_time
        self.broken_buses = []
        cb = []
        for bus in self._designations:
            cb += MyParser.get_neighbors(bus)
        self._cb_around_b = set(cb)
        super().__init__(name, host, port, voltage)
        if not self.schedule_attr_broadcast("voltage", refresh_time):
            raise(Exception("Error Scheduling broadcast"))
        
    
    def broadcast(self, name: str, state: str):
        self._agents_states[name] = state
        if self.its_SOURCE(name) and state == 'r':
            self._reset()
            return
        dg = self.its_DG(name)
        _exist =self.supply_path_exist()
        N = 1
        if self._designations and _exist:
            if name in self._cb_around_b and state == AgentCB.switch[0] and self.voltage == 0: # AgentCB should not be here and class should be independent of other agents.
                # line is broken
                N = 2
                self._affected_action_1(name, 0)
            elif dg and dg < self.id and float(state) == float(LINE_VOLTAGE):
                # DG behind is on, means breakage and must therefore be on too
                N = 3
                self._affected_action_2()
            elif dg and dg < self.id and float(state) == 0 and len(self.broken_buses) == 0:
                # DG behind is off and no broken buses, turn off.
                N = 4
                self._affected_action_3()
            # elif name in self.broken_buses and state == AgentCB.switch[1] and self.voltage == LINE_VOLTAGE:
            #     # Circuit breaker is restored (Assuming after bus is fixed)
            #     N = 5
            #     self._affected_action_1(name, 1)
            elif dg and dg < self.id and float(state) == 0 and self._power2desg_broken():
                self.voltage = LINE_VOLTAGE

        elif not _exist and self.voltage != 0:
            self.voltage = 0
            N = 6
    
    def _affected_action_1(self, name, state):
        if state:
            self.broken_buses.remove(name)
            self.voltage = 0
        else:
            if (self.its_CB(name) not in self._after_designations):
                if name not in self.broken_buses:
                    self.broken_buses.append(name)
                sleep(self._response_time)
                self.voltage = LINE_VOLTAGE
    
    def _affected_action_2(self):
        # sleep(self._response_time)
        if not self._no_breakage_from_line():
            self.voltage = LINE_VOLTAGE
    
    def _affected_action_3(self):
        self.voltage = 0
    
    def _no_breakage_from_line(self):
        _line = self.main_line[:-1]
        for agent in _line:
            if self.its_CB(agent) and self._agents_states[agent] == AgentCB.switch[0]:# do not use AgentCB class
                return False
            elif self.its_B(agent) and float(self._agents_states[agent]) == 0:
                return False
            elif self.its_SOURCE(agent) and float(self._agents_states[agent]) == 0:
                return False
            elif self.its_DG(agent) and float(self._agents_states[agent])== 0:
                return False
        return True
    
    def supply_path_exist(self):
        return self._agents_states[self._first_cb] == AgentCB.switch[1]
    
    def _power2desg_broken(self):
        for b in self.ss2d:
            if float(self._agents_states[b]) == 0:
                return True
        return False
    
    def _reset(self):
        self.voltage = 0
        self.broken_buses = []
        for key in self._agents_states.keys():
           self._agents_states[key] = MyParser.get_r_val(key)


if __name__ == "__main__":
    print(AgentCB('B7'))
