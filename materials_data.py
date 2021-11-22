import pandas as pd
import sql_connector
# import math

class FlangeMaterial:
    def __init__(self, material_name, thickness, temperature):
        self.temperature = self.check_number(temperature, "temperature")
        self.material_name = self.check_material_name(material_name)
        self.thickness = self.check_number(thickness, "thickness")
        # Ambient
        self.ambient_data = self.data("ambient")
        self.material_num = self.ambient_data["material_num"]
        self.re = self.get_re()
        self.rm_max = self.ambient_data["Rm_max"]
        self.rm_min = self.ambient_data["Rm_min"]
        self.elongation_l = self.ambient_data["elo_l"]
        self.elongation_t = self.ambient_data["elo_t"]
        # Elevated
        self.elevated_data = self.data("elevated")
        self.reh = self.get_reh()

    @staticmethod
    def check_material_name(material_name):
        if isinstance(material_name, str):
            materials = sql_connector.sql_request(f""" SELECT material_name FROM ambient """)
            materials = [material[0] for material in materials]
            if material_name in materials:
                return material_name
            else: raise ValueError("No such material in Ambient Data Table")
        else: raise ValueError("Invalid material_name data type! Use str.")

    @staticmethod
    def check_number(var, what = ""):
        if isinstance(var, (int,float)):
            return var
        else:
            raise ValueError(f"Invalid {what} data type! Use int or  float")

    def data(self, which_data):
        #which_data = ambient, elevated
        data    = sql_connector.sql_request(f""" SELECT * FROM {which_data} WHERE material_name = '{self.material_name}'""")
        columns = sql_connector.columns(which_data)
        return pd.DataFrame(data, columns = columns).squeeze(axis=0)

    def get_re(self):
        if self.thickness < 16:
            re = self.ambient_data["T_less_than_16"]
        elif self.thickness >= 16 and self.thickness < 40:
            re = self.ambient_data["from16_T_to40"]
        elif self.thickness >= 40 and self.thickness < 60:
            re = self.ambient_data["from40_T_to60"]
        elif self.thickness >= 60 and self.thickness < 100:
            re = self.ambient_data["from60_T_to100"]
        else: raise ValueError("Thickness out of range in Ambient Table Data!")
        if re is None: raise ValueError("No Re for provided thickness!")
        else: return re

    @property
    def max_temp(self):
        max_temp_index =  self.elevated_data.dropna().index[-1]
        return int(max_temp_index[1:])

    def get_reh(self):
        from calculations import linear_interpolation
        if self.temperature > 100 and self.temperature <= self.max_temp:
            for t in range(100,610,50):
                if self.temperature <= t:
                    break
            x0, x1 = t-50, t
            y0, y1 = float(self.elevated_data[f"T{x0}"]), float(self.elevated_data[f"T{x1}"])
        elif self.temperature <= 100:
            x0, x1, y0, y1 = 50, 100, float(self.re), float(self.elevated_data["T100"])

        if isinstance(y0, (int, float)) and isinstance(y1, (int, float)):
            return linear_interpolation(y0, y1, x0, x1, self.temperature)
        else: raise ValueError("Invalid data type in reh()")



print(FlangeMaterial("P195GH", 6.3, 70).reh)
print(FlangeMaterial("P195GH", 6.3, 325).elevated_data)
