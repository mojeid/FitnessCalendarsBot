# Module responsible for sending the requests to the page #

import requests
import credentials


class PerfectGymBot:
    _session = requests.session()

    def client_login(self):
        self._session.get('https://crossfit.perfectgym.pl/ClientPortal2/')
        payload = {'Login': credentials.username, 'Password': credentials.password}
        self._session.post("https://crossfit.perfectgym.pl/ClientPortal2/Auth/Login", data=payload)
        return self

    def _isLoggedIn(self):
        response = self._session.get(
            'https://crossfit.perfectgym.pl/ClientPortal2/Profile/Profile/GetFamilyMembersForEdit')
        return response.status_code == 200
