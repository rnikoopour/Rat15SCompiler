import inspect
import pdb
def p():
    pass
pdb.set_trace = p

"""
@package recursive_decent_parser
This parses the tokens generated by the Lexer
"""
import sys
from lexicalanalyzer import Lexer

index = 0
num_double_at = 0

ERROR_STRING = '\nError on line {1}\nToken type is "{2}"\nLexeme is "{3}"\nDescription: {0}\n'
INPUT_FILE = ''
MAX_DOUBLE_AT = 2
TOKENS = []
OUTPUT_FILE = None
PrintParseInfo = None
PrintCurrentTokenInfo = None

def PrintCurrentTokenInfoToScreen():
    print('Token: {0}\t\tLexeme: {1}'.format(TOKENS[index].token_type, TOKENS[index].lexeme))

def PrintCurrentTokenInfoToFile():
    OUTPUT_FILE.write('Token: {0}\t\tLexeme: {1}\n'.format(TOKENS[index].token_type, TOKENS[index].lexeme))
   
def SayErrorAndDie(description):
    print(ERROR_STRING.format(description, TOKENS[index].line_number, TOKENS[index].token_type, TOKENS[index].lexeme))
    print('Failed to parse file "{0}" exiting'.format(INPUT_FILE))
    sys.exit(1)

def PrintParseInfoToScreen(leftside, rightside):
    print('\t{0} -> {1}'.format(leftside, rightside))

def PrintParseInfoToFile(leftside, rightside):
    OUTPUT_FILE.write('\t{0} -> {1}\n'.format(leftside, rightside))

def Parser(input_file, output_file=None):
    """
    @brief Outputs how to each token was parsed

    @param[in] input_file The source code we are parsing
    @param[in] output_file The file to write all output to
    """
    # Allow us to mutate globals
    global index
    global INPUT_FILE
    global TOKENS
    global OUTPUT_FILE
    global PrintParseInfo
    global PrintCurrentTokenInfo
    
    INPUT_FILE = input_file
    index = 0
    TOKENS = Lexer(input_file)
    if output_file is not None:
        OUTPUT_FILE = open(output_file, 'w')
        PrintCurrentTokenInfo = PrintCurrentTokenInfoToFile
        PrintParseInfo = PrintParseInfoToFile
    else:
        PrintCurrentTokenInfo = PrintCurrentTokenInfoToScreen
        PrintParseInfo = PrintParseInfoToScreen
        
    Rat15S()

def Empty():
    PrintParseInfo('<Empty>', 'epsilon')

def Qualifier(should_print=True):
    global index
    if TOKENS[index] == 'real':
        if should_print:
            PrintCurrentTokenInfo()
            index += 1
        PrintParseInfo('<Qualifier>', 'real')
    elif TOKENS[index] == 'boolean':
        if should_print:
            PrintCurrentTokenInfo()
            index += 1
        PrintParseInfo('<Qualifier>', 'boolean')
    elif TOKENS[index] == 'int':
        if should_print:
            PrintCurrentTokenInfo()
            index += 1
        PrintParseInfo('<Qualifier>', 'int')
    else:
        SayErrorAndDie('Expected Qualifier "real", "int", or "boolean"')
    
def IDs():
    global index
    multiple_ids = False
    for token in TOKENS[index+1:]:
        if token.lexeme in ';:[':
            break
        elif token == ',':
            multiple_ids = True
            break

    if multiple_ids:
        PrintParseInfo('<IDs>', '<Identifier>, <IDs>')
        if TOKENS[index].token_type == 'Identifier':
            index += 1
        else:
            SayErrorAndDie('Expected Identifier')
        PrintCurrentTokenInfo()
        index += 1
        PrintCurrentTokenInfo()
        IDs()
    else:
        PrintParseInfo('<IDs>', '<Identifier>')


def Declaration():
    global index
    Qualifier()
    PrintCurrentTokenInfo()
    IDs()
    index += 1
        
def DeclarationList():
    global index
    multiple_declarations = False
    num_keywords = 0
    for token in TOKENS[index:]:
        if token.token_type == 'Keyword':
            num_keywords += 1
        if num_keywords > 1:
            multiple_declarations = True
            break
        if token in ['{', '@@']:
            break

    if multiple_declarations:
        PrintParseInfo('<Declaration List>', '<Declaration>; <Decalartion List>')
        Declaration()
        if TOKENS[index] == ';':
            PrintCurrentTokenInfo()
            index += 1
            DeclarationList()
        else:
            SayErrorAndDie('Expected separator ";"')
    else:
        PrintParseInfo('<Declaration List>', '<Declaration>;')
        Declaration()
        if TOKENS[index] == ';':
            PrintCurrentTokenInfo()
            index += 1
        else:
            SayErrorAndDie('Expected separator ";"')
        

