import configparser
import logging

from main import session_builder, bot
from main.data_containers import FitnessClasses

if __name__ == "__main__":
    # execute only if run as a script
    config = configparser.ConfigParser()
    config.read('resources/configuration.ini')
    logging.basicConfig(level=config['DEFAULT']['logging_level'])

    class_details = FitnessClasses(None, 'TRX', '27-02-2019', '20:00', 'Łukasz Balicki', 'Silownia',
                                   None)

    # perfectGymBot = bot.PerfectGymBot(session=session_builder.Session.build(), config=config['Platinium'])
    # perfectGymBot.book_class(class_details)

    efitness_bot = bot.EFitnessBot(session_builder.Session.build(), config=config['Infinity'])
    efitness_bot.login().book_class(class_details)
