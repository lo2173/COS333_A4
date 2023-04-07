#-----------------------------------------------------------------------
# Author: Lois Omotara
# runserver.py
#-----------------------------------------------------------------------
import sys
import argparse
import reg
def main():
    try:
        parser= argparse.ArgumentParser(prog='runserver.py',
            usage='runserver.py[-h] port',
            description='The registrar application')
        parser.add_argument('port',
            help='the port at which the server should listen',
            type=int)
        args = parser.parse_args()
        port = args.port
    except Exception as ex:
        print(ex,file=sys.stderr)
        sys.exit(2)
    try:
        reg.app.run(host='0.0.0.0', port=port)
    except Exception as ex:
        print(ex,file=sys.stderr)
        sys.exit(1)
if __name__ == '__main__':
    main()
