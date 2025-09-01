# Calculates spacecraft azimuth and elevation from a site on the Earth.
# For full details, see Algorithm 27 (RAZEL) on page 265 of Fundamentals of Astrodynamics and Applications (4th ed.) by David A Vallado.

from datetime import datetime
import numpy as np
from numpy import sin, cos
from utils.rotations import rot2, rot3


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

    r_ecef: np.ndarray
    v_ecef: np.ndarray
    r_ecef, v_ecef = fk5(r_ECI, v_ECI, datetime, dUT1, dAT, x_p, y_p)

    r_site_ecef: np.ndarray = site(phi_gd, lda, h_ellp)

    rho_ecef: np.ndarray = r_ecef - r_site_ecef
    
    rho_dot_ecef: np.ndarray = v_ecef

    rot2_90_minus_phi_gd: np.ndarray = rot2(90 - phi_gd)
    rot3_lambda: np.ndarray = rot3(lda)

    sin_phi_gd: float = sin(phi_gd)
    cos_phi_gd: float = cos(phi_gd)
    sin_lambda: float = sin(lda)
    cos_lambda: float = cos(lda)
    sez_over_ecef: np.ndarray = np.array([[sin_phi_gd * cos_lambda, sin_phi_gd * sin_lambda, -cos_phi_gd], 
                                          [-sin_lambda, cos_lambda, 0],
                                          [cos_phi_gd * cos_lambda, cos_phi_gd * sin_lambda, sin_phi_gd]])

    assert(rot2_90_minus_phi_gd * rot3_lambda == sez_over_ecef)

    rho_sez: np.ndarray = sez_over_ecef * rho_ecef
    rho_sez_dot: np.ndarray = sez_over_ecef * rho_dot_ecef

    rho: float = float(np.linalg.norm(rho_sez))

    sin_el: float = float(rho_sez / rho)  # Book says rho_z rather than rho_sez for first value but unclear what rho_z is.

    ...

    # FIXME fix placeholder values for outputs.
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
