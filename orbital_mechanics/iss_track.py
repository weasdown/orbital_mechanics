from datetime import datetime

import numpy as np

from orbital_mechanics.utils import IERS
from orbital_mechanics.razel.razel import razel


def iss_track(latitude: float, longitude: float, height: float, date_time: datetime) -> list[float]:
    """Tracks the International Space Station."""
    # FIXME: remove hardcoding of r_eci, v_eci
    r_eci: np.ndarray = np.array([1,2,3])
    v_eci: np.ndarray = np.array([1,2,3])

    iers: IERS = IERS()
    d_at: int = iers.d_at()
    d_ut1: float = iers.d_ut1()
    poles: list[float] = iers.poles()

    razel_data: list[float] = razel(r_eci=r_eci, v_eci=v_eci, date_time=date_time, d_ut1=d_ut1, d_at=d_at,
                                    x_p=poles[0], y_p=poles[1], phi_gd=latitude, lda=longitude,h_ellp=height)

    return razel_data
