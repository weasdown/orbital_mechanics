# Calculates spacecraft azimuth and elevation from a site on the Earth.
# For full details, see Algorithm 27 (RAZEL) on page 265 of Fundamentals of Astrodynamics and Applications (4th ed.) by David A Vallado.

import numpy as np
from datetime import datetime


# TODO add missing argument type hints once types known.
def razel(r_ECI: np.ndarray, v_ECI: np.ndarray, datetime: datetime, dUT1, dAT, x_p, y_p, phi_gd, lda, h_ellp) -> list[float]:
    """
    Calculates a spacecraft's range, azimuth, elevation, and the rates of these, from a point on the ground.
    
    Inputs:
    r_ECI, v_ECI, yr, mo, day, UTC, ΔUT1, ΔAT, x_p, y_p, φ_gd, λ, h_ellp

    Outputs: 
    ρ, β, el, ρ_dot, β_dot, el_dot

    Based on Algorithm 27 on page 265 of Fundamentals of Astrodynamics and Applications (4th ed.) by David A Vallado.
    """

    # FIXME fix placeholder values for outputs.
    rho: float = 0.0
    beta: float = 0.0
    el: float = 0.0

    rho_dot: float = 0.0
    beta_dot: float = 0.0
    el_dot: float = 0.0

    return [rho, beta, el, rho_dot, beta_dot, el_dot]


# TODO add missing argument type hints once types known.
def fk5(r_ECI: np.ndarray, v_ECI: np.ndarray, datetime: datetime, dUT1, dAT, x_p, y_p) -> list[np.ndarray]:
    """
    Converts position and velocity vectors in the ECI frame to the ECEF frame.
    """
    
    raise NotImplementedError

    # # FIXME fix placeholder values for outputs.
    # r_ecef: np.ndarray = np.ndarray([])
    # v_ecef: np.ndarray = np.ndarray([])

    # return [r_ecef, v_ecef]


# TODO add missing argument type hints once types known.
def site(phi_gd, lda, h_ellp) -> np.ndarray:
    """
    Calculates the ECEF position vector for a site on the Earth's surface.
    """
    
    raise NotImplementedError

    # # FIXME fix placeholder value for output.
    # r_site_ecef: np.ndarray = np.ndarray([])
    # return r_site_ecef


if __name__ == '__main__':
    pass
