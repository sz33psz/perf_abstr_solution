import unittest
import time

from ResponseBuilder import ResponseBuilder
from Tokenizer import Tokenizer
from TokenizerTests import FULL_EXAMPLE


class ResponseBuilderTests(unittest.TestCase):
    def test_full_example(self):
        tokenizer = Tokenizer()
        response_builder = ResponseBuilder()
        start_time = time.time()
        tokens = tokenizer.tokenize(FULL_EXAMPLE)
        result = response_builder.process_tokens(tokens)
        end_time = time.time()
        print result
        print "Calculated in %s" % str(end_time - start_time)