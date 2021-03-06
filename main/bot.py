# Module responsible for sending the requests to the page #

import logging
from typing import List, Any

from bs4 import BeautifulSoup
from requests import RequestException

from main import json_parser, configmanager
from main.data_containers import FitnessClasses


class Bot:
    """
    Represents basic Bot functionality, common for all fitness apps&pages bots.

    Parameters:
    ----------
    session : requests.sessions
        User parametrised requests.session class.
    config_name: str
        Name of configuration that is present in config.ini file and should be loaded.
    """

    _session = None
    _baseUrl = None
    _credentials = None
    _logger = logging.getLogger("Bot")

    def __init__(self, session, config_name):
        self._session = session
        # baseUrl assigned automatically based on configuration.
        config_manager = configmanager.ConfigManager()
        self._baseUrl = config_manager.read_base_url(config_name)
        self._credentials = configmanager.CredentialsManager().read_credentials(config_name)

    def book_classes(self, class_details):
        """
        Try to book classes given by user. Exception will be thrown if classes could not be booked.
        :param class_details: FitnessClasses
        :return: self
        """
        pass

    def _is_user_logged_in(self):
        raise NotImplementedError()

    def _is_class_bookable(self, class_id):
        raise NotImplementedError()

    def get_booked_classes(self):
        raise NotImplementedError()

    def _ensure_user_logged_in(self):
        """
        Checks if user is logged into the given fitness booking system. If not, tries to log user in.
        In case of login failure error message is shown.
        """
        if not self._is_user_logged_in():
            self.login()
            if not self._is_user_logged_in():
                raise RequestException("Could not login. Please check your credentials!")


class PerfectGymBot(Bot):
    """ Bot designed to work with PerfectGym system used by Fitness Platinium, CF Krakow and others"""

    def login(self):
        """
        Performs login to the application using credentials from credentials.py file not stored in VCS

        :rtype: PerfectGymBot
        """
        payload = {'Login': self._credentials[0], 'Password': self._credentials[1]}
        self._session.post(self._baseUrl + "Auth/Login", data=payload)
        return self

    def book_classes(self, class_details):
        """
        Books classes for user based on class details like start date/time, club and trainer.
        User login is verified inside the method already.
        """
        self._ensure_user_logged_in()

        class_id = self._get_class_id(class_details)

        if not class_id:
            self._logger.warning('Wrong class information. Please check your classes details.')
            return self

        if not self._is_class_bookable(class_id):
            self._logger.warning('Classes are not bookable! Classes are either full or its too early too book them')

        booking_payload = {'classId': class_id}
        response = self._session.post(self._baseUrl + 'Classes/ClassCalendar/BookClass', booking_payload)

        if response.status_code == 200:
            self._logger.info('Class were properly booked!')
        else:
            self._logger.warning('There was an error while booking. Classes were not booked')

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
            raise AssertionError("Could not retrieve list of classes")

        return json_parser.PerfectGymParser.parse_booked_classes_from_users_calendar(response.json())

    def _get_class_id(self, class_details):
        """
        Sends request to get classes available in whole week in PerfectGym system.
        Then parses information about classes available and returns ID of classess matching class details param
        """
        start_date = class_details.date + "T" + "00:00:00"
        club_payload = {"clubId": json_parser.get_club_id(class_details), "date": start_date}
        r = self._session.post(self._baseUrl + "Classes/ClassCalendar/WeeklyClasses", data=club_payload)
        classes_response_data = r.json()

        return json_parser.PerfectGymParser.get_class_id_from_classes_list(classes_response_data, class_details)

    def _is_user_logged_in(self):
        """
        :return: True when user is logged in and can access his profile. False otherwise.
        """
        response = self._session.get(self._baseUrl + 'Profile/Profile/GetFamilyMembersForEdit')
        return response.status_code == 200

    def _is_class_bookable(self, class_id):
        """
        Checks whether given class can be booked by User. Some classes are not bookable because they are full or it's
        too early to book them.

        :return: True when class can be booked. False otherwise.
        """
        if not class_id:
            return False

        url = self._baseUrl + 'Classes/ClassCalendar/Details?classId={}'.format(class_id)
        response = self._session.get(url)
        return (response.json())['Status'] == 'Bookable'


