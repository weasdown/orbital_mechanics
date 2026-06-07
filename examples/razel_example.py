from datetime import datetime

import numpy as np

from orbital_mechanics import razel, IERS

iss_r_eci = np.array([])
iss_v_eci = np.array([])

iers = IERS()

lat = 51.761146
long = -1.255242
height = 50

outputs = razel(iss_r_eci, iss_v_eci, datetime.now(), lat, long, height)
print(outputs)
