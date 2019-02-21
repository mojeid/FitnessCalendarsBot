import json
import unittest

from main import json_parser
from main.data_containers import FitnessClasses


class JsonParserTestCase(unittest.TestCase):

    def test_get_class_id_from_perfectgym_classes_list(self):
        file = open('resources/parser_clubs_test_data')
        json_test_data = json.loads(file.read())
        file.close()

        class_details = FitnessClasses(None, 'CrossFit Beginners', '2019-01-27', '10:00', 'Wiktor Stopyra',
                                       'Crossfit Lea', None)
        self.assertEqual(89352,
                         json_parser.PerfectGymParser.get_class_id_from_classes_list(json_test_data, class_details))

    def test_get_booked_classes_from_users_calendar(self):
        file = open('resources/parser_booked_classes_test_data')
        json_test_data = json.loads(file.read())
        file.close()
        parser = json_parser.PerfectGymParser

        self.assertEqual(2, len(parser.parse_booked_classes_from_users_calendar(json_response=json_test_data)))
        self.assertEqual("WOD Beginners",
                         parser.parse_booked_classes_from_users_calendar(json_response=json_test_data)[1][1])

    def test_supported_networks_list(self):
        SUPPORTED_NETWORKS_COUNT = 2
        self.assertEqual(SUPPORTED_NETWORKS_COUNT, len(json_parser.get_supported_fitness_networks()))

    def test_get_list_of_clubs(self):
        self.assertEqual(11, len(json_parser.get_list_of_clubs("Platinium")))
