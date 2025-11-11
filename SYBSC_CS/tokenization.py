import re

token_specification = [
    ('NUMBER', r'\d+(\.\d*)?'),
    ('ASSIGN', r'='),
    ('END', r';'),
    ('ID', r'[A-Za-z]+'),
    ('OP', r'[+\-*/]'),
    ('SKIP', r'[ \t]+'),
    ('MISMATCH', r'.'),
]
tok_regex = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in token_specification)

def tokenize(code):
    for match in re.finditer(tok_regex, code):
        kind = match.lastgroup
        value = match.group()
        if kind == 'SKIP':
            continue
        elif kind == 'MISMATCH':
            raise RuntimeError(f'Unexpected token: {value}')
        yield kind, value

code = "x = a + b * 5;"
for token in tokenize(code):
    print(token)