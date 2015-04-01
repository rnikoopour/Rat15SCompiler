import sys

def main():
    if len(sys.argv[1:]) is 2:
        Parser(sys.argv[1], sys.argv[2])
    else:
        Parser(sys.argv[1])

if __name__ == '__main__':
    sys.path.append('../Lib')
    from recursive_decent_parser import Parser
    main()
