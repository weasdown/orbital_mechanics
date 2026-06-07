from abc import ABC, abstractmethod
from datetime import datetime

import requests as r


class LatestBulletin(ABC):
    def __init__(self, letter: str):
        self._letter: str = letter
        self.date_retrieved = datetime.today().date()

    @property
    @abstractmethod
    def json(self) -> str:
        pass

    @property
    @abstractmethod
    def json_url(self):
        pass

    @property
    def text(self) -> str:
        resp: r.Response = r.get(self.url)
        return resp.text

    @property
    def url(self) -> str:
        return f'https://datacenter.iers.org/data/latestVersion/bulletin{self._letter}.txt'

    @property
    def vol_num_line(self) -> str:
        text_lines: list[str] = self.text.split('\n')
        vol_num_line: str = text_lines[7].rstrip()  # Get the line that includes the bulletin's "Vol." and "No.".
        vol_num_line = vol_num_line[vol_num_line.index('V'):]
        return vol_num_line


class LatestBulletinA(LatestBulletin):
    def __init__(self):
        super().__init__('A')

    @property
    def json(self) -> dict:
        return r.get(self.json_url).json()

    @property
    def json_url(self):
        return f'https://datacenter.iers.org/data/json/bulletin{self._letter.lower()}-{self.vol.lower()}-{self.num}.json'

    @property
    def num(self) -> str:
        vol_num_split = self.vol_num_line.split(' ')
        num = vol_num_split[3]
        return num

    @property
    def vol(self) -> str:
        vol_num_split = self.vol_num_line.split(' ')
        vol = vol_num_split[1]
        return vol


class LatestBulletinC(LatestBulletin):
    def __init__(self):
        super().__init__('C')

    @property
    def json(self) -> dict:
        return r.get(self.json_url).json()

    @property
    def json_url(self):
        raise NotImplementedError('LatestBulletinC.json_url property is not yet implemented.')


class LatestBulletinD(LatestBulletin):
    def __init__(self):
        super().__init__('D')

    @property
    def json(self) -> dict:
        """Bulletin Ds are not available in JSON form."""
        raise TypeError('LatestBulletinD does not support the json property.')

    @property
    def json_url(self):
        raise NotImplementedError('LatestBulletinD.json_url property is not yet implemented.')


class IERS:
    """Class for getting time correction values and Earth rotation poles from IERS."""

    @staticmethod
    def d_at():
        """Gets the latest ΔAT value from the latest Bulletin C."""
        bulletin_c: str = LatestBulletinC().text
        bulletin_lines: list[str] = bulletin_c.split('\n')

        value_lead: str = 'UTC-TAI = '
        value_line: str = [line for line in bulletin_lines if value_lead in line.lstrip()][0]
        print(f'{value_line = }')

        lead_index: int = value_line.find(value_lead)
        value: int = int(value_line[lead_index:-1].replace(value_lead, '').rstrip())
        return value

        # value: float = float(value_line.replace(value_lead, '').replace(' s', ''))
        # return value

    @staticmethod
    def d_ut1() -> float:
        """Gets the latest ΔUT1 value from the latest Bulletin D."""
        bulletin_d: str = LatestBulletinD().text
        bulletin_lines: list[str] = bulletin_d.split('\n')

        value_lead: str = 'DUT1 = '
        value_line: str = [line.lstrip() for line in bulletin_lines if line.lstrip().startswith(value_lead)][0]

        value: float = float(value_line.replace(value_lead, '').replace(' s', ''))
        return value

    @staticmethod
    def _rapid_service_date(date: datetime):
        """Returns a date in the format supplied in a Bulletin A IERS Rapid Service table."""
        ymd = date.strftime('%y %m %d')
        return ymd.replace(' 0', '  ')  # remove zero padding

    @staticmethod
    def poles() -> list[float]:
        """Gets the latest (predicted) x_p and y_p value from the latest Bulletin A."""
        bulletin_a: LatestBulletinA = LatestBulletinA()
        time_series: list[dict] = bulletin_a.json['EOP']['data']['timeSeries']

        # Find today's entry in the time series.
        def time_match(entry: dict) -> bool:
            today: datetime = datetime.today()
            today_year = today.strftime('%Y')
            today_month = today.strftime('%m')
            today_day = today.strftime('%d')

            time: dict = entry['time']

            return True if (time['dateYear'] == today_year) and (time['dateMonth'] == today_month) and (
                    time['dateDay'] == today_day) else False

        today_entry: dict = [entry for entry in time_series if time_match(entry)][0]
        pole_data: dict = today_entry['dataEOP']['pole']

        return [float(pole_data['X']), float(pole_data['Y'])]
