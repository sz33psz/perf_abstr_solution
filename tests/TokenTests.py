import unittest

from Token import Token, TokenType, InvalidTokenTypeException


class TokenTests(unittest.TestCase):
    def test_value_type_integer(self):
        tok = Token("Integer,3,5,6,3,7,2,6")
        self.assertEqual(tok.token_type, TokenType.Value)
        self.assertEqual(tok.token_value, ["integer", "3,5,6,3,7,2,6"])

    def test_value_type_string(self):
        val = """"This is some text that
        gets to the next line
                         and the next line and possibly any number of lines."""""
        tok = Token("ASC," + val)
        self.assertEqual(tok.token_type, TokenType.Value)
        self.assertEqual(tok.token_value, ["asc", val])

    def test_value_type_bool(self):
        tok = Token("bool,false")
        self.assertEqual(tok.token_type, TokenType.Value)
        self.assertEqual(tok.token_value, ["bool", "false"])

    def test_value_type_float(self):
        tok = Token("float,4.3,44.2")
        self.assertEqual(tok.token_type, TokenType.Value)
        self.assertEqual(tok.token_value, ["float", "4.3,44.2"])

    def test_stream_and_function(self):
        tok = Token("S4F10")
        self.assertEqual(tok.token_type, TokenType.StreamAndFunction)
        self.assertEqual(tok.token_value, [4, 10])

    def test_array_def(self):
        tok = Token("L,33")
        self.assertEqual(tok.token_type, TokenType.ArrayDef)
        self.assertEqual(tok.token_value, 33)

    def test_header(self):
        tok = Token("accept reply: true")
        self.assertEqual(tok.token_type, TokenType.Header)
        self.assertEqual(tok.token_value, ["accept reply", "true"])

    def test_unknown_type(self):
        self.assertRaises(InvalidTokenTypeException, Token, "L44")
        self.assertRaises(InvalidTokenTypeException, Token, "double,4.11")
        self.assertRaises(InvalidTokenTypeException, Token, "S3F1A")
