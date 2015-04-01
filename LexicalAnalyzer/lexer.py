import sys

def main():
    if len(sys.argv[1:]) is 2:
        Lexer(sys.argv[1], sys.argv[2])
    else:
        Lexer(sys.argv[1])

if __name__ == '__main__':
    sys.path.append('../Lib')
    from lexicalanalyzer import Lexer
    main()
