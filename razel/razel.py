# Calculates spacecraft azimuth and elevation from a site on the Earth.
# For full details, see Algorithm 27 (RAZEL) on page 265 of Fundamentals of Astrodynamics and Applications (4th ed.) by David A Vallado.

def razel():
    """
    Calculates a spacecraft's range, azimuth, elevation, and the rates of these, from a point on the ground.
    
    Inputs:
    r_ECI, v_ECI, yr, mo, day, UTC, ΔUT1, ΔAT, x_p, y_p, φ_gd, λ, h_ellp

    Outputs: 
    ρ, β, el, ρ_dot, β_dot, el_dot

    Based on Algorithm 27 on page 265 of Fundamentals of Astrodynamics and Applications (4th ed.) by David A Vallado.
    """
    pass

if __name__ == '__main__':
    pass
