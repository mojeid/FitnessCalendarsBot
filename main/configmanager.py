import configparser


class ConfigManager:
    _config = None

    def __load_configuration(self):
        """ Loads default configuration file """
        self._config = configparser.ConfigParser()
        self._config.read('../main/resources/configuration.ini')

    def read_base_url(self, config_name):
        self.__load_configuration()
        return self._config.get(config_name, "BaseURL")


class CredentialsManager:
    _credentials_file = None

    def __load_credentials_file(self):
        self._credentials_file = configparser.ConfigParser()
        self._credentials_file.read("../main/resources/credentials.ini")

    def read_credentials(self, site_name):
        """ Loads credentials for given site"""
        self.__load_credentials_file()
        username = self._credentials_file.get(site_name, "username")
        password = self._credentials_file.get(site_name, "password")
        return [username, password]
