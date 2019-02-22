import configparser
import logging

from main import session_builder, bot
from main.data_containers import FitnessClasses

if __name__ == "__main__":
    # execute only if run as a script
    config = configparser.ConfigParser()
    config.read('resources/configuration.ini')
    logging.basicConfig(level=config['DEFAULT']['logging_level'])

    class_details = FitnessClasses(None, ' K1 P1 Struga', '20-02-2019', '18:00', 'Paweł Kotaba', 'Nad Struga',
                                   None)

    # perfectGymBot = bot.PerfectGymBot(session=session_builder.Session.build(), config=config['Platinium'])
    # perfectGymBot.book_class(class_details)

    efitness_bot = bot.EFitnessBot(session_builder.Session.build(), config=config['Grappling'])
    efitness_bot.book_class(class_details)
