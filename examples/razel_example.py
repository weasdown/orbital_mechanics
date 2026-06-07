from datetime import datetime

import numpy as np

from orbital_mechanics import razel, IERS

iss_r_eci = np.array([])
iss_v_eci = np.array([])

iers = IERS()
poles = iers.poles()
x_p = poles[0]
y_p = poles[1]

lat = 51.761146
long = -1.255242
height = 50

outputs = razel(iss_r_eci, iss_v_eci, datetime.now(), iers.d_ut1(), iers.d_at(), x_p, y_p, lat, long, height)
print(outputs)
