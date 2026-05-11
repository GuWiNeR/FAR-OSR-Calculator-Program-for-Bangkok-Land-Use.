from data_regulation import far_osr_data
class calculatorareas:
    def __init__(self, project_create):
        self.name = project_create['name']
        self.area = float(project_create['areas'])
        self.sub_zoning = project_create['sub_zoning']

        regulation = far_osr_data.get(self.sub_zoning, {"far": 0, "osr": 0})
        self.far = regulation['far']
        self.osr = regulation['osr']

    def calculate_far(self, bonus = False):
        result = self.area * self.far
        new_far = self.far + (self.far*(20/100))
        if bonus == True:
            return self.area * new_far
        
        else:
            return result
    
    def calculate_osr(self):
        return self.area * (self.osr/100)

    