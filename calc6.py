
INTEGER, PLUS, MINUS, MUL, DIV, OPEN_PAR, CLOSE_PAR, EOF = 'INTEGER', 'PLUS', 'MINUS', 'MUL', 'DIV', 'OPEN_PAR', 'CLOSE_PAR', 'EOF'

class Token(object):
    def __init__(self, type, value):
        self.type = type
        self.value = value
    
    def __str__(self): 
        return 'Token({t}, {v})'.format(
            t = self.type,
            v = repr(self.value)
        )
    
    def __repr__(self):
        return self.__str__()

class AST(object):
    pass

class BinOp(AST): # operator node with children, each integer operand or another operator
    def __init__(self, left, op, right):
        self.token = self.op = op # operator token
        self.left = left
        self.right = right

class Num(AST): # integer operands
    def __init__(self, token):
        self.token = token  # integer token
        self.value = token.value

class Lexer(object):
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = text[0]
    
    def error(self):
        raise Exception("Invalid character at position {p}".format(p=self.pos+1))

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
        num = ''
        while self.current_char is not None and self.current_char.isdigit():
            num += self.current_char
        return int(num)

    def get_next_token(self):
        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_spaces()
            if self.current_char.isdigit():
                return Token(INTEGER, self.multigit())
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
    
class Parser(object): 
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()

    def error(self):
        raise Exception("Syntax Error!")
    
    def eat(self, type):
        if self.current_token.type == type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error()

    def factor(self):
        """factor : INTEGER | LPAREN expr RPAREN"""
        token = self.current_token
        if token.type == INTEGER:
            self.eat(INTEGER)
            return Num(token)
        elif token.type == OPEN_PAR:
            self.eat(OPEN_PAR)
            node = self.expr()
            self.eat(CLOSE_PAR)
            return node
        
    def term(self):
        """term: factor ((MUL|DIV) factor )* """
        node = self.factor()
        while self.current_token.type in (MUL, DIV):
            token = self.current_token
            if token.type == MUL:
                self.eat(MUL)
            elif token.type == DIV:
                self.eat(DIV)
            
            node = BinOp(left=node, op=token, right=self.factor())
        return node

    def expr(self):
        """expr: term ((PLUS|MINUS) term)* """
        node = self.term()
        while self.current_token.type in (PLUS, MINUS):
            token = self.current_token
            if token.type == PLUS:
                self.eat(PLUS)
            elif token.type == MINUS:
                self.eat(MINUS)
            
            node = BinOp(left=node, op=token, right=self.term())
        return node
    
    def parse(self):
        return self.expr()
    