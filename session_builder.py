import requests


class Session:
    """
    Responsible for preparing the Session with all parameters needed by Bot client class.
    """
    _session = requests.session()

    @classmethod
    def build(cls):
        """
        Returns a user-prepared :class:`Session`. Call it when you are done with
        parametrisation of your session

        :rtype: Session
        """
        return cls._session

    def with_proxy(self, proxy_dict):
        self._session.proxies.update(proxy_dict)
        return self

