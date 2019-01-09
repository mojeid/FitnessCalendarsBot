# Module responsible for sending the requests to the page #

import requests

class PerfectGymBot:

    def client_login(self):
        requests.get('https://crossfit.perfectgym.pl/ClientPortal2/')
        payload = {'Login': 'mujeid@gmail.com', 'Password': 'Rsft789p'}
        requests.post("https://crossfit.perfectgym.pl/ClientPortal2/Auth/Login", data=payload)

