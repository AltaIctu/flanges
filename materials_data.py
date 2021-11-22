
from sql_connector import sql_request
# import math

#Obliczenia kołnierzy wg EN 1591
P_1 = 9.45 #Cisnienie proby
P_2 = 6.3 #Cisnienie pracy


print(sql_request(""" SELECT * FROM ambient """))