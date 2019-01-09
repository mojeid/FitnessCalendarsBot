import bot

if __name__ == "__main__":
    # execute only if run as a script
    perfectGymBot = bot.PerfectGymBot()
    testValue = perfectGymBot.connect()
    print(testValue)