def OptDeclarationList():
    if TOKENS[index].lexeme in  ['{', '@@']:
        PrintParseInfo('<Opt Declaration List>', '<Empty>')
        Empty()
    else:
        PrintParseInfo('<Opt Declaration List>', '<Declaration List>')
        DeclarationList()
    
def StatementList():
    multiple_statements = False
    num_semicolons = 0
    for token in TOKENS[index:]:
        if token == ';':
            num_semicolons += 1
        elif token == '}':
            break
        if num_semicolons > 1:
            multiple_statements = True
            break
    if multiple_statements:
        PrintParseInfo('<Statement List>', '<Statement> <Statement List>')
        Statement()
        PrintCurrentTokenInfo()
        StatementList()
    else:
        PrintParseInfo('<Statement List>', '<Statement>')
        Statement()

def Read():
    global index
    PrintParseInfo('<Read>', 'read ( <IDs> );')
    index += 1
    if TOKENS[index] == '(':
        PrintCurrentTokenInfo()
        index += 1
        PrintCurrentTokenInfo()
        IDs()
        index += 1
        if TOKENS[index] == ')':
            PrintCurrentTokenInfo()
            index += 1
        else:
            SayErrorAndDie('Expected separator ")"')

        if TOKENS[index] == ';':
            PrintCurrentTokenInfo()
            index += 1
        else:
            SayErrorAndDie('Expected separator ";"')
    else:
        SayErrorAndDie('Expected separator "("')

def Expression():
    PrintParseInfo('<Expression>', '<Term> <Expression Prime>')
    Term()
    ExpressionPrime()

def ExpressionPrime():
    global index
    if TOKENS[index] == '+':
        PrintParseInfo('<Expression Prime>', '+ <Term> <Expression Prime>')
        index += 1
        PrintCurrentTokenInfo()
        Term()
        ExpressionPrime()
    elif TOKENS[index] == '-':
        PrintParseInfo('<Expression Prime>', '- <Term> <Expression Prime>')
        index += 1
        PrintCurrentTokenInfo()
        Term()
        ExpressionPrime()
    else:
        PrintParseInfo('<Expression Prime>', 'epsilon')


def Term():
    PrintParseInfo('<Term>', '<Factor> <Term Prime>')
    Factor()
    TermPrime()

def TermPrime():
    global index
    PrintCurrentTokenInfo()
    if TOKENS[index] == '*':
        PrintParseInfo('<Term Prime>', '* <Factor> <Term Prime>')
        index += 1
        PrintCurrentTokenInfo()
        Factor()
        TermPrime()
    elif TOKENS[index] == '/':
        PrintParseInfo('<Term Prime>', '/ <Factor> <Term Prime>')
        index += 1
        PrintCurrentTokenInfo()
        Factor()
        TermPrime()
    else:
        PrintParseInfo('<Term Prime>', 'epsilon')

def Factor():
    global index
    if TOKENS[index].token_type == 'Identifier':
        if TOKENS[index+1] == '[':
            PrintParseInfo('<Factor>', '<Identifier> [ <IDs> ]')
            index += 1
            if TOKENS[index] == '[':
                PrintCurrentTokenInfo()
                index += 1
                PrintCurrentTokenInfo()
                IDs()
                index += 1
            if TOKENS[index] == ']':
                PrintCurrentTokenInfo()
                index += 1
            else:
                SayErrorAndDie('Expected Separator "]"')
        else:
            PrintParseInfo('<Factor>', '<Identifier>')
            index += 1
    elif TOKENS[index].token_type == 'Integer':
        PrintParseInfo('<Factor>', '<Integer>')
        index += 1
    elif TOKENS[index].token_type == 'Real':
        PrintParseInfo('<Factor>', '<Real>')
        index += 1
    elif TOKENS[index] == 'true':
        PrintParseInfo('<Factor>', 'true')
        index += 1
    elif TOKENS[index] == 'false':
        PrintParseInfo('<Factor>', 'false')
        index += 1
    elif TOKENS[index] == '(':
        PrintParseInfo('<Factor>', '( <Expression> )')
        index += 1
        PrintCurrentTokenInfo()
        Expression()
        if TOKENS[index] == ')':
            index += 1
        else:
            SayErrorAndDie('Expected separator ")"')
        
def Write():
    global index
    PrintParseInfo('<Write>', 'write ( <Expression> );')
    index += 1
    if TOKENS[index] == '(':
        PrintCurrentTokenInfo()
        index += 1
        PrintCurrentTokenInfo()
        Expression()
        if TOKENS[index] == ')':
            index += 1
        else:
            SayErrorAndDie('Expected separator ")"')

        if TOKENS[index] == ';':
            PrintCurrentTokenInfo()
            index += 1
        else:
            SayErrorAndDie('Expected separator ";"')

    else:
        SayErrorAndDie('Expected separator "("')

