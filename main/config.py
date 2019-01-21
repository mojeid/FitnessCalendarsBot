class Config:
    APP_NAME = 'fitness_calendars_bot'


class PlatiniumGymConfig(Config):
    BASE_URL = 'https://platinium.perfectgym.pl/ClientPortal2'
    CLASS_DETAILS_REQUEST_METHOD = 'GET'


class CrossfitConfig(Config):
    BASE_URL = 'https://crossfit.perfectgym.pl/ClientPortal2'
    CLASS_DETAILS_REQUEST_METHOD = 'POST'
