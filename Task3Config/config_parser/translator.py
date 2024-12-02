import yaml
from collections import OrderedDict

class OrderedDumper(yaml.Dumper):
    def represent_dict(self, data):
        return self.represent_mapping('tag:yaml.org,2002:map', data.items())

OrderedDumper.add_representer(OrderedDict, OrderedDumper.represent_dict)

class Translator:
    @staticmethod
    def to_yaml(parsed_data):
        # Используем OrderedDict, чтобы сохранить порядок
        def convert_to_ordered(data):
            if isinstance(data, dict):
                return OrderedDict((key, convert_to_ordered(value)) for key, value in data.items())
            elif isinstance(data, list):
                return [convert_to_ordered(item) for item in data]
            return data

        ordered_data = convert_to_ordered(parsed_data)
        return yaml.dump(ordered_data, Dumper=OrderedDumper, default_flow_style=False)
