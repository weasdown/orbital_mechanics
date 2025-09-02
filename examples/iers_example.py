import orbital_mechanics as om

iers = om.IERS()

# print(f'Bulletin C:\n{iers.bulletin_c()}\n\n')
# print(f'Bulletin D:\n{iers.bulletin_d()}\n\n')
#
# print(f'ΔUT1 from IERS: {iers.d_ut1()}')
print(f'ΔAT from IERS: {iers.d_at()}')
