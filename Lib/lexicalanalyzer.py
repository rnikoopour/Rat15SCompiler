'''
@package lexicalanalyzer
This will break up source code into tokens
'''

import re
from dfsm import GetIdentifierDFSM, GetNumeralDFSM, GetOperatorSeparatorDFSM

def Lexer(input_file, output_file=None):
    """
    @brief Returns the tokens generated from the input file

    @return A list containing tokens
    """
    source_code = open(input_file, 'r')
    tokens = []
    char = source_code.read(1)
    end_of_file = True if char == '' else False
    line_number = 1
    while not end_of_file:
        # Choose DFSM based on what char is
        # Let IDDFSM handle anything that starts with '_'
        if char.isalpha() or char == '_':
            dfsm = GetIdentifierDFSM()
        # Let NumeralDFSM handle anything that starts with '.'
        elif char.isdigit() or char == '.':
            dfsm = GetNumeralDFSM()
        # The OperatorSeparatorDFSM handles everything else
        else:
            dfsm = GetOperatorSeparatorDFSM()

        # Start building lexeme
        lexeme = char
        # If Transition returns -1 its an epsilon transition
        #  we need to stop taking in characters and process the lexeme
        line_number_increment = 0
        while dfsm.Transition(char) is not -1:
            char = source_code.read(1)
            # Check to see if EOF is reached to set end_of_file properly
            #  This prevents us from losing the last letter of the file
            if char == '':
                end_of_file = True
            if char == '\n':
                line_number_increment += 1
            lexeme += char
                        
        if not end_of_file:
            # This "ungets" the last char.
            if len(lexeme) > 1:
                char = lexeme[-1]
                lexeme = lexeme[:-1]
            # If len(lexeme) is 1 we need to read the next char in the file
            #  We do this because if the len of lexeme is 1 we haven't read
            #  from the file to update char
            else:
                char = source_code.read(1)

        # We don't want to add comments to the token list
        token = dfsm.GetToken(lexeme)
        token.line_number = line_number
        if token.token_type is not 'Comment':
            tokens.append(token)
            
        # Strips any whitespace we encounter
        while re.match(r'[\s]', char):
            char = source_code.read(1)
            if char == '\n':
                line_number_increment += 1
                
        # Increment line_number after total number of increments have been calculated
        #  so that the last lexeme isn't a line number ahead of where it should be
        line_number += line_number_increment
        
        # We need to check if after stripping whitespaces we've reached EOF
        if char == '':
            end_of_file = True

    if output_file is not None:
        output_file = open(output_file, 'w')
        output_file.write('token -- lexeme -- line number\n')
        for token in tokens:
            output_file.write(token.token_type + ' -- ' + token.lexeme + ' -- ' + str(token.line_number) + '\n')
        output_file.close()

    return tokens

