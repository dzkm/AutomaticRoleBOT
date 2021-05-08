from colorama import init, Fore, Back, Style
from datetime import datetime as dt
""" 
This function makes colorful printing with time
0 = SUCCESS
1 = INFORMATION
2 = WARNING
3 =  ERROR
4 = CRITICAL ERROR
 """
def log(textInput,logType):
    init()
    if logType == 0:
        print(Fore.GREEN + "(%s)[SUCCESS] " % dt.now() + textInput + Style.RESET_ALL)
    elif logType == 1:
        print(Fore.WHITE + "(%s)[INFO] " % dt.now() + textInput + Style.RESET_ALL)
    elif logType == 2:
        print(Fore.YELLOW + Back.RED + "(%s)[WARNING] " % dt.now() + textInput + Style.RESET_ALL)
    elif logType == 3:
        print(Fore.RED + "(%s)[ERROR] " % dt.now() + textInput + Style.RESET_ALL)
    elif logType == 4:
        print(Fore.BLACK + Back.RED + "(%s)[CRITICAL ERROR] " % dt.now()+ textInput + Style.RESET_ALL)

if __name__ == "__main__":
    print("Don't run this directly. This is a library")
