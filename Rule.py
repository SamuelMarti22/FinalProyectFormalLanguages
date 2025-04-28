class Rule:
    def __init__(self,simboloProduccion,producion):
        self.simboloProduccion = simboloProduccion
        self.produccion = producion
        self.first = None

    def get_production_symbol(self):
        return self.simboloProduccion

    def get_production(self):
        return self.produccion

    def get_first(self):
        return self.first
    
    def set_first(self, first):
        self.first = first
