
class JsonResponsePostProcessor(object):
    ARRAY_START = "["
    ARRAY_END = "]"
    OBJECT_START = "{"
    OBJECT_END = "}"
    KEY_VALUE_SEPARATOR = ": "
    ELEMENTS_SEPARATOR = ","
    STRING_PREFIX_POSTFIX = "\""
    LINE_END = "\n"

    def __init__(self, indent="\t"):
        self.indent = indent

    def post_process(self, response):
        string_list = []
        self.process(response, string_list)
        return ''.join(string_list)

    def process(self, element, string_list, indentation=''):
        element_type = type(element)
        if element_type is list:
            self._emit_list(element, indentation, string_list)
        elif element_type is dict:
            self._emit_dict(element, indentation, string_list)
        elif element_type is str:
            self._emit_str(element, string_list)
        elif element_type is bool:
            self._emit_bool(element, string_list)
        else:
            self._emit_number(element, string_list)

    def _emit_number(self, element, string_list):
        string_list.append(str(element))

    def _emit_bool(self, element, string_list):
        string_list.append('true' if element else 'false')

    def _emit_str(self, element, string_list):
        string_list.append(self.STRING_PREFIX_POSTFIX)
        string_list.append(element)
        string_list.append(self.STRING_PREFIX_POSTFIX)

    def _emit_dict(self, element, indentation, string_list):
        string_list.append(self.OBJECT_START)
        string_list.append(self.LINE_END)
        items = list(element.iteritems())
        if items:
            for kv in items[:-1]:
                self._emit_dict_element(kv[0], kv[1], string_list, indentation)
            self._emit_dict_element(items[-1][0], items[-1][1], string_list, indentation, True)
        string_list.append(self.LINE_END)
        string_list.append(indentation)
        string_list.append(self.OBJECT_END)

    def _emit_list(self, element, indentation, string_list):
        string_list.append(self.ARRAY_START)
        string_list.append('\n')
        if element:
            for list_element in element[:-1]:
                self._emit_array_element(list_element, string_list, indentation)
            self._emit_array_element(element[-1], string_list, indentation, True)
        string_list.append(self.LINE_END)
        string_list.append(indentation)
        string_list.append(self.ARRAY_END)

    def _emit_array_element(self, element, string_list, indentation='', last=False):
        string_list.append(indentation + self.indent)
        self.process(element, string_list, indentation + self.indent)
        if not last:
            string_list.append(self.ELEMENTS_SEPARATOR)
            string_list.append(self.LINE_END)

    def _emit_dict_element(self, key, val, string_list, indentation='', last=False):
        string_list.append(indentation + self.indent)
        self._emit_str(key, string_list)
        string_list.append(self.KEY_VALUE_SEPARATOR)
        self.process(val, string_list, indentation + self.indent)
        if not last:
            string_list.append(self.ELEMENTS_SEPARATOR)
            string_list.append(self.LINE_END)
