
# Token Types

INTEGER, PLUS, MINUS, MUL, DIV, OPEN_PAR, CLOSE_PAR, EOF = 'INTEGER', 'PLUS', 'MINUS', 'MUL', 'DIV', 'OPEN_PAR', 'CLOSE_PAR', 'EOF'

class Token(object):
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __str__(self):
        return 'Token({t}, {v})'.format(
            t=self.type,
            v=repr(self.value)
        )
    
    def __repr__(self):
        return self.__str__()

class Lexer(object):
    def __init__(self, text):
        self.text = text
        self.current_char = self.text[0]
        self.pos = 0

    def error(self):
        raise Exception('Invalid character at position {p}'.format(p=self.pos+1))
    
    def advance(self):
        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.current_char = None
        else:
            self.current_char = self.text[self.pos]

    def skip_spaces(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()
    
    def multidigit(self):
        res = ''
        while self.current_char is not None and self.current_char.isdigit():
            res += self.current_char
            self.advance()
        return int(res)

    def get_next_token(self):
        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_spaces()
                continue
            if self.current_char.isdigit():
                return Token(INTEGER, self.multidigit())
            if self.current_char == '+':
                self.advance()
                return Token(PLUS, '+')
            if self.current_char == '-':
                self.advance()
                return Token(MINUS, '-')
            if self.current_char == '*':
                self.advance()
                return Token(MUL, '*')
            if self.current_char == '/':
                self.advance()
                return Token(DIV, '/')
            if self.current_char == '(':
                self.advance()
                return Token(OPEN_PAR, '(')
            if self.current_char == ')':
                self.advance()
                return Token(CLOSE_PAR, ')')
            
            self.error()

        return Token(EOF, None)

class Interpreter(object):
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()

    def error(self):
        raise Exception('Syntax Error')

    def eat(self, type):
        if self.current_token.type == type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error()

    def factor(self):
        token = self.current_token
        if token.type == INTEGER:
            self.eat(INTEGER)
            return token.value
        elif token.type == OPEN_PAR:
            self.eat(OPEN_PAR)
            result = self.expr()
            self.eat(CLOSE_PAR)
            return result
    
    def term(self):
        result_term = self.factor()
        while self.current_token.type in (MUL, DIV):
            if self.current_token.type == MUL:
                self.eat(MUL)
                result_term = result_term * self.factor()
            else:
                self.eat(DIV)
                result_term = result_term // self.factor()
        return result_term

    def expr(self):

        result = self.term()
        while self.current_token.type in (PLUS, MINUS):
            if self.current_token.type == PLUS:
                self.eat(PLUS)
                result = result + self.term()
            else:
                self.eat(MINUS)
                result = result - self.term()
        return result

def main():

    while True:
        try:
            text = input('calculate:')
        except EOFError:
            break
        if not text:
            continue
        lexer = Lexer(text)
        interpreter = Interpreter(lexer)
        result = interpreter.expr()
        print(result)

if __name__ == '__main__':
    main()
