import configparser
import logging

from main import session_builder, bot
from main.data_containers import FitnessClasses

if __name__ == "__main__":
    # execute only if run as a script
    config = configparser.ConfigParser()
    config.read('resources/configuration.ini')
    logging.basicConfig(level=config['DEFAULT']['logging_level'])

    class_details = FitnessClasses(None, 'BOKS Nowy nabór', '2019-02-25', '21:00', 'Tomasz Broda', 'Platinium Plaza',
                                   None)

    perfectGymBot = bot.PerfectGymBot(session=session_builder.Session.build(), config=config['Platinium'])
    perfectGymBot.book_class(class_details)
