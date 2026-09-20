import json
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path

import requests as r

mocks_path: Path = Path('orbital_mechanics/mocks')


class LatestBulletin(ABC):
    def __init__(self, letter: str, use_mocks: bool = True):
        self._letter: str = letter
        self.date_retrieved = datetime.today().date()
        self._use_mocks: bool = use_mocks

    @property
    def json(self) -> dict:
        if self._use_mocks:
            try:
                with open(self.mock) as f:
                    return json.loads(f.read())
            except FileNotFoundError:
                pass

        # If fail to use mock or don't want to, get the JSON from the IERS website.
        return r.get(self.json_url).json()

    @property
    @abstractmethod
    def json_url(self):
        pass

    @property
    def mock(self) -> Path:
        ext: str = 'json' if isinstance(self, LatestBulletinA) else 'txt'
        return Path(f'{mocks_path}/bulletin_{self._letter.lower()}.{ext}')

    @property
    def text(self) -> str:
        if self._use_mocks:
            try:
                with open(self.mock) as f:
                    return f.read()
            except FileNotFoundError:
                pass

        # If fail to use mock or don't want to, get the text from the IERS website.
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

    def __init__(self, use_mocks: bool = True):
        self._use_mocks: bool = use_mocks

    @property
    def d_at(self) -> int:
        """Gets the latest ΔAT value from the latest Bulletin C."""
        bulletin_c: LatestBulletinC = LatestBulletinC()
        bulletin_lines: list[str] = bulletin_c.text.split('\n')

        value_lead: str = 'UTC-TAI = '

        try:
            # Iterate over each line in the list of text lines and extract the one that contains "UTC-TAI = ".
            # We iterate through the lines in reverse order as the "UTC-TAI = " line is near the bottom of the Bulletin.
            value_line: str = [line for line in reversed(bulletin_lines) if value_lead in line.lstrip()][0]
        except IndexError as ie:
            in_mock: str = f' in mock "{bulletin_c.mock}"' if self._use_mocks else ''
            raise RuntimeError(
                f'Could not get ΔAT value from latest Bulletin C - could not find "UTC-TAI = " line{in_mock}.') from ie

        lead_index: int = value_line.find(value_lead)
        value: int = int(value_line[lead_index:-1].replace(value_lead, '').rstrip())
        return value

    @property
    def d_ut1(self) -> float:
        """Gets the latest ΔUT1 value from the latest Bulletin D."""
        bulletin_d: LatestBulletinD = LatestBulletinD()
        bulletin_lines: list[str] = bulletin_d.text.split('\n')

        value_lead: str = 'DUT1 = '
        try:
            # Iterate over each line in the list of text lines and extract the one that starts with "DUT1 = ".
            # We iterate through the lines in reverse order as the "DUT1 = " line is near the bottom of the Bulletin.
            value_line: str = \
                [line.lstrip() for line in reversed(bulletin_lines) if line.lstrip().startswith(value_lead)][0]
        except IndexError as ie:
            in_mock: str = f' in mock "{bulletin_d.mock}"' if self._use_mocks else ''
            raise RuntimeError(
                f'Could not get ΔUT1 value from latest Bulletin D - could not find "DUT1 = " line{in_mock}.') from ie

        value: float = float(value_line.replace(value_lead, '').replace(' s', ''))
        return value

    @staticmethod
    def _rapid_service_date(date: datetime):
        """Returns a date in the format supplied in a Bulletin A IERS Rapid Service table."""
        ymd = date.strftime('%y %m %d')
        return ymd.replace(' 0', '  ')  # remove zero padding

    @property
    def poles(self) -> list[float]:
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

        today_entry: dict = {}
        for t in time_series:
            if time_match(t):
                today_entry: dict = t
                break

        pole_data: dict = today_entry['dataEOP']['pole']

        return [float(pole_data['X']), float(pole_data['Y'])]

    @property
    def x_p(self) -> float:
        """Latest (predicted) x_p value from the latest Bulletin A."""
        return self.poles[0]

    @property
    def y_p(self) -> float:
        """Latest (predicted) y_p value from the latest Bulletin A."""
        return self.poles[0]
