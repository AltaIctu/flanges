
#Obliczenia kołnierzy wg EN 1591
P_1 = 9.45 #Cisnienie proby
P_2 = 6.3 #Cisnienie pracy

class Project_Data:
    def __init__(self, temperature, design_pressure):
        self.temperature = temperature
        self.design_pressure = design_pressure
