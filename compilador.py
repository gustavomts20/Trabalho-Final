from ply import lex, yacc # type: ignore
import logging

context = 0
symbols = {}

def get_context():
    return context

reserved = {
    'if': 'IF', 'else': 'ELSE', 'for': 'FOR', 'while': 'WHILE', 'main': 'MAIN',
    'int': 'INT', 'float': 'FLOAT', 'char': 'CHAR', 'void': 'VOID',
    'string': 'STRING', 'double': 'DOUBLE', 'printf': 'PRINTF',
    'scanf': 'SCANF', 'return': 'RETURN', 'uint8': 'UNSIGNEDINT8', 'uint16': 'UNSIGNEDINT16',
}

tokens = [
    'EQUALS', 'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'POWER',
    'LPAREN', 'RPAREN', 'LT', 'LE', 'GT', 'GE', 'NE',
    'COMMA', 'SEMI', 'INTEGER', 'FLOATN',
    'ID', 'SEMICOLON', 'RBRACES', 'LBRACES', 'QUOTE',
    'ITERPLUS', 'ITERMIN', 'TRUE',
] + list(reserved.values())

t_ignore = ' \t\n'

t_EQUALS = r'='
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_POWER = r'\^'
t_DIVIDE = r'/'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_RBRACES = r'\}'
t_LBRACES = r'\{'
t_SEMICOLON = r'\;'
t_LT = r'<'
t_LE = r'<='
t_GT = r'>'
t_GE = r'>='
t_NE = r'!='
t_COMMA = r'\,'
t_SEMI = r';'
t_INTEGER = r'\d+'
t_FLOATN = r'((\d*\.\d+)(E[\+-]?\d+)?|([1-9]\d*E[\+-]?\d+))'
t_STRING = r'\".*?\"'
t_QUOTE = r'\''
t_ITERPLUS = r'\+\+'
t_ITERMIN = r'\-\-'
t_TRUE = r'\;\;'

def t_REM(t):
    r'REM .*'
    return t

def t_ID(t):
    r'[a-zA-Z][a-zA-Z0-9]*'
    t.type = reserved.get(t.value,'ID')
    return t

def t_error(t):
    print("Illegal character %s" % t.value[0])
    t.lexer.skip(1)

lexer = lex.lex()

#####################################################

def p_start(p):
    '''start : INT MAIN LPAREN RPAREN main_block'''
    print("End of analysis .. ")
    print(symbols)

def p_main_block(p):
    '''main_block : LBRACES declarations expressions_functions functions RETURN INTEGER SEMICOLON RBRACES 
                    | LBRACES function_declaration declarations expressions_functions functions RETURN INTEGER SEMICOLON RBRACES
                    | LBRACES empty RETURN INTEGER SEMICOLON RBRACES
                    | LBRACES declarations expressions_functions functions RBRACES'''
    print("Executing main block .. ")

def p_declarations(p):
    '''declarations : type ID SEMICOLON
                 | type ID COMMA ID SEMICOLON
                 | type ID COMMA ID COMMA ID SEMICOLON
                 | type ID SEMICOLON declarations
                 | type ID EQUALS INTEGER SEMICOLON declarations
                 | type ID EQUALS FLOATN SEMICOLON declarations
                 | CHAR ID EQUALS QUOTE ID QUOTE SEMICOLON declarations
                 | empty'''
    print("Processing declarations .. ")
    current_scope = get_context()

    if len(p) == 4:
        if p[2] in symbols and symbols[p[2]]['context'] == current_scope:
            print(f"Error: Variable {p[2]} already declared in this scope")
        else:
            symbols[p[2]] = {'value': None, 'type': p[1], 'context': current_scope}
    elif len(p) == 6:
        for i in [2, 4]:
            if p[i] in symbols and symbols[p[i]]['context'] == current_scope:
                print(f"Error: Variable {p[i]} already declared in this scope")
            else:
                symbols[p[i]] = {'value': None, 'type': p[1], 'context': current_scope}
    elif len(p) == 8:
        for i in [2, 4, 6]:
            if p[i] in symbols and symbols[p[i]]['context'] == current_scope:
                print(f"Error: Variable {p[i]} already declared in this scope")
            else:
                symbols[p[i]] = {'value': None, 'type': p[1], 'context': current_scope}
    elif len(p) == 5:
        symbols[p[2]] = {'value': None, 'type': p[1], 'context': current_scope}
        print(str(symbols[p[2]]))

