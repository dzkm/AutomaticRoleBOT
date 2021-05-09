import asyncio
from colorama import init, Fore, Back, Style
from datetime import datetime as dt
""" 
This function makes colorful printing with time
0 = SUCCESS
1 = INFORMATION
2 = WARNING
3 =  ERROR
4 = CRITICAL ERROR
5 = DEBUG INFO
 """

async def log(textInput,logType):
    init()
    if logType == 0:
        print("{0}{1}{2}({3})[SUCCESS]{4}{5}".format(Fore.GREEN,Back.RESET,Style.NORMAL,dt.now(), textInput, Style.RESET_ALL))
    elif logType == 1:
        print("{0}{1}{2}({3})[INFO]{4}{5}".format(Fore.WHITE,Back.RESET,Style.NORMAL,dt.now(), textInput, Style.RESET_ALL))
    elif logType == 2:
        print("{0}{1}{2}({3})[WARNING]{4}{5}".format(Fore.YELLOW,Back.RED,Style.NORMAL,dt.now(), textInput, Style.RESET_ALL))
    elif logType == 3:
        print("{0}{1}{2}({3})[ERROR]{4}{5}".format(Fore.RED,Back.RESET,Style.NORMAL,dt.now(), textInput, Style.RESET_ALL))
    elif logType == 4:
        print("{0}{1}{2}({3})[CRITICAL ERROR]{4}{5}".format(Fore.BLACK,Back.RED,Style.BRIGHT,dt.now(), textInput, Style.RESET_ALL))
    elif logType == 5:
        print("{0}{1}{2}({3})[DEBUG INFO]{4}{5}".format(Fore.CYAN,Back.RESET,Style.NORMAL,dt.now(), textInput, Style.RESET_ALL))
if __name__ == "__main__":
    asyncio.run(log("Don't run this directly. This is a library", 4))
