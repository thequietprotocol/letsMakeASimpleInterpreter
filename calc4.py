
#Definitions
INTEGER, PLUS, MINUS, MULT, DIV, EOF = 'INTEGER', 'PLUS', 'MINUS', 'MULT', 'DIV', 'EOF'

class Token(object):

    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __str__(self):
        return 'Token({type}, {value})'.format(
            type=self.type,
            value=repr(self.value)
        )
    
    def __repr__(self):
        return self.__str__()

class Lexer: 

    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = self.text[0]
    
    def error(self):
        raise Exception('Invalid Character')
    
    def advance(self):
        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.current_char = None
        else:
            self.current_char = self.text[self.pos]

    def integer(self):
        result = ''
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        return int(result)
    
    def skip_spaces(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    #The lexer/scanner/tokenizer - outputs objects of class Token
    def get_next_token(self):
        
        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_spaces()
                continue
            if self.current_char.isdigit():
                return Token(INTEGER, self.integer())
            if self.current_char == '+':
                self.advance()
                return Token(PLUS, '+')
            if self.current_char == '-':
                self.advance()
                return Token(MINUS, '-')
            if self.current_char == '*':
                self.advance()
                return Token(MULT, '*')
            if self.current_char == '/':
                self.advance()
                return Token(DIV, '/')
            
            self.error()

        return Token(EOF, None)

class Interpreter:

    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()

    def error(self):
        raise Exception('Syntax Error')

    def eat(self, token_type):

        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error()

    def factor(self):
        token = self.current_token #save current token before calling eat
        self.eat(INTEGER)
        return token.value

    #Asserting a structure: INT -> OPER -> INT ... i.e. 'parsing' & interpreting
    def expr(self):

        self.current_token = self.get_next_token()

        #Accumulate result: take first term and move to first op
        result = self.factor()

        while self.current_token.type in (PLUS, MINUS, MULT, DIV):  # ((PLUS|MINUS|MULT|DIV)factor)*
            oper = self.current_token
            # (PLUS|MINUS|MULT|DIV)factor
            if oper.type == PLUS:
                #move to term after +
                self.eat(PLUS)
                #term after + added and moved to next operator
                result = result + self.factor()
            elif oper.type == MINUS:
                self.eat(MINUS)
                result = result - self.factor()
            elif oper.type == MULT:
                self.eat(MULT)
                result = result * self.factor()
            else:
                self.eat(DIV)
                result = result // self.factor()

        return result
    
def main():
    while True: 
        try:
            text = input('calc: ')
        except EOFError:
            break
        if not text:  #if only empty string
            continue
        interpreter = Interpreter(text)
        result = interpreter.expr()
        print(result)

if __name__ == '__main__':
    main()