def Compound():
    global index
    PrintParseInfo('<Compound>', '{ <Statement List> }')
    if TOKENS[index] == '{':
        index += 1
        PrintCurrentTokenInfo()
        StatementList()
    else:
        SayErrorAndDie('Expected separator "{"')
    if TOKENS[index] == '}':
        PrintCurrentTokenInfo()
        index +=1
    else:
        SayErrorAndDie('Expected separator "}"')

def Relop():
    global index
    if TOKENS[index] == '=':
        PrintParseInfo('<Relop>', '=')
    elif TOKENS[index] == '!=':
        PrintParseInfo('<Relop>', '!=')
    elif TOKENS[index] == '>':
        PrintParseInfo('<Relop>', '>')
    elif TOKENS[index] == '<':
        PrintParseInfo('<Relop>', '<')
    elif TOKENS[index] == '=>':
        PrintParseInfo('<Relop>', '=>')
    elif TOKENS[index] == '<=':
        PrintParseInfo('<Relop>', '<=')
    else:
        SayErrorAndDie('Expected <Relop>')
    index += 1
        
def Condition():
    global index
    PrintParseInfo('<Condition>', '<Expression>  <Relop>   <Expression>')
    PrintCurrentTokenInfo()
    Expression()
    if TOKENS[index].token_type == 'Relop':
        Relop()
        Expression()
    else:
        SayErrorAndDie('Expected <Relop>')
        
def If():
    pdb.set_trace()
    global index
    else_found = False
    for token in TOKENS[index+2:]:
        if token == 'else':
            else_found = True
            break
        if token == 'endif':
            break
        if token == 'if':
            break
    if else_found:
        PrintParseInfo('<If>', 'if  ( <Condition>  ) <Statement> else <Statment> endif')
    else:
        PrintParseInfo('<If>', 'if  ( <Condition>  ) <Statement> endif')
    index += 1

    if TOKENS[index] == '(':
        PrintCurrentTokenInfo()
        index += 1
        Condition()
    else:
        SayErrorAndDie('Expected Separator "("')

    if TOKENS[index] == ')':
        index += 1
        PrintCurrentTokenInfo()
        Statement()
    else:
        SayErrorAndDie('Expected separtor ")"')

    if else_found:
        if TOKENS[index] == 'else':
            PrintCurrentTokenInfo()
            index += 1
            PrintCurrentTokenInfo()
            Statement()
        
    if TOKENS[index] == 'endif':
        PrintCurrentTokenInfo()
        index += 1
    else:
        SayErrorAndDie('Expected keyword "endif"')


def Return():
    global index
    PrintCurrentTokenInfo()
    if TOKENS[index] == 'return':
        if TOKENS[index+1] == ';':
            PrintParseInfo('<Return>', 'return;')
            index += 1
            PrintCurrentTokenInfo()
            index += 1
        else:
            PrintParseInfo('<Return>', 'return <Expression>;')
            index += 1
            PrintCurrentTokenInfo()
            Expression()
            if TOKENS[index] == ';':
                index += 1
    else:
        SayErrorAndDie('Expected "return"')

def While():
    global index
    PrintCurrentTokenInfo()
    if TOKENS[index] == 'while':
        index += 1
        if TOKENS[index] == '(':
            PrintCurrentTokenInfo()
            index += 1
            PrintCurrentTokenInfo()
            Condition()
            if TOKENS[index] == ')':
                index += 1
                PrintCurrentTokenInfo()
                Statement()
                PrintCurrentTokenInfo()
            else:
                SayErrorAndDie('Expected separtor ")"')
        else:
            SayErrorAndDie('Expected separator "("')
        
def Statement():
    global index
    if TOKENS[index] == '{':
        PrintParseInfo('<Statement>', '<Compound>')
        Compound()
    elif TOKENS[index] == 'if':
        PrintParseInfo('<Statement>', '<If>')
        If()
    elif TOKENS[index] == 'return':
        PrintParseInfo('<Statement>', '<Return>')
        Return()
    elif TOKENS[index] == 'write':
        PrintParseInfo('<Statement>', '<Write>')
        Write()
    elif TOKENS[index] == 'read':
        PrintParseInfo('<Statement>', '<Read>')
        Read()
    elif TOKENS[index] == 'while':
        PrintParseInfo('<Statement>', '<While>')
        While()
    elif TOKENS[index+1] == ':=':
        PrintParseInfo('<Statement>', '<Assignment>')
        Assignment()
    else:
        SayErrorAndDie('Expected one of the following symbols "{", "if", "return", "write", "read", or "while"')

