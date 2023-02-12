#!/usr/bin/python2.7
import os
from commands import *
import platform
if not (platform.system() in ('Windows', 'Microsoft')):
    import readline
    readline.parse_and_bind("tab: complete")

def main():
    print "******************************************************"
    print "*              WELCOME TO JQ-REPL                    *"
    print "*           Type :help for help Menu                 *"
    print "******************************************************\n"
    #PrintHelp()
    init()
    prompt = ""
    while (1):
        try:
            if sys.stdin.isatty():
                prompt = "jq>>"
            GetInput(raw_input(prompt).strip())
        except EOFError, e:
            sys.stdin.flush()
            sys.stdin = open("/dev/tty")
        except KeyboardInterrupt:
            print "\nKeyboardInterrupt"
            pass
        except Exception,e:
            print "\nError: ",str(e)
            pass

if __name__ == "__main__":
    main()
