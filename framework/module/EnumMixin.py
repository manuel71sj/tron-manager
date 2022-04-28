from enum import Enum


class EnumMixin(Enum):
    def get_name(self):
        return self.name

    def get_value(self):
        return self.value
