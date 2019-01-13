import bot

if __name__ == "__main__":
    # execute only if run as a script

    classDetails = {
        "startTime": "07:00",
        "date": "2019-01-16",
        "trainer": "Kamil Klich",
        "title": 'CrossFit'
    }

    perfectGymBot = bot.PerfectGymBot()
    perfectGymBot.client_login()._get_classess_id(classDetails)
