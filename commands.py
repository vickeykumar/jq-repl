#!/usr/bin/python env
import os,re,subprocess,sys
import platform

CLEAR = "cls"   #clear command on ur system
FOUND_JQ = not os.system("jq --version > /dev/null 2>&1")
if not (platform.system() in ('Windows', 'Microsoft')):
        import readline
        readline.parse_and_bind("tab: complete")
        CLEAR = 'clear'

jsonstring = ""
CommandHelpStr = {  
        ":h, :help" : "Print Help Menu.",
        ":q" : "Quit the session.",
        ":c" : "Clear the session,and Restart.",
        }
CommandArg = ''

def Clear(): 
    os.system(CLEAR)
    init()
    return

def Exit():
    sys.exit()
    return

Command2FuncMap = {
        ":h":       "PrintHelp",
        ":help":    "PrintHelp",
        ":c":       "Clear",
        ":q":       "Exit",
}

def has_option_flag(input_string):
    return bool(re.search(r'(?<!\w)-{1,2}[a-zA-Z]+(?!\w)', input_string))

openPar = ["[", "{"]
closePar = ["]", "}"]
# utility functions
def GetInput(inputstring = ''):
    global jsonstring
    if inputstring == '':
        return
    if inputstring.startswith("jq "):
        #command already present
        inputstring=inputstring.lstrip("jq ")
    for k,fun in Command2FuncMap.iteritems():
        if inputstring.startswith(k):
            inputstring = inputstring.split(" ",1)
            CommandArg = inputstring[1] if len(inputstring)>1 else ''
            if callable(globals()[fun]):
                err=globals()[fun]()
                if err!=None:
                    print err
            return
    if inputstring[0] in openPar or (inputstring[0] in openPar and inputstring[-1] in closePar) :
        old_json = jsonstring
        jsonstring = read_json_block(inputstring)
        #print "recieved: ", jsonstring
        err = runRepl()
        if err != '':
            jsonstring=old_json
            # not a valid input, fallback
            print err
        else:
            print "Input Json Loaded Successfully"
    elif inputstring != '':
        err = runRepl(inputstring)    #lets try compiling with jq
        if err != '':
            print err,

def init():
    global jsonstring
    #initialize again
    jsonstring =  ""
    return 

def is_valid_json(string):
    stack = []
    for char in string:
        if char in ('{', '['):
            stack.append(char)
        elif char in ('}', ']'):
            if not stack:
                return False
            if char == '}' and stack[-1] != '{':
                return False
            if char == ']' and stack[-1] != '[':
                return False
            stack.pop()
    return not stack

def read_json_block(line=''):
    try:
        while not is_valid_json(line):
            line = line + "\n\t" + raw_input().strip()
        return line.strip()
    except Exception,e:
        print "Error: ",str(e)
    return ""

def runRepl(filterstring = '.'):
    global jsonstring
    if not has_option_flag(filterstring):
        # cover in quotes for protection
        filterstring = "'"+filterstring+"'"
    cmd = "jq "+filterstring
    if jsonstring != "" :
        cmd = "echo '%s' | "%jsonstring + cmd
    out,err = subprocess.Popen(cmd, stderr=subprocess.PIPE, shell=True).communicate()
    return err

def PrintHelp():
    print "\n  COMMANDS:\n"
    width = max([len(word) for word in CommandHelpStr.keys()])
    for key,val in CommandHelpStr.iteritems():
        print "\t",key.ljust(width),"\t",val
    print "\n\nJq USAGE: "
    err = runRepl("jq --help")
    if err != '':
        print err,

