import json


class MyParser:
    '''
    Parses the config file.
    '''
    _model = {}

    def __init__(self, file_loc="./config.json") -> None:
        with open(file_loc, 'r') as fp:
            _model = json.load(fp)
            for key, value in _model.items():
                self._model[key] = value

    @staticmethod
    def _print_model(model):
        if not len(model):
            print("dead end!")
            return
        keys = list(model.keys())
        print(keys)
        for key in keys:
            MyParser._print_model(model[key])

    def print_model(self):
        '''
        Unrolls and display the model on the console.
        '''
        model = self._model["SystemModel"]
        MyParser._print_model(model)

    @classmethod
    def _get_neighbors(cls, model:dict, id:str, prev_key:dict) -> list:
        if not len(model):
            return
        keys = list(model.keys())
        if id not in keys:
            for key in keys:
                neigbors = cls._get_neighbors(model[key], id, key)
                if neigbors:
                    return neigbors
        else:
            if prev_key:
                return [prev_key] + list(model[id].keys())
            return list(model[id].keys())

    @classmethod
    def get_neighbors(cls, id:str) -> list:
        '''
        returns the surrounding neighbors of `id` in the `model`.
        '''
        model = cls._model
        return cls._get_neighbors(model, id, None)
        



if __name__ == "__main__":
    MyParser().print_model()
    print(MyParser().get_neighbors('B7'))
