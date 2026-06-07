from datetime import datetime

import requests as r


class LatestBulletin:
    def __init__(self, letter: str):
        self._letter: str = letter
        self.date_retrieved = datetime.today().date()

    @property
    def json_url(self):
        return f'https://datacenter.iers.org/data/json/bulletin{self._letter.lower()}-{self.vol.lower()}-{self.num}.json'

    @property
    def json(self) -> str:
        raise NotImplementedError('Bulletin.json property is not yet implemented.')

    @property
    def num(self) -> str:
        vol_num_split = self.vol_num_line.split(' ')
        num = vol_num_split[3]
        return num

    @property
    def text(self) -> str:
        resp: r.Response = r.get(self.url)
        return resp.text

    @property
    def url(self) -> str:
        return IERS.latest_bulletin_url(self._letter)

    @property
    def vol_num_line(self) -> str:
        text_lines: list[str] = self.text.split('\n')
        vol_num_line: str = text_lines[7].rstrip()  # Get the line that includes the bulletin's "Vol." and "No.".
        vol_num_line = vol_num_line[vol_num_line.index('V'):]
        return vol_num_line

    @property
    def vol(self) -> str:
        vol_num_split = self.vol_num_line.split(' ')
        vol = vol_num_split[1]
        return vol


class IERS:
    """Class for getting time correction values and Earth rotation poles from IERS."""

    @staticmethod
    def _latest_bulletin_url(bulletin_letter: str) -> str:
        return f'https://datacenter.iers.org/data/latestVersion/bulletin{bulletin_letter}.txt'

    @staticmethod
    def bulletin_a() -> str:
        """Gets the latest Bulletin A."""
        url: str = IERS._latest_bulletin_url('A')
        resp: r.Response = r.get(url)
        return resp.text

    @staticmethod
    def bulletin_c() -> str:
        """Gets the latest Bulletin C."""
        url: str = IERS._latest_bulletin_url('C')
        resp: r.Response = r.get(url)
        return resp.text

    @staticmethod
    def bulletin_d():
        """Gets the latest Bulletin D."""
        url: str = IERS._latest_bulletin_url('D')
        resp: r.Response = r.get(url)
        return resp.text

    def d_at(self):
        """Gets the latest ΔAT value from the latest Bulletin C."""
        bulletin_c: str = self.bulletin_c()
        bulletin_lines: list[str] = bulletin_c.split('\n')

        value_lead: str = 'UTC-TAI = '
        value_line: str = [line for line in bulletin_lines if value_lead in line.lstrip()][0]
        print(f'{value_line = }')

        lead_index: int = value_line.find(value_lead)
        value: int = int(value_line[lead_index:-1].replace(value_lead, '').rstrip())
        return value

        # value: float = float(value_line.replace(value_lead, '').replace(' s', ''))
        # return value

    def d_ut1(self) -> float:
        """Gets the latest ΔUT1 value from the latest Bulletin D."""
        bulletin_d: str = self.bulletin_d()
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

    def poles(self) -> list[float]:
        """Gets the latest (predicted) x_p and y_p value from the latest Bulletin A."""
        bulletin_a: str = self.bulletin_a()
        bulletin_lines: list[str] = bulletin_a.split('\n')

        # FIXME: build URL for JSON from Vol. and No. in latest Bulletin A.
        example_json_url: str = 'https://datacenter.iers.org/data/json/bulletina-xxxviii-035.json'

        a_json: dict = r.get(example_json_url).json()
        time_series: list[dict] = a_json['EOP']['data']['timeSeries']

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
