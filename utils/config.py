import yaml
from box import Box
 
def load_config(config_file):
    with open(config_file, 'r') as stream:
        try:
            return Box(yaml.safe_load(stream))
        except yaml.YAMLError as exc:
            print(exc)
 
if __name__ == '__main__':
    ...