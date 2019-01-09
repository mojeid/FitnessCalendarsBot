import Bot

if __name__ == "__main__":
    # execute only if run as a script
    perfectGymBot = Bot.PerfectGymBot()
    testValue = perfectGymBot.connect()
    print(testValue)