class EFitnessBot(Bot):
    """
    Bot designed to work with `EFitness system <http://http://efitness.pl/>`_ used by Grappling Krakow,
    Infinity Fitness Krakow etc
    """

    def login(self):
        """
        Performs login to the application using credentials from credentials.py file not stored in VCS
        :rtype: EFitnessBot
        """
        payload = {'Login': self._credentials[0], 'Password': self._credentials[1]}
        self._session.post(self._baseUrl + "Login/SystemLogin", data=payload)
        return self

    def book_classes(self, class_details):
        """
        Books classes in EFitness system for user based on class details like start date/time, club and trainer.
        """

        # self._ensure_user_logged_in()
        #
        class_id = self._get_class_id(class_details)
        print(class_id)

        if not class_id:
            self._logger.warning('Wrong class information. Please check your classes details.')
            return self

        if not self._is_class_bookable(class_id):
            self._logger.warning('Classes are not bookable! Classes are either full or its too early too book them')

        # booking_payload = {'id': class_id, 'memberID': '3956236'}
        # response = self._session.post(self._baseUrl + 'Schedule/RegisterForClass', booking_payload)
        #
        # print(response)
        # print(response.json())
        # if response.status_code == 200 and response.json()['Success']:
        #     self._logger.info('Class were properly booked!')
        # else:
        #     self._logger.warning('There was an error while booking. Classes were not booked')
        #
        # return self

    def _is_user_logged_in(self):
        """
        :return: True when user is logged in and can access his profile. False otherwise.
        """
        response = self._session.get(self._baseUrl + 'MemberInfo/Index')
        return 'class="daneprofilowe"' in response.text

    def _is_class_bookable(self, class_id):
        pass

    def get_booked_classes(self):
        response = self._session.get(self._baseUrl + 'kalendarz-zajec')
        # TODO: load Beautifulsoup only once per class instance
        soup = BeautifulSoup(response.text, 'html.parser')
        parsed_response = soup.find_all(class_='button calendar_cancel_reservation')
        booked_classes_list = []
        for x in parsed_response:
            # TODO rework to parse this data in private method, without magic numbers
            date = x['title'][39:49]
            start_time = x['title'][52:57]
            name = x['title'][60:len(x['title']) - 1]
            booked_classes_list.append(
                FitnessClasses(x['meta:id'], name, date, start_time, None, None, None));
        return booked_classes_list

    def _get_class_id(self, class_details):
        """
       Sends request to get classes available in whole week in EFitness system.
       Then parses information about classes available and returns ID of classes matching class details param
       """
        response = self._session.get(
            self._baseUrl + 'kalendarz-zajec?room=&view=WeekCascading&day={}'.format(class_details.date))
        soup = BeautifulSoup(response.text, 'html.parser')
        list_of_fitness_classes = soup.find_all(class_='event')

        # TODO: refactor those 2 loops
        # Go through all fitness classes and find ones with matching trainer and name
        matching_classes_ids: List[Any] = list()
        for event in list_of_fitness_classes:
            children = event.findChildren()
            if children[3].text == class_details.name \
                    and children[4].text == class_details.trainer:
                matching_classes_ids.append(event.get('meta:id'))

        # check multiple matching classes to find exact one by date.
        for event_id in matching_classes_ids:
            response = self._session.get(self._baseUrl + 'schedule/showoverlay?schiid={}'.format(event_id))
            soup = BeautifulSoup(response.text, 'html.parser')
            if soup.find("span", attrs={"class": "dark"}).text[-10:] == class_details.date:
                return event_id
