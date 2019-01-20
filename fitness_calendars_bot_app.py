import bot

if __name__ == "__main__":
    # execute only if run as a script

    classDetails = {
        "clubName": "CF Kraków",
        "startTime": "08:00",
        "date": "2019-01-18",
        "trainer": "Filip Jopek",
        "title": 'WOD'
    }

    perfectGymBot = bot.PerfectGymBot()
    class_id = perfectGymBot.client_login().book_class(classDetails)

    import session_builder
    session_builder.SessionBuilder.create().with_proxy().build()


