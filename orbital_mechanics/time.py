from datetime import datetime

def julian_date(date_time: datetime) -> float:
    """Calculate the Julian Date for a given calendar date.

    Based on Algorithm 14 on page 183 (PDF page 210) of **Fundamentals of Astrodynamics and Applications** (4th ed.) by David A. Vallado."""
    year: int = date_time.year
    month: int = date_time.month
    day: int = date_time.day
    hour: int = date_time.hour - 1
    minute: int = date_time.minute
    second: int = date_time.second

    print([year, month, day, hour, minute, second])

    first_term = 367 * year
    second_term = int(7 * (year + int(month + 9 / 12)) / 4)
    third_term = int(275 * month / 9)
    fourth_term = day + 1721013.5
    fifth_term =  (((second / 60 + minute) / 60 + hour) / 24)

    # jd: float = (367 * year) - int(7 * (year + int(month + 9 / 12)) / 4) + int(275 * month / 9) + day + 1721013.5 + (((second / 60 + minute) / 60 + hour) / 24)
    jd = first_term - second_term + third_term + fourth_term + fifth_term

    # FIXME returned result is two weeks, two mins and 35 seconds too early

    return jd


def modified_julian_date(date_time: datetime) -> float:
    return julian_date(date_time) - 2400000.5


print(julian_date(datetime.now()))
print(modified_julian_date(datetime.now()))