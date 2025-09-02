import requests as r

class IERS:
    """Class for getting time correction values and Earth rotation poles from IERS."""

    @staticmethod
    def d_at():
        pass

    @staticmethod
    def d_ut1():
        pass

    @staticmethod
    def x_p():
        pass

    @staticmethod
    def y_p():
        pass

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
