from datetime import datetime, timedelta
from math import sin

from utils.iers import IERS


# FIXME fix slightly incorrect tdb, t_ut1, t_tt, t_tdb outputs
def conv_time(date_time: datetime, d_ut1: float, d_at: int) -> list:
    """
    Based on Algorithm 16 on page 195 of *Fundamentals of Astrodynamics and Applications* (4th ed.) by David A Vallado.

    :param date_time: the date and time of interest, in UTC.
    :type date_time: datetime
    :param d_ut1: the value of ΔUT1 provided by `IERS`_ for the given date.
    :type d_ut1: float
    :param d_at: the value of ΔAT provided by `IERS`_ for the given date.
    :type d_at: int
    :return: list containing the following: ``[UT1, TAI, TT, TDB, T<sub>UT1</sub>, T<sub>TT</sub>, T<sub>TDB</sub>]``.
    :rtype: list

    .. _IERS: https://www.iers.org/IERS/EN/Home
    """

    utc: datetime = date_time
    ut1: datetime = utc + timedelta(days=0, seconds=d_ut1)

    # Check that utc and ut1 are within 0.9 seconds (i.e. that d_ut1 - ΔUT1 - is less than 0.9 seconds),
    # as recommended by Fundamentals pg 195 (PDF pg 222).
    if d_ut1 > 0.9:
        raise AttributeError(f'd_ut1 should be less than 0.9 seconds but was {d_ut1} seconds')

    tai: datetime = date_time + timedelta(days=0, seconds=d_at)

    gps_offset: int = get_gps_utc_offset()
    gps: datetime = date_time + timedelta(days=0, seconds=d_at - gps_offset)

    tt: datetime = tai + timedelta(days=0, seconds=32.184)

    jd_tt: float = julian_date(datetime(date_time.year, date_time.month, date_time.day, tt.hour, tt.minute, tt.second))

    t_tt: float = (jd_tt - 2451545.0) / 36525

    # jd_tai: float = julian_date(
    #     datetime(date_time.year, date_time.month, date_time.day, tai.hour, tai.minute, tai.second))

    # Hardcoded values copied from Algorithm 16 in Vallado.
    tdb: datetime = tt + timedelta(days=0, seconds=0.001657 * sin(628.3076 * t_tt + 6.2401)
                                                   + 0.000022 * sin(575.3385 * t_tt + 4.2970)
                                                   + 0.000014 * sin(1256.6152 * t_tt + 6.1969)
                                                   + 0.000005 * sin(606.9777 * t_tt + 4.0212)
                                                   + 0.000005 * sin(52.9691 * t_tt + 0.4444)
                                                   + 0.000002 * sin(21.3299 * t_tt + 5.5431)
                                                   + 0.000010 * t_tt * sin(628.3076 * t_tt + 4.2490))

    jd_tdb: float = julian_date(
        datetime(date_time.year, date_time.month, date_time.day, tdb.hour, tdb.minute, tdb.second))

    jd_ut1: float = julian_date(
        datetime(date_time.year, date_time.month, date_time.day, ut1.hour, ut1.minute, ut1.second))

    # tdb: float = (jd_tt - 2451545.0) / 36525
    t_ut1: float = (jd_ut1 - 2451545.0) / 36525

    t_tdb: float = (jd_tdb - 2451545.0) / 36525

    return [ut1, tai, tt, tdb, t_ut1, t_tt, t_tdb]


def get_gps_utc_offset() -> int:
    """
    Gets the integer number of seconds between GPS time and UTC.

    Retrievable from https://www.cnmoc.usff.navy.mil/Our-Commands/United-States-Naval-Observatory/Precise-Time-Department/Global-Positioning-System/GPS-Timing-Data-and-Information/.

    :return: The number of seconds between GPS time and UTC.
    :rtype: int
    """
    # GPS time is always ahead of TAI by exactly 19 seconds (source: https://gssc.esa.int/navipedia/index.php/Transformations_between_Time_Systems).
    tai_gps_offset: int = 19

    # The offset between TAI and UTC, written as ΔΑΤ, is a number of leap seconds. This is published by IERS as
    # UTC - TAI in their Bulletin C (latest Bulletin C: https://datacenter.iers.org/data/latestVersion/bulletinC.txt).
    # ΔAT is negative to show that TAI is ahead of UTC. Therefore, TAI = UTC - ΔAT, or UTC + |ΔAT|.
    iers = IERS()
    delta_at: int = iers.d_at

    # The offset between GPS time and UTC is therefore |ΔAT + (GPS to TAI offset)|.
    # Or GPS = UTC + ΔAT - 19s (from Example 3-7 in Fundamentals)
    # As of 20/9/2026, the offset is 18 seconds.
    # This is also published by the US Navy at https://www.cnmoc.usff.navy.mil/Our-Commands/United-States-Naval-Observatory/Precise-Time-Department/Global-Positioning-System/GPS-Timing-Data-and-Information/.
    offset: int = abs(delta_at + tai_gps_offset)

    return offset


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
