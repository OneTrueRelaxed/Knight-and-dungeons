import yaml
from abc import ABC


Levels = """
levels:
  - !empty_map {}
  - !special_map
    rat: 5
  - !special_map
    rat: 10
    knight: 5
  - !special_map
    rat: 10
    knight: 10
  - !random_map {}
"""

class MapFactory(yaml.YAMLObject):

    @classmethod
    def from_yaml(cls, loader, node):

        _map = cls.Map()
        _obj = cls.Objects()

        return {'map': _map, 'obj': _obj}

    @classmethod
    def create_map(cls):
        return cls.Map()

    @classmethod
    def create_objects(cls):
        return cls.Objects()

    class Map(ABC):
        pass

    class Objects(ABC):
        pass

class EndMap(MapFactory):
    yaml_tag = "!end_map"

    class Map:
        def __init__(self):
            pass

        def get_map(self):
            pass

    class Objects:
        def __init__(self):
            pass

        def get_objects(self):
            pass

class SpecialMap(MapFactory):
    yaml_tag = "!special_map"

    class Map:
        def __init__(self):
            pass

        def get_map(self):
            pass

    class Objects:
        def __init__(self):
            pass

        def get_objects(self):
            pass

class RandomMap(MapFactory):
    yaml_tag = "!random_map"

    class Map:
        def __init__(self):
            pass

        def get_map(self):
            pass

    class Objects:
        def __init__(self):
            pass

        def get_objects(self):
            pass


class EmptyMap(MapFactory):
    yaml_tag = "!empty_map"

    class Map:
        def __init__(self):
            pass

        def get_map(self):
            pass

    class Objects:
        def __init__(self):
            pass

        def get_objects(self):
            pass


if __name__ == "__main__":
    file = open("levels.yml", "r")
    level_list = yaml.load(file.read())['levels']
    level_list.append({'map': EndMap.Map(), 'obj': EndMap.Objects()})
    print(level_list)
    file.close()