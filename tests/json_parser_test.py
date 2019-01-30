import unittest
import json

from main import json_parser


class JsonParserTestCase(unittest.TestCase):

    def test_get_class_id_from_perfectgym_classes_list(self):
        file = open('resources/parser_clubs_test_data')
        json_test_data = json.loads(file.read())
        file.close()

        classDetails = {
            "clubName": "Crossfit Lea",
            "startTime": "10:00",
            "date": "2019-01-27",
            "trainer": "Wiktor Stopyra",
            "title": 'CrossFit Beginners'
        }

        self.assertEqual(89352, json_parser.get_class_id_from_perfectgym_classes_list(json_test_data, classDetails))

    def test_get_booked_classes_from_users_calendar(self):
        file = open('resources/parser_booked_classes_test_data')
        json_test_data = json.loads(file.read())
        file.close()

        self.assertEqual(2, len(json_parser.get_booked_classes_from_users_calendar(json_response=json_test_data)))
        self.assertEqual("WOD Beginners",
                         json_parser.get_booked_classes_from_users_calendar(json_response=json_test_data)[1][1])

    def test_supported_networks_list(self):
        SUPPORTED_NETWORKS_COUNT = 2
        self.assertEqual(SUPPORTED_NETWORKS_COUNT, len(json_parser.get_supported_fitness_networks()))

    def test_get_list_of_clubs(self):
        self.assertEqual(11, len(json_parser.get_list_of_clubs("Platinium")))
