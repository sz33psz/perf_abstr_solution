import unittest

from Token import Token
from ValueToken import ValueToken, NotValueTokenException


class ValueTokenTests(unittest.TestCase):
    def test_int_value_token(self):
        tok = Token("Integer,3,5,6,3,7,2,6")
        val_tok = ValueToken(tok)
        self.assertEqual(val_tok.get_value(), [3, 5, 6, 3, 7, 2, 6])

    def test_string_value_token(self):
        val = """"This is some text that
gets to the next line
and the next line and possibly any number of lines."""""
        tok = Token("ASC," + val)
        val_tok = ValueToken(tok)
        self.assertEqual(val_tok.get_value(), val.replace('\n', '\\n').replace('\t', '\\t')[1:-1])

    def test_bool_value_token(self):
        tok = Token("bool,true, true, false,    true")
        val_tok = ValueToken(tok)
        self.assertEqual(val_tok.get_value(), [True, True, False, True])

    def test_float_value_token(self):
        tok = Token("Float,3.44,3.1415,2.22,33333.344")
        val_tok = ValueToken(tok)
        self.assertEqual(val_tok.get_value(), [3.44, 3.1415, 2.22, 33333.344])

    def test_wrong_token_type_array(self):
        tok = Token("L,33")
        self.assertRaises(NotValueTokenException, ValueToken, tok)

    def test_wrong_token_heaer(self):
        tok = Token("accept reply: true")
        self.assertRaises(NotValueTokenException, ValueToken, tok)

    def test_wrong_token_stream_and_function(self):
        tok = Token("S4F10")
        self.assertRaises(NotValueTokenException, ValueToken, tok)