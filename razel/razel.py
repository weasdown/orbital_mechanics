# Calculates spacecraft azimuth and elevation from a site on the Earth.
# For full details, see Algorithm 27 (RAZEL) on page 265 of Fundamentals of Astrodynamics and Applications (4th ed.) by David A Vallado.

from datetime import datetime
import numpy as np
from numpy import sin, cos, asin, deg2rad, sqrt, dot
from utils.rotations import rot2, rot3


# TODO add missing argument type hints once types known.
def razel(r_eci: np.ndarray, v_eci: np.ndarray, date_time: datetime, d_ut1: float, d_at: float, x_p, y_p, phi_gd: float, lda: float, h_ellp: float) -> list[float]:
    """
    Calculates a spacecraft's range, azimuth, elevation, and the rates of these, from a point on the ground.
    
    Inputs:
    r_ECI, v_ECI, yr, mo, day, UTC, ΔUT1, ΔAT, x_p, y_p, φ_gd, λ, h_ellp

    d_ut1 (ΔUT1): an observed time correction value to align UT1 with UTC. This should be less than 0.9 seconds, e.g. 0.463326 seconds.
    d_at (ΔAT): an atomic time correction value obtained from the [Astronomical Almanac](https://aa.usno.navy.mil/publications/asa), e.g. 32 seconds.
    As of September 2nd, 2025, this stands at 37 seconds, according to the [International Earth Rotation and Reference
    Systems Service (IERS)](https://www.iers.org/IERS/EN/Home/home_node.html), which is the authority on this.
    Their [Bulletin C of July 7th, 2025](https://datacenter.iers.org/data/latestVersion/bulletinC.txt), also confirms
    that no leap second will be added at the end of December 2025, so ΔAT will remain at 37 seconds until further notice.

    φ_gd: latitude, with North being positive.
    λ: longitude in degrees, with West being negative.
    h_ellp: height above mean sea level in metres.

    Outputs: 
    ρ, β, el, ρ_dot, β_dot, el_dot

    Based on Algorithm 27 on page 265 of Fundamentals of Astrodynamics and Applications (4th ed.) by David A Vallado.
    """

    r_ecef: np.ndarray
    v_ecef: np.ndarray
    r_ecef, v_ecef = fk5(r_eci, v_eci, date_time, d_ut1, d_at, x_p, y_p)

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
    rho_dot_sez: np.ndarray = sez_over_ecef * rho_dot_ecef

    rho: float = float(np.linalg.norm(rho_sez))

    rho_s: float = float(rho_sez[0])  # S component of rho SEZ vector
    rho_e: float = float(rho_sez[1])  # E component of rho SEZ vector
    rho_z: float = float(rho_sez[2])  # Z component of rho SEZ vector

    rho_dot_s: float = float(rho_dot_sez[0])  # S component of rho dot SEZ vector
    rho_dot_e: float = float(rho_dot_sez[1])  # E component of rho dot SEZ vector
    rho_dot_z: float = float(rho_dot_sez[2])  # Z component of rho dot SEZ vector


    # Book says rho_z rather than rho_sez for first value but unclear what rho_z is.
    sin_el: float = float(rho_sez / rho)
    el: float = float(asin(rho_z / rho))  # radians

    rs_sq_re_sq: float = rho_s ** 2 + rho_e ** 2
    sqrt_rs_sq_re_sq: float = sqrt(rho_s ** 2 + rho_e ** 2)
    sqrt_rs_dot_sq_re_dot_sq: float = sqrt(rho_dot_s ** 2 + rho_dot_e ** 2)

    if el != deg2rad(90):  # el is not 90 degrees
        sin_beta = rho_e / sqrt_rs_sq_re_sq
        # cos_beta = -rho_s / sqrt_rs_sq_re_sq

    else:  # el is 90 degrees
        sin_beta = rho_dot_e / sqrt_rs_dot_sq_re_dot_sq
        # cos_beta = -rho_dot_s / sqrt_rs_dot_sq_re_dot_sq

    beta: float = asin(sin_beta)

    rho_dot: float = dot(rho_sez, rho_dot_sez) / rho
    beta_dot: float = (rho_dot_s * rho_e - rho_dot_e * rho_s) / rs_sq_re_sq
    el_dot: float = (rho_dot_z - rho_dot * sin_el) / sqrt_rs_sq_re_sq

    return [rho, beta, el, rho_dot, beta_dot, el_dot]


# TODO add missing argument type hints once types known.
def fk5(r_eci: np.ndarray, v_eci: np.ndarray, date_time: datetime, d_ut1: float, d_at: float, x_p, y_p) -> list[np.ndarray]:
    """
    Converts position and velocity vectors in the ECI frame to the ECEF frame.

    d_ut1 (ΔUT1): an observed time correction value to align UT1 with UTC. This should be less than 0.9 seconds, e.g. 0.463326 seconds.
    d_at (ΔAT): an atomic time correction value obtained from the [Astronomical Almanac](https://aa.usno.navy.mil/publications/asa), e.g. 32 seconds.
    """
    raise NotImplementedError

    # # FIXME fix placeholder values for outputs.
    # r_ecef: np.ndarray = np.ndarray([])
    # v_ecef: np.ndarray = np.ndarray([])

    # return [r_ecef, v_ecef]


# TODO add missing argument type hints once types known.
def site(phi_gd: float, lda: float, h_ellp: float) -> np.ndarray:
    """
    Calculates the ECEF position vector for a site on the Earth's surface.

    phi_gd: latitude, with North being positive.
    lda (λ): longitude in degrees, with West being negative.
    h_ellp: height above mean sea level in metres.
    """
    
    raise NotImplementedError

    # # FIXME fix placeholder value for output.
    # r_site_ecef: np.ndarray = np.ndarray([])
    # return r_site_ecef


if __name__ == '__main__':
    pass
