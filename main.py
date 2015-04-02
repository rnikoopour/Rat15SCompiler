'''
@mainpage Rat15S Compiler

@section intro_sec Introduction
This will become a Rat15S compiler.  Currently working on Lexical Analyzer.
@author Reza Nikoopour
@author Eric Roe
'''
def main():
    tokens = Lexer()
    
if __name__ == '__main__':
    sys.path.append('Lib')
    from lexicalanalyzer import Lexer
    main(sys.argv[1], sys.argv[2])
