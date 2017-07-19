import yaml


def _read_yaml(path):
    stream = file(path, 'r')
    conf = yaml.safe_load(stream)
    stream.close()
    return conf


def read_configuration(path='conf.yml'):
    return _read_yaml(path)


def read_credentials(path='creds.yml'):
    return _read_yaml(path)


class Conf:
    def __init__(self):
        self.config = read_configuration()
        self.creds = read_credentials()

