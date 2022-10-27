import os

import yaml

basedir = os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))))

with open(os.path.join(basedir, 'config.yaml')) as f:
    settings = yaml.load(f.read(), yaml.FullLoader)


def get_yaml(key, default=None):
    data = settings
    for i in key.split('.'):
        data = data.get(i, default)
    return data


if __name__ == '__main__':
    print(settings)
