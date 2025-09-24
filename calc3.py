
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

class Interpreter:

    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_token = None
        self.current_char = text[0]

    def error(self):
        raise Exception('Error parsing input')
    
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
                token = Token(INTEGER, self.integer())
                return token
            
            if self.current_char == '+':
                token = Token(PLUS, self.current_char)
                self.advance()
                return token
            
            if self.current_char == '-':
                token = Token(MINUS, self.current_char)
                self.advance()
                return token
            
            if self.current_char == '*':
                token = Token(MULT, self.current_char)
                self.advance()
                return token
            
            if self.current_char == '/':
                token = Token(DIV, self.current_char)
                self.advance()
                return token


            self.error()

        return Token(EOF, None)
    

    def eat(self, token_type):

        if self.current_token.type == token_type:
            self.current_token = self.get_next_token()
        else:
            self.error()

    #Asserting a structure: INT -> OPER -> INT ... i.e. 'parsing' & interpreting
    def expr(self):

        self.current_token = self.get_next_token()

        #To accumulate result, first term
        result = self.current_token.value
        #move to operator after first term
        self.eat(INTEGER)  

        while self.current_token.type in (PLUS, MINUS, MULT, DIV):
            oper = self.current_token
            if oper.type == PLUS:
                #move to term after +
                self.eat(PLUS)
                #term after + added
                result = result + self.current_token.value
                #move to next operator
                self.eat(INTEGER) 
            elif oper.type == MINUS:
                self.eat(MINUS)
                result = result - self.current_token.value
                self.eat(INTEGER)  
            elif oper.type == MULT:
                self.eat(MULT)
                result = result * self.current_token.value
                self.eat(INTEGER)  
            else:
                self.eat(DIV)
                result = result / self.current_token.value
                self.eat(INTEGER)   

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