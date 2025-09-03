from datetime import datetime

from orbital_mechanics import iss_track

print(iss_track(51.5, 0.51, 50, datetime.today()))
