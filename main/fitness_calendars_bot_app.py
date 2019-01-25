from main import session_builder, bot, json_parser
import configparser

if __name__ == "__main__":
    # execute only if run as a script

    classDetails = {
        "clubName": "CrossFit Lea",
        "startTime": "07:00",
        "date": "2019-01-28",
        "trainer": "Kamil Klich",
        "title": 'CrossFit Beginners'
    }

    config = configparser.ConfigParser()
    config.read('resources/configuration.ini')

    perfectGymBot = bot.PerfectGymBot(session=session_builder.Session.build(), config=config['Crossfit'])
    perfectGymBot.cancel_booking(classDetails)
