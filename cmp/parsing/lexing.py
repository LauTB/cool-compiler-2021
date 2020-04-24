import re
import sys
from typing import List, Any, Generator, Tuple, Pattern, Optional, Callable, Dict


class Token:
    """
    A Token class.

    Parameters
    ----------
    lex: str
        Token's lexeme.
    token_type: Enum
        Token's type.
    """

    def __init__(self, lex, token_type, line=0, column=0):
        """
        :param lex: str
        :param token_type: Enum
        :param line: int
        :param column: int
        """
        self.lex: str = lex
        self.token_type: Any = token_type
        self.line: int = line
        self.column: int = column

    def __str__(self):
        return f'{self.token_type}: {self.lex}'

    def __repr__(self):
        return str(self)

    @property
    def is_valid(self):
        return True


class Lexer:
    def __init__(self, table: List[Tuple[str, str]], eof: str,
                 token_rules: Optional[Dict[str, Callable[['Lexer'], Optional[Token]]]] = None,
                 error_handler: Optional[Callable[['Lexer'], None]] = None):
        if token_rules is None:
            token_rules = {}

        if error_handler is None:
            error_handler = self.error

        self.lineno: int = 0  # Current line number
        self.column: int = 0  # Current column in the line
        self.position: int = 0  # Current position in recognition
        self.token: Token = Token('', '', 0, 0)  # Current token in recognition
        self.pattern: Pattern = self._build_regex(table)
        self.token_rules = token_rules  # type: Dict[str, Callable[['Lexer'], Optional[Token]]]
        self.contain_errors: bool = False
        self.error_handler = error_handler  # type: Callable[['Lexer'], None]
        self.eof: str = eof

    def tokenize(self, text: str) -> Generator[Token, None, None]:
        while self.position < len(text):
            match = self.pattern.match(text, pos=self.position)

            if match is None:
                self.contain_errors = True
                self.token = Token(text[self.position], None, self.lineno, self.column)
                self.error_handler(self)
                continue

            lexeme = match.group()
            token_type = match.lastgroup if match.lastgroup is not None else match.group()
            self.token = Token(lexeme, token_type, self.lineno, self.column)

            if token_type in self.token_rules:
                token = self.token_rules[token_type](self)
                if token is None or not isinstance(token, Token):
                    continue
                yield token

            yield self.token

            self.position = match.end()
            self.column += len(match.string)
        yield Token('$', self.eof, self.lineno, self.column)

    @staticmethod
    def print_error(error_msg):
        sys.stderr(error_msg)

    @staticmethod
    def error(lexer: 'Lexer') -> None:
        lexer.print_error(f'LexerError: Unexpected symbol "{lexer.token.lex}"\n')
        lexer.position += 1
        lexer.column += 1

    @staticmethod
    def _build_regex(table: List[Tuple[str, str]]) -> Pattern:
        return re.compile('|'.join(['(?P<%s>%s)' % (name, regex) for name, regex in table]))

    def __call__(self, text: str) -> List[Token]:
        return list(self.tokenize(text))
