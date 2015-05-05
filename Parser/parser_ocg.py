import sys
sys.path.append('../Lib')
from rdp_ocg import Parser

def main(file=None):
    if file is None:
        if len(sys.argv[1:]) is 2:
            Parser(sys.argv[1], sys.argv[2])
        else:
            Parser(sys.argv[1])
    else:
            Parser(file)
if __name__ == '__main__':
    sys.path.append('../Lib')
    from rdp_ocg import Parser    
    main()
