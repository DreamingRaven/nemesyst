# @Author: George Onoufriou <georgeraven>
# @Date:   2018-05-22
# @Filename: log.py
# @Last modified by:   georgeraven
# @Last modified time: 2018-05-22
# @License: Please see LICENSE file in project root



class Log(object):

    import os, sys
    from colorama import Fore, Back, Style, init

    className = "Log"
    prePend = "[ " + os.path.basename(sys.argv[0]) + " -> " + className + "] "
    prePend_parent = "[ " + os.path.basename(sys.argv[0]) + " ]"
    init(autoreset=True) # forces colorama to auto reset colors

    def __init__(self, logLevel=-1):
        self.logLevel = logLevel

    def print(self, text, minLogLevel=3, colour=None):
        if(minLogLevel==-1):
            print(text) # this allows for universal formating as no prePending
        elif(minLogLevel==0) and (self.logLevel >= minLogLevel):
            print(self.Fore.GREEN + self.prePend_parent + " [ info ] " + str(text))
        elif(minLogLevel==1) and (self.logLevel >= minLogLevel):
            print(self.Fore.YELLOW + self.prePend_parent + " [ warn ] " + str(text))
        elif(minLogLevel==2) and (self.logLevel >= minLogLevel):
            print(self.Fore.RED + self.prePend_parent + " [ error ] " + str(text))
        elif(minLogLevel==3) and (self.logLevel >= minLogLevel):
            print(self.Fore.MAGENTA +self.prePend_parent + " [ debug ] " + str(text))
        #TODO implement level specific formating

if __name__ == "__main__":
    log = Log()
