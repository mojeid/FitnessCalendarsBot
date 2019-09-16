import unittest

from main import bot, session_builder


class GeneralBotTestCase(unittest.TestCase):
    pass


class PerfectGymBotTestCase(unittest.TestCase):
    def setUp(self):
        self.bot = bot.PerfectGymBot(session=session_builder.Session.build(), config_name='Centrumfitness')

    def test_client_login(self):
        self.bot.login()
        self.assertTrue(self.bot._is_user_logged_in(), "Client Login is not working correctly!")

    def test_get_booked_classes(self):
        self.assertTrue(isinstance(self.bot.get_booked_classes(), list))


class EFitnessBotTestCase(unittest.TestCase):
    def setUp(self):
        self.bot = bot.EFitnessBot(session=session_builder.Session.build(), config_name='Infinity')

    def test_client_login(self):
        self.bot.login()
        self.assertTrue(self.bot._is_user_logged_in(), "Client Login is not working correctly!")

    # def test_get_booked_classes(self):
    #     self.assertTrue(isinstance(self.bot.get_booked_classes(), list))
