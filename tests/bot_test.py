import configparser
import unittest
from main import bot, session_builder


class BotRequestsTestCase(unittest.TestCase):
    def setUp(self):
        config = configparser.ConfigParser()
        config.read('../main/resources/configuration.ini')
        self.bot = bot.PerfectGymBot(session=session_builder.Session.build(), config=config['Crossfit'])

    def test_client_login(self):
        self.assertIsNotNone(self.bot.client_login(), "Client Login is not working correctly!")

    def test_get_booked_classes(self):
        self.assertTrue(isinstance(self.bot.get_booked_classes(), list))
