import logging

from main import session_builder, bot
import configparser

if __name__ == "__main__":
    # execute only if run as a script
    config = configparser.ConfigParser()
    config.read('resources/configuration.ini')
    logging.basicConfig(level=config['DEFAULT']['logging_level'])

    classDetails = {
        "clubName": "CrossFit Lea",
        "startTime": "07:00",
        "date": "2019-02-04",
        "trainer": "Kamil Klich",
        "title": 'CrossFit Beginners'
    }

    perfectGymBot = bot.PerfectGymBot(session=session_builder.Session.build(), config=config['Crossfit'])
    perfectGymBot.book_class(classDetails)
