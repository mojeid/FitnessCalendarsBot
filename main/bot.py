# Module responsible for sending the requests to the page #

import requests
from main import json_parser, credentials


class Bot:
    """
    Represents basic Bot functionality, common for all fitness apps&pages bots.
    """
    _session = requests.session()
    _config = None

    def __init__(self, session, config):
        self._session = session
        self._config = config


class PerfectGymBot(Bot):
    """ Bot designed to work with PerfectGym system used by Platinium, CF Krakow and others"""

    def client_login(self):
        self._session.get('https://crossfit.perfectgym.pl/ClientPortal2/')
        payload = {'Login': credentials.username, 'Password': credentials.password}
        self._session.post("https://crossfit.perfectgym.pl/ClientPortal2/Auth/Login", data=payload)
        return self

    def book_class(self, class_details):
        """Books classes for user based on class details like start date/time, club and trainer.

        User login is verified inside the method already. """
        if not self._is_user_logged_in():
            self.client_login()

        class_id = self._get_class_id(class_details)

        if not class_id or not self._is_class_bookable(class_id):
            print('Wrong class information or class is not bookable. Please check your classes details.')
            return

        booking_payload = {'classId': class_id}
        response = self._session.post('https://crossfit.perfectgym.pl/ClientPortal2/Classes/ClassCalendar/BookClass',
                                      booking_payload)

        if response.status_code == 200:
            print('Class were properly booked!')
        else:
            print('There was an error while booking. Classes were not booked')

    def cancel_booking(self, class_details):
        """ Cancels user's reservation for classes for classes specfied by date/time and trainer.

        If user have no reservation, appropriate message will be shown to user. """
        if not self._is_user_logged_in():
            self.client_login()

        class_id = self._get_class_id(class_details)

        if not class_id:
            print('There are no such classes as specified. Please provide correct class details.')
            return

        cancel_payload = {'classId': class_id}
        self._session.post('https://crossfit.perfectgym.pl/ClientPortal2/Classes/ClassCalendar/CancelBooking',
                           cancel_payload)

    def _get_class_id(self, class_details):
        """Parses information about classes available and returns ID of classess matching class details param """
        club_payload = {"clubId": self._get_club_id(class_details)}
        r = self._session.post("https://crossfit.perfectgym.pl/ClientPortal2/Classes/ClassCalendar/WeeklyClasses",
                               data=club_payload)
        classes_response_data = r.json()

        return json_parser.get_class_id_from_perfectgym_classess_list(classes_response_data, class_details)

    def _is_user_logged_in(self):
        response = self._session.get(
            'https://crossfit.perfectgym.pl/ClientPortal2/Profile/Profile/GetFamilyMembersForEdit')
        return response.status_code == 200

    def _is_class_bookable(self, class_id):
        if not class_id:
            return False

        url = "https://crossfit.perfectgym.pl/ClientPortal2/Classes/ClassCalendar/Details?classId={}".format(class_id)
        response = self._session.get(url)
        return (response.json())['Status'] == 'Bookable'

    @staticmethod
    def _get_club_id(class_details):
        # In PerfectGym system 3 is hardcoded for CF Krakow and 4 for CF Lea
        if 'Lea' in class_details['clubName']:
            return 4
        if 'Kraków' in class_details['clubName'] or 'Krakow' in class_details['clubName']:
            return 3

        print('There is no club with such name. Please provide correct club name')
        return
