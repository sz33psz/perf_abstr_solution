import unittest

from Token import TokenType
from Tokenizer import Tokenizer
from ValueToken import ValueToken

FULL_EXAMPLE = """


S2F3
accept reply: true
L,3
ASC,"This is some text that
gets to the next line
and the next line and possibly any number of lines."
L,3
integer,6
bool,true
float,5.21
L,2
ASC,"More text"
L,1
integer,8

S10F11
accept reply: false
asc,"test2"

S9F1
accept reply: false
L,0

S1F15
accept reply: true
L,4
bool,true,false,true,true,false
Integer,3,5,6,3,7,2,6
float,9
L,3
integer,4
L,2
float, 4.6,9.3

bool, false
L,2
L,1
L,2
integer,5
L,0
L,3
asc,"test3"
asc,"test
4"
L,0


        """


class TokenizerTests(unittest.TestCase):
    def test_basic_tokenize(self):
        str = """
S10F11
accept reply: false
asc,"test2"
        """
        tokenizer = Tokenizer()
        result = tokenizer.tokenize(str)
        self.assertEqual(len(result), 3)

    def test_full_tokenize(self):
        format_1_string = FULL_EXAMPLE
        tokenizer = Tokenizer()
        result = tokenizer.tokenize(format_1_string)
        self.assertEqual(len(result), 38)
        self.assertEqual(result[0].token_type, TokenType.StreamAndFunction)
        self.assertEqual(result[0].token_value, [2, 3])
        self.assertEqual(result[1].token_type, TokenType.Header)
        self.assertEqual(result[1].token_value, ["accept reply", "true"])
        self.assertEqual(result[2].token_type, TokenType.ArrayDef)
        self.assertEqual(result[2].token_value, 3)
        self.assertEqual(result[3].token_type, TokenType.Value)
        res_3_value_token = ValueToken(result[3])
        res_3_string_value = """This is some text that
gets to the next line
and the next line and possibly any number of lines."""
        self.assertEqual(res_3_value_token.get_value(), res_3_string_value.replace('\n', '\\n').replace('\t', '\\t'))
