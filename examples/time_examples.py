from datetime import datetime

from orbital_mechanics import conv_time

outputs = conv_time(date_time=datetime(2004, 5, 14, 16, 43), d_ut1=-0.463326, d_at=32)
print(outputs)
