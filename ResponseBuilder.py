from ResponsePostProcessor import JsonResponsePostProcessor
from Token import TokenType
from Tokenizer import Tokenizer
from ValueToken import ValueToken


class InvalidSyntaxException(Exception):
    def __init__(self, token):
        self.token = token

    def __str__(self):
        return "Invalid syntax. Unexpected token: %s" % self.token


class UnknownHeaderException(Exception):
    def __init__(self, header_name):
        self.header_name = header_name

    def __str__(self):
        return "Unknown header: %s" % self.header_name


class ResponseBuilder(object):
    RESULT = "result"
    REMAINING = "remaining_tokens"
    # header_label: (header_name, header_value_converter)
    HEADER_MAPPINGS = {
        "accept reply": ("reply", lambda v: v.lower() == 'true')
    }

    def __init__(self, post_processor=JsonResponsePostProcessor()):
        self.post_processor = post_processor

    def process_tokens(self, tokens):
        remaining = tokens
        result = []
        while remaining:
            current_command = {}
            res = self.process_header(remaining)
            remaining = res[self.REMAINING]
            current_command["header"] = res[self.RESULT]
            res = self.process_body(remaining)
            remaining = res[self.REMAINING]
            current_command["body"] = res[self.RESULT]
            result.append(current_command)
        return self.post_processor.post_process(result)

    def process_header(self, tokens):
        first_token = tokens[0]
        self._check_type(first_token, TokenType.StreamAndFunction)

        result = {
            "stream": first_token.token_value[0],
            "function": first_token.token_value[1]
        }

        header_tokens = 0
        for t in tokens[1:]:
            if t.token_type != TokenType.Header:
                break
            header_tokens += 1
            header_mapping = self.HEADER_MAPPINGS[t.token_value[0]]
            if header_mapping is None:
                raise UnknownHeaderException(t.token_value[0])
            header_name = header_mapping[0]
            header_value_converter = header_mapping[1]
            result[header_name] = header_value_converter(t.token_value[1])

        return {
            self.RESULT: result,
            self.REMAINING: tokens[1+header_tokens:]
        }

    def process_body(self, tokens):
        first_token = tokens[0]
        if first_token.token_type == TokenType.Value:
            return self.process_value(tokens)
        elif first_token.token_type == TokenType.ArrayDef:
            return self.process_array(tokens)

    def process_value(self, tokens):
        first_token = tokens[0]
        self._check_type(first_token, TokenType.Value)
        value_token = ValueToken(first_token)

        result = {
            "format": value_token.get_format(),
            "value": value_token.get_value()
        }
        return {
            self.RESULT: result,
            self.REMAINING: tokens[1:]
        }

    def process_array(self, tokens):
        first_token = tokens[0]
        self._check_type(first_token, TokenType.ArrayDef)
        array_size = first_token.token_value
        result = []
        remaining = tokens[1:]
        if array_size == 0:
            return {
                self.RESULT: result,
                self.REMAINING: remaining
            }

        for i in range(0, array_size):
            first_array_value = remaining[0]
            if first_array_value.token_type == TokenType.ArrayDef:
                process_result = self.process_array(remaining)
                remaining = process_result[self.REMAINING]
                result.append(process_result[self.RESULT])
            elif first_array_value.token_type == TokenType.Value:
                process_result = self.process_value(remaining)
                remaining = process_result[self.REMAINING]
                result.append(process_result[self.RESULT])
            else:
                raise InvalidSyntaxException(first_array_value)

        return {
            self.REMAINING: remaining,
            self.RESULT: result
        }

    def _check_type(self, token, type):
        if token.token_type != type:
            raise InvalidSyntaxException(token)


def process(input_string, post_processor=JsonResponsePostProcessor()):
    tokenizer = Tokenizer()
    response_builder = ResponseBuilder(post_processor)
    tokens = tokenizer.tokenize(input_string)
    return response_builder.process_tokens(tokens)