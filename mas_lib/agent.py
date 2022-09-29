from communications import ComBase


class Agent(ComBase):
    def __init__(self, name, host=..., port=10001) -> None:
        super().__init__(name, host, port)
    
    def broadcast(self, name, state):
        return super().broadcast(name, state)
    
    def broadcast_message(self, message: str):
        return super().broadcast_message(message)
