# Module responsible for sending the requests to the page #

import logging
from main import json_parser
from main.resources import credentials


class Bot:
    """
    Represents basic Bot functionality, common for all fitness apps&pages bots.
    """
    _session = None
    _config = None
    _baseUrl = None
    _logger = logging.getLogger("Bot")

    def __init__(self, session, config):
        self._session = session
        self._config = config
        self._baseUrl = config['BaseURL']


class PerfectGymBot(Bot):
    """ Bot designed to work with PerfectGym system used by Platinium, CF Krakow and others"""

    def client_login(self):
        """
        Performs login to the application using credentials from credentials.py file not stored in VCS

        :rtype: PerfectGymBot
        """
        payload = {'Login': credentials.username, 'Password': credentials.password}
        self._session.post(self._baseUrl + "Auth/Login", data=payload)
        return self

    def book_class(self, class_details):
        """
        Books classes for user based on class details like start date/time, club and trainer.
        User login is verified inside the method already.
        """
        self._ensure_user_logged_in()

        class_id = self._get_class_id(class_details)
        if not class_id or not self._is_class_bookable(class_id):
            self._logger.warning('Wrong class information or class is not bookable. Please check your classes details.')
            return self

        booking_payload = {'classId': class_id}
        response = self._session.post(self._baseUrl + 'Classes/ClassCalendar/BookClass', booking_payload)

        if response.status_code == 200:
            self._logger.info('Class were properly booked!')
        else:
            self._logger.info('There was an error while booking. Classes were not booked')

        return self

    def cancel_booking(self, class_details):
        """
        Cancels user's reservation for classes for classes specified by date/time and trainer.
        If user have no reservation, appropriate message will be shown to user.
        """
        self._ensure_user_logged_in()

        class_id = self._get_class_id(class_details)
        if not class_id:
            self._logger.warning('There are no such classes as specified. Please provide correct class details.')
            return self

        cancel_payload = {'classId': class_id}
        response = self._session.post(self._baseUrl + 'Classes/ClassCalendar/CancelBooking', cancel_payload)

        if response.status_code == 200:
            self._logger.info('Classes were successfully cancelled!')
        else:
            self._logger.warning('Could not cancel your booking!')
        return self

    def get_booked_classes(self):
        """
        :return: List of classes booked by user.
        """
        self._ensure_user_logged_in()

        response = self._session.get(self._baseUrl + 'MyCalendar/MyCalendar/GetCalendar')
        if not response.status_code == 200:
            self._logger.warning("Could not access user's list of classes.")

        return json_parser.get_booked_classes_from_users_calendar(response.json())

    def _get_class_id(self, class_details):
        """
        Sends request to get classes available in whole week in PerfectGym system.
        Then parses information about classes available and returns ID of classess matching class details param
        """
        start_date = class_details['date'] + "T" + "00:00:00"
        club_payload = {"clubId": json_parser.get_club_id(class_details), "date": start_date}
        r = self._session.post(self._baseUrl + "Classes/ClassCalendar/WeeklyClasses", data=club_payload)
        classes_response_data = r.json()

        return json_parser.get_class_id_from_perfectgym_classes_list(classes_response_data, class_details)

    def _ensure_user_logged_in(self):
        """
        Checks if user is logged into the PerfectGym system. If not, tries to log user in. In case of login failure
        error message is shown.
        """
        if not self._is_user_logged_in():
            self.client_login()
            if not self._is_user_logged_in():
                self._logger.warning(
                    'Login was not successful 2 times in a row. Please check your account credentials.')

    def _is_user_logged_in(self):
        response = self._session.get(self._baseUrl + 'Profile/Profile/GetFamilyMembersForEdit')
        return response.status_code == 200

    def _is_class_bookable(self, class_id):
        if not class_id:
            return False

        url = self._baseUrl + 'Classes/ClassCalendar/Details?classId={}'.format(class_id)
        response = self._session.get(url)
        return (response.json())['Status'] == 'Bookable'