def Assignment():
    global index
    PrintParseInfo('<Assignment>', '<Identifier> := <Expression>;');
    index += 1

    if TOKENS[index] == ':=':
        PrintCurrentTokenInfo()
        index += 1
    else:
        SayErrorAndDie('Expected operator ":="')
    PrintCurrentTokenInfo()
    Expression()

    if TOKENS[index] == ';':
        PrintCurrentTokenInfo()
        index += 1
    else:
        SayErrorAndDie('Expected ";"')
        
def Body(special=False):
    global index
    if not special:
        if TOKENS[index] == '{':
            PrintParseInfo('<Body>', '{ <Statement List> }')
            index += 1
            PrintCurrentTokenInfo()
            StatementList()
            if TOKENS[index] != '}':
                Body(True)
        else:
            SayErrorAndDie('Expected separator "{"')
    else:
        PrintCurrentTokenInfo()
        StatementList()
        if TOKENS[index] != '}':
            Body(True)

    if TOKENS[index] == '}':
        index += 1
        PrintCurrentTokenInfo()
                    
def Function():
    global index
    if TOKENS[index] == 'function':
        PrintParseInfo('<Function>', 'function <Identifier> [ <Opt Parameter List ] <Opt Declaration List> <Body>')
        index += 1
        if TOKENS[index].token_type == 'Identifier':
            PrintCurrentTokenInfo()
            index += 1
        else:
            SayErrorAndDie('Expected identifier')

        if TOKENS[index] == '[':
            PrintCurrentTokenInfo()
            index += 1
        else:
            SayErrorAndDie('Expected separator "["')

        PrintCurrentTokenInfo()
        if TOKENS[index] == ']':
            index += 1
            OptParameterList()
        else:
            OptParameterList()
            if TOKENS[index] == ']':
                PrintCurrentTokenInfo()
                index += 1
            else:
                SayErrorAndDie('Expected separator "]"')

        PrintCurrentTokenInfo()
        if TOKENS[index] == '{':
            OptDeclarationList()
            Body()
        else:
            OptDeclarationList()
            PrintCurrentTokenInfo()
            Body()
                
    
def FunctionDefinitions():
    multiple_functions = False
    for token in TOKENS[index+1:]:
        if token == '@@':
            break
        elif token == 'function':
            multiple_functions = True
            break

    if multiple_functions:
        PrintParseInfo('<Function Definitions>', '<Function> <Function Definitions>')
        Function()
        FunctionDefinitions()
    else:
        PrintParseInfo('<Function Definitions>', '<Function>')
        Function()
    
def OptFunctionDefinitions():
    if TOKENS[index] == '@@':
        PrintParseInfo('<Opt Function Definitions>', '<Empty>')
        Empty()
    elif TOKENS[index] == 'function':
        PrintParseInfo('<Opt Function Definitions>', '<Function Definitions>')
        FunctionDefinitions()
    else:
        SayErrorAndDie('Expecting "@@" or "function".')
    
def Rat15S():
    global index
    PrintCurrentTokenInfo()
    OptFunctionDefinitions()
    if TOKENS[index] == '@@':
        index += 1
        if TOKENS[index] == '@@':
            PrintCurrentTokenInfo()
            OptDeclarationList()
            index += 1
            PrintCurrentTokenInfo()
            StatementList()
        else:
            PrintCurrentTokenInfo()
            OptDeclarationList()
            if TOKENS[index] == '@@':
                PrintCurrentTokenInfo()
                index += 1
                PrintCurrentTokenInfo()
                StatementList()
            else:
                SayErrorAndDie('Expected separator "@@"')
        while index is not len(TOKENS):
            StatementList()
    else:
        SayErrorAndDie('Expected separator "@@"')


def Parameter():
    global index
    PrintParseInfo('<Parameter>', '<IDs> : <Qualifier>')
    IDs()
    index += 1
    if TOKENS[index] == ':':
        PrintCurrentTokenInfo()
        index +=1
        Qualifier()
    else:
        SayErrorAndDie('Expected separator ":"')
    
def ParameterList():
    global index
    num_colons = 0
    multiple_parameters = False
    for token in TOKENS[index:]:
        if token == ':':
            num_colons += 1
        if token == ']':
            break
        if num_colons > 1:
            multiple_parameters = True
            break
                

    if multiple_parameters:
        PrintParseInfo('<Parameter List>', '<Parameter>, <Parameter List>')
        Parameter()
        if TOKENS[index] == ',':
            PrintCurrentTokenInfo()
            index += 1
            ParameterList()
        else:
            SayErrorAndDie('Expected separator ","')
    else:
        PrintParseInfo('<Parameter List>', '<Parameter>')
        Parameter()
                
def OptParameterList():
    if TOKENS[index-1] == ']':
        PrintParseInfo('<Opt Parameter List>', '<Empty>')
        Empty()
    else:
        PrintParseInfo('<Opt Parameter List>', '<Parameter List>')
        ParameterList()
