import configparser

def main():

    c = AppConfiguration()
    print(c.settings['meta'])

class AppConfiguration(object):

    def __init__(self, config_path='conf.ini'):

        self._path = config_path
        self.load_config()

    def load_config(self):

        self.c = configparser.ConfigParser(allow_no_value=True)
        self.c.optionxform=str
        self.c.read(self._path)

    @property
    def settings(self):

        return self.c

if __name__ == '__main__':
    main()