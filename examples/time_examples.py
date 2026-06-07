from datetime import datetime

from orbital_mechanics import conv_time

ut1, tai, tt, tdb, t_ut1, t_tt, t_tdb = conv_time(date_time=datetime(2004, 5, 14, 16, 43), d_ut1=-0.463326, d_at=32)
print(f'ut1 = {ut1.strftime("%H:%M:%S.%f")}\n'
      f'tai = {tai.strftime("%H:%M:%S.%f")}\n'
      f'tt = {tt.strftime("%H:%M:%S.%f")}\n'
      f'tdb = {tdb.strftime("%H:%M:%S.%f")}\n'
      f'{t_ut1 = }\n'
      f'{t_tt = }\n'
      f'{t_tdb = }\n')
