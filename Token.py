import re


class InvalidTokenTypeException(Exception):
    def __init__(self, token):
        self.token = token

    def __repr__(self):
        return "Invalid token type for token " + self.token

class InvalidTokenValueException(Exception):
    def __init__(self, token):
        self.token = token

    def __repr__(self):
        return "Invalid token value for token " + self.token


class TokenType:
    def __init__(self):
        pass

    StreamAndFunction, Header, ArrayDef, Value = range(4)

    STREAM_AND_FUNCTION_PATTERN = re.compile("^S([0-9]+)F([0-9]+)$")
    ARRAY_DEF_PATTERN = re.compile("^L,([0-9]+)$")
    VALUE_TYPES = ("asc", "bool", "integer", "float")
    HEADERS = ("accept reply") # can be extended later

    @classmethod
    def from_token(cls, token):
        if cls.ARRAY_DEF_PATTERN.match(token):
            return cls.ArrayDef
        if cls.STREAM_AND_FUNCTION_PATTERN.match(token):
            return cls.StreamAndFunction
        if token.lower().startswith(cls.VALUE_TYPES):
            return cls.Value
        if token.startswith(cls.HEADERS):
            return cls.Header
        raise InvalidTokenTypeException(token)


class Token(object):
    def __init__(self, token):
        self.token_type = TokenType.from_token(token)
        self.token_value = self._determine_value(token)

    def _determine_value(self, token):
        if self.token_type == TokenType.ArrayDef:
            return int(TokenType.ARRAY_DEF_PATTERN.match(token).groups()[0])
        if self.token_type == TokenType.StreamAndFunction:
            groups = TokenType.STREAM_AND_FUNCTION_PATTERN.match(token).groups()
            return [int(groups[0]), int(groups[1])]
        if self.token_type == TokenType.Value:
            splitted = token.split(",")
            return [splitted[0].lower(), ",".join(splitted[1:])]
        if self.token_type == TokenType.Header:
            splitted = token.split(":")
            return [splitted[0], splitted[1].strip()]
        raise InvalidTokenValueException(token)
