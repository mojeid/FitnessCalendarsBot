import unittest
import json
from main import json_parser


class JsonParserTestCase(unittest.TestCase):

    def test_get_class_id_from_perfectgym_classess_list(self):
        file = open('parser_test_data')
        json_test_data = json.loads(file.read())
        file.close()

        classDetails = {
            "clubName": "Crossfit Lea",
            "startTime": "10:00",
            "date": "2019-01-27",
            "trainer": "Wiktor Stopyra",
            "title": 'CrossFit Beginners'
        }

        print(json_test_data)
        self.assertEqual(89352, json_parser.get_class_id_from_perfectgym_classess_list(json_test_data, classDetails))
