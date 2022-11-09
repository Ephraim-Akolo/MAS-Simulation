# MAS-Simulation
A system for Power Distribution

## Implementation steps

Firstly, a suitable communication protocol was determined to be the TCP and the TCP server was built in python programming language to take a broadcast message sent from one agent and broadcast it to the remaining agents in the network. 
The whole network was represented in a JSON format in a JSON file so that all agents in the network can locate the position of any other agent in the network so that they can take independent decisions based on the state and position of an agent.
In order simulate the flow of electricity, the bus agent class was created in the python programming language to always broadcast their current voltages at all times so that other agents know the voltage in any bus at any given time.
Then the Circuit Breakers agent class was built also in the python programming language to control their respective circuit breakers in the network. They broadcast their states and also receive the states of other agents, then process that information to decide whether to trip off or not. The circuit breaker will trip off it it believes their is a problem (based of the operating current and voltage) in the neighbouring bus to isolate the bus from the rest of the system.
The Generator agent class was then built also in the python programming language to control the system generators, they also brodcast their states and also received the states of other agents in the system. They process the states of the circuit breaker and turn on if any unaffected area has no electricity because of a problem in the line.
Then a graphical user interface was created in the kivy framework of the python programming language to represent the states of all agents in the network and aid visualization. The graph of the fault was generated using the matplotlib module of the python programming language.
