from datetime import datetime, timedelta


# TODO implement conv_time() function
def conv_time(date_time: datetime, d_ut1: float, d_at: int) -> list:
    """
    Based on Algorithm 16 on page 195 of *Fundamentals of Astrodynamics and Applications* (4th ed.) by David A Vallado.

    :param date_time: the date and time of interest.
    :type date_time: datetime
    :param d_ut1: the value of ΔUT1 provided by `IERS`_ for the given date.
    :type d_ut1: float
    :param d_at: the value of ΔAT provided by `IERS`_ for the given date.
    :type d_at: int
    :return: list containing the following: ``[UT1, TAI, TT, TDB, T<sub>UTI</sub>, T<sub>TT</sub>, T<sub>TDB</sub>]``.
    :rtype: list

    .. _IERS: https://www.iers.org/IERS/EN/Home
    """
    ut1 = date_time + timedelta(days=0, seconds=d_ut1)
    tai = ...
    tt = ...
    tdb = ...
    t_uti = ...
    t_tt = ...
    t_tdb = ...

    raise NotImplementedError('conv_time() function is not yet implemented.')
    # return [ut1, tai, tt, tdb, t_uti, t_tt, t_tdb]


def julian_date(date_time: datetime) -> float:
    """Calculate the Julian Date for a given calendar date.

    :param date_time: The date and time to be converted.
    :type date_time: datetime

    Based on Algorithm 14 on page 183 (PDF page 210) of **Fundamentals of Astrodynamics and Applications** (4th ed.) by David A. Vallado."""
    year: int = date_time.year
    month: int = date_time.month
    day: int = date_time.day
    hour: int = date_time.hour
    minute: int = date_time.minute
    second: int = date_time.second

    # TODO implement has_leap_second() function - currently assumes the day does not have a leap second
    def has_leap_second(day_num) -> bool:
        # raise NotImplementedError('has_leap_second() function is not yet implemented.')
        return False

    first_term = 367 * year
    second_term = -int(7 * (year + int((month + 9) / 12)) / 4)
    third_term = int(275 * month / 9)
    fourth_term = day
    fifth_term = 1721013.5
    seconds_per_day = 86400 if not has_leap_second(day) else 86401
    sixth_term = (hour * 3600 + minute * 60 + second) / seconds_per_day

    jd: float = first_term + second_term + third_term + fourth_term + fifth_term + sixth_term
    return jd


def modified_julian_date(date_time: datetime) -> float:
    return julian_date(date_time) - 2400000.5
