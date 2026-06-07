import orbital_mechanics as om

iers = om.IERS()

print(f'ΔUT1 from IERS: {iers.d_ut1()}')
print(f'ΔAT from IERS: {iers.d_at()}')

print(f'poles from IERS: {iers.poles()}')
