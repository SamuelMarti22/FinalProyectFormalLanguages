class State:
    def __init__(self,numberState,setRules):
        self.numberState = numberState
        self.setRules = setRules
        self.previusState = None
        self.symbol = None

    def get_number_state(self):
        return self.numberState
    def get_set_rules(self):
        return self.setRules
    def get_previus_state(self):
        return self.previusState
    def get_symbol(self):
        return self.symbol
    def set_previus_state(self, previusState):
        self.previusState = previusState
    def set_symbol(self, symbol):
        self.symbol = symbol