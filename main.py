from time import sleep
from mas_lib.agent import AgentCB, AgentB, AgentDG, AgentSource

source = AgentSource('SOURCE33V')
dg = [
    AgentDG("DG1")
]
cb = [
    AgentCB("CB1A"),
    AgentCB("CB1B"),
    AgentCB("CB2A"),
    AgentCB("CB2B"),
    AgentCB("CB3A"),
    AgentCB("CB4A")
    ]
b =[
    AgentB("B1"),
    AgentB("B2"),
    AgentB("B3"),
    AgentB("B4"),
]

sleep(3)
print("STARTING NETWORK")
source.reset_network()
# sleep(5)
input()
# source.reset_network()
print("Breaking!!!")
b[1].broken = True
b[1].voltage = 0
input()
print("integrating cb4a")
cb[-1].dggg = True
input()

