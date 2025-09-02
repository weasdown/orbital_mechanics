import orbital_mechanics as om

iers = om.IERS()

print(f'Bulletin C:\n{iers.bulletin_c()}\n\n')
print(f'Bulletin D:\n{iers.bulletin_d()}')
