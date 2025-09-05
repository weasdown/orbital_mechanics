from dataclasses import dataclass

au_km: float = 149597870  # 1 AU in km

@dataclass
class Planet:
    sma_km: float
    sma_au: float
    eccentricity: float
    inclination: float
    raan: float
    long_perihelion: float
    long_true: float
    period_years: float
    period_days: float
    velocity: float
    radius_equatorial: float
    reciprocal_flattening: float
    gravitational_parameter: float
    mass_rel_earth: float
    mass_kg: float
    rotation: float
    inclination_equator_orbit: float
    j2: float
    j3: float
    j4: float
    density: float

# TODO add other planets (see PDF pg 1068 of Fundamentals)

earth: Planet = Planet(1.0000010178, 149598023, 0.016708617, 0.00000000, 0.00000000, 102.93734808, 100.46644851,
                       0.99997862, 365.2421897, 29.7859, 6378.1363, 0.0033528131, 3.986004415E5, 1.0, 5.9742E24,
                       0.99726968, 23.45, 0.0010826269, -0.0000025323, -0.0000016204, 5.515)