def p_type(p):
    ''' type : INT
            | FLOAT
            | CHAR 
            | STRING
            | DOUBLE
            | VOID
            | UNSIGNEDINT8
            | UNSIGNEDINT16 '''
    print("Defining type .. ")
    p[0] = p[1]

def p_function_declaration(p):
    ''' function_declaration : type ID LPAREN function_expression RPAREN SEMICOLON
                | empty'''

def p_function_expression(p):
    ''' function_expression : type ID COMMA function_expression
                | type ID
                | empty'''
    
def p_functions(p):
    ''' functions : IF LPAREN function_declarations RPAREN LBRACES expressions_functions RBRACES
            | IF LPAREN function_declarations RPAREN LBRACES expressions_functions RBRACES function_continuation functions
            | FOR LPAREN TRUE RPAREN LBRACES expressions_functions functions RBRACES functions
            | FOR LPAREN ID EQUALS INTEGER SEMICOLON ID function_comparisons ID SEMICOLON ID ITERPLUS RPAREN LBRACES expressions_functions RBRACES functions
            | WHILE LPAREN INTEGER RPAREN LBRACES expressions_functions RBRACES functions
            | empty'''

def p_function_declarations(p):
    ''' function_declarations : ID function_comparisons ID
                        | ID function_comparisons INTEGER
                        | ID function_comparisons FLOATN
                        | ID function_comparisons STRING
                        | ID function_comparisons QUOTE ID QUOTE'''
    if p[1] == p[3]:   
        print("Declarations have the same identifier: " + p[1])
    else:
        print("Declarations have different identifiers: " + p[1] + ", " + p[3])


def p_function_comparisons(p):
    ''' function_comparisons : LT
                        | LE
                        | GT
                        | GE
                        | NE
                        | EQUALS EQUALS'''
    
def p_operations(p):
    ''' operations : EQUALS
                | PLUS
                | MINUS
                | TIMES
                | DIVIDE
                | POWER'''
    
def p_expressions_functions(p):
    ''' expressions_functions : ID EQUALS ID SEMICOLON expressions_functions
                        | ID EQUALS INTEGER SEMICOLON expressions_functions
                        | ID EQUALS ID operations INTEGER SEMICOLON expressions_functions
                        | ID EQUALS ID operations ID SEMICOLON expressions_functions
                        | ID ITERPLUS SEMICOLON expressions_functions
                        | ID ITERMIN SEMICOLON expressions_functions
                        | PRINTF LPAREN STRING RPAREN SEMICOLON expressions_functions
                        | empty'''
    if len(p) > 1:
        expression_parts = [str(part) for part in p[1:-1] if part is not None]
        expression_str = " ".join(expression_parts)
        print("Expression encountered: " + expression_str)
    else:
        print("Empty expression")
    
def p_function_continuation(p):
    ''' function_continuation : ELSE LBRACES expressions_functions functions RBRACES
                        | ELSE IF LPAREN function_declarations RPAREN LBRACES expressions_functions functions RBRACES function_continuation
                        | empty'''
def p_empty(p):
    ''' empty :'''
    pass

yacc.yacc()

logging.basicConfig(
    level=logging.INFO,
    filename="parselog.txt"
)

file = open("input.txt",'r')
data = file.read()

lexer.input(data)

for tok in lexer:
    print(tok)

yacc.parse(data, debug=logging.getLogger())
