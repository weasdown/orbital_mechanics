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

    def x_p(self):
        """Gets the latest x_p value from the latest Bulletin A."""
        pass

    @staticmethod
    def y_p():
        """Gets the latest y_p value from the latest Bulletin A."""
        pass
