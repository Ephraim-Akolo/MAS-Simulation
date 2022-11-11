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
    AgentCB("CB4B"),
    AgentCB("CB5A"),
    AgentCB("CB6A"),
    AgentCB("CB7A"),
    AgentCB("CB7B"),
    AgentCB("CB8A"),
    AgentCB("CB9A"),
    AgentCB("CB9B"),
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




for i in ((1, 3), (3, 1), (1, 4), (9, 7), (8 , 10), (4, 9), (2, 3, 8)):
    print("Breaking!!!!!!!!!!!!!!!!!!!!!!!!!!", i[0], "then", i[1], "later")
    input()
    for j in i:
        print("NOW BREAKING!!!!!!!!!!!!!!!!!!!!!!!!!", j)
        b[j-1].broken = True
        b[j-1].voltage = 40
        input()
    source.reset_network()
