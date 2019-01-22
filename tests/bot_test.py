import unittest
from main import bot, session_builder, config


class BotRequestsTestCase(unittest.TestCase):
    def setUp(self):
        self.Bot = bot.PerfectGymBot(session=session_builder.Session.build(), config=config.CrossfitConfig)

    def test_client_login(self):
        self.assertIsNotNone(self.Bot.client_login())
