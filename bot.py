# Module responsible for sending the requests to the page #

import requests
import credentials
import json_parser


class PerfectGymBot:
    _session = requests.session()

    def client_login(self):
        self._session.get('https://crossfit.perfectgym.pl/ClientPortal2/')
        payload = {'Login': credentials.username, 'Password': credentials.password}
        self._session.post("https://crossfit.perfectgym.pl/ClientPortal2/Auth/Login", data=payload)
        return self

    def _get_classess_id(self, class_details):
        """Parses information about classes available and returns ID of classess matching class details param """
        s = self._session
        club_payload = {"clubId": "4"}
        r = s.post("https://crossfit.perfectgym.pl/ClientPortal2/Classes/ClassCalendar/WeeklyClasses",
                   data=club_payload)
        classes_response_data = r.json()

        return json_parser.JsonParserForPerfectGymData().get_class_id(classes_response_data, class_details)

    def _isLoggedIn(self):
        response = self._session.get(
            'https://crossfit.perfectgym.pl/ClientPortal2/Profile/Profile/GetFamilyMembersForEdit')
        return response.status_code == 200
