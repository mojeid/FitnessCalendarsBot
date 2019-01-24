""" Module responsible data from custom PerfectGym app HTTP responses. """
import json
import logging

import os

_logger = logging.getLogger("json_parser")


def get_class_id_from_perfectgym_classess_list(json_response, class_details):
    """ Parses JSON data and returns Class ID for specific class date/time and trainer."""
    class_id = None
    classes_per_hour = ((json_response['CalendarData'])[0])['ClassesPerHour']

    for entry in classes_per_hour:
        # Classes calendar in Response is organised first by hour then by day.
        if class_details['startTime'] not in entry['Hour']:
            continue
        for crossfit_classes in entry['ClassesPerDay']:
            # skip empty results lists
            if not crossfit_classes:
                continue
            # skip classes that does not match date or trainer requested
            if class_details['date'] not in crossfit_classes[0]['StartTime'] or class_details[
                'trainer'] != crossfit_classes[0]['Trainer']:
                continue

            class_id = crossfit_classes[0]['Id']

    return class_id


def get_supported_fitness_networks():
    """
    :return: List of supported fitness networks
    """
    json_data = _read_fitness_clubs_json()

    fitness_networks_list = []
    for network in json_data:
        fitness_networks_list.append(network.title())
    return fitness_networks_list


def get_list_of_clubs(fitness_network_name):
    """
    Shows list of currently supported fitness clubs within given Fitness network like Platinium.

    :param fitness_network_name: E.g. Platinium, Crossfit etc
    :return: List of clubs available in that network
    """
    json_data = _read_fitness_clubs_json()
    fitness_clubs = []

    try:
        for club in json_data[fitness_network_name.lower()]:
            fitness_clubs.append(club['name'])
    except KeyError:
        _logger.warning('There is no club with such name. Please provide correct club name')
        return

    return fitness_clubs


def _read_fitness_clubs_json():
    if 'tests' in os.getcwd():
        filepath = '../main/resources/fitness_clubs.json'
    else:
        filepath = 'main/resources/fitness_clubs.json'

    file = open(filepath)
    json_data = json.loads(file.read())
    file.close()

    return json_data
