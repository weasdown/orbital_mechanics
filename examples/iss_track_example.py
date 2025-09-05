from datetime import datetime

from orbital_mechanics import iss_track, site

# print(iss_track(51.5, 0.51, 50, datetime.today()))

print(site(phi_gd=39.007, lda=104.883, h_ellp=2187))

