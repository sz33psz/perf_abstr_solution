from Token import Token


class Tokenizer(object):
    def __init__(self):
        pass

    def tokenize(self, format_one_string):
        tokens = []
        lines = format_one_string.splitlines()
        current_line_idx = 0
        while current_line_idx < len(lines):
            current_line = lines[current_line_idx]
            if len(current_line.strip()) == 0:
                current_line_idx += 1
                continue
            if current_line.count("\"") == 1:
                current_token = current_line
                current_line_idx += 1
                for l in lines[current_line_idx:]:
                    current_token += "\n" + l
                    current_line_idx += 1
                    if l.count("\""):
                        break

                tokens.append(Token(current_token))

            else:
                tokens.append(Token(current_line))
                current_line_idx += 1

        return tokens
