from datetime import datetime

import requests as r


class IERS:
    """Class for getting time correction values and Earth rotation poles from IERS."""

    @staticmethod
    def bulletin_a() -> str:
        """Gets the latest Bulletin A."""
        url: str = 'https://datacenter.iers.org/data/latestVersion/bulletinA.txt'
        resp: r.Response = r.get(url)
        return resp.text

    @staticmethod
    def bulletin_c() -> str:
        """Gets the latest Bulletin C."""
        url: str = 'https://datacenter.iers.org/data/latestVersion/bulletinC.txt'
        resp: r.Response = r.get(url)
        return resp.text

    @staticmethod
    def bulletin_d():
        """Gets the latest Bulletin D."""
        url: str = 'https://datacenter.iers.org/data/latestVersion/bulletinD.txt'
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
