from time import sleep
from mas_lib.agent import AgentCB, AgentB, AgentDG, AgentSource

source = AgentSource('SOURCE33V')
dg = [
    AgentDG("DG1"),
    AgentDG("DG2")
]
cb = [
    AgentCB("CB1A"),
    AgentCB("CB1B"),
    AgentCB("CB2A"),
    AgentCB("CB2B"),
    AgentCB("CB3A"),
    AgentCB("CB4A"),
    AgentCB("CB5A"),
    AgentCB("CB6A"),
    AgentCB("CB7A"),
    AgentCB("CB7B"),
    AgentCB("CB8A"),
    AgentCB("CB9A"),
    AgentCB("CB10A")
    ]
b =[
    AgentB("B1"),
    AgentB("B2"),
    AgentB("B3"),
    AgentB("B4"),
    AgentB("B5"),
    AgentB("B6"),
    AgentB("B7"),
    AgentB("B8"),
    AgentB("B9"),
    AgentB("B10")
]

sleep(3)
print("STARTING NETWORK")
source.reset_network()
# sleep(5)
input()
# source.reset_network()
print("Breaking!!!")
b[0].broken = True
b[0].voltage = 0
sleep(5)
b[1].broken = True
b[1].voltage = 0
input()

