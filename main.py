from mas_lib.agent import AgentCB, AgentB
ag = AgentCB("CB7A")
print(ag.neighbors, ag.state)
ab = AgentB("B7")
AgentCB("CB7B")
AgentCB("CB6A")
from time import sleep
for i in range(33):
    ab.voltage = ab.voltage - 1
    sleep(.5)
input()

