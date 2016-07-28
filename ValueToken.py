from Token import TokenType


class NotValueTokenException(Exception):
    pass


class ValueToken(object):
    VALUE_FORMAT_MAPPINGS = {
        "asc": "A",
        "bool": "Boolean",
        "integer": "U4",
        "float": "F4"
    }

    def __init__(self, token):
        if token.token_type != TokenType.Value:
            raise NotValueTokenException

        self.token_value_type = token.token_value[0]
        self.token_value = token.token_value[1]

    def get_value(self):
        return {
            "asc": self._string_value,
            "bool": self._bool_value,
            "integer": self._int_value,
            "float": self._float_value
        }[self.token_value_type](self.token_value)

    def get_format(self):
        return self.VALUE_FORMAT_MAPPINGS[self.token_value_type]

    def _string_value(self, param):
        escaped = param.replace('\n', '\\n').replace('\t', '\\t')
        return escaped[1:-1]  # strip beginning and end doublequote

    def _bool_value(self, param):
        res = [el.lower().strip() == 'true' for el in param.split(",")]
        return self._remove_array_if_necessary(res)

    def _int_value(self, param):
        res = [int(el) for el in param.split(",")]
        return self._remove_array_if_necessary(res)

    def _float_value(self, param):
        res = [float(el) for el in param.split(",")]
        return self._remove_array_if_necessary(res)

    def _remove_array_if_necessary(self, res):
        if len(res) == 1:
            return res[0]
        else:
            return res
