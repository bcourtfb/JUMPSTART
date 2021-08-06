#!/usr/bin/env python3

(WORK IN PROGRESS)

import os
import sys
import time
import colorama
from colorama import Fore, Back, Style
colorama.init(autoreset=True)

################################################################
# colored text and background

# print(Fore.RED + 'some red text')
# print(Back.GREEN + 'and with a green background')
# print(Style.DIM + 'and in dim text')
# print(Style.BRIGHT + "BRIGHT")
# print(Style.RESET_ALL)
# print('back to normal now')

################################################################
os.system("clear")
print(Fore.CYAN + r"""
    
     _ _   _ __  __ ____    ____ _____  _    ____ _____ 
    | | | | |  \/  |  _ \  / ___|_   _|/ \  |  _ \_   _|
 _  | | | | | |\/| | |_) | \___ \ | | / _ \ | |_) || |  
| |_| | |_| | |  | |  __/   ___) || |/ ___ \|  _ < | |  
 \___/ \___/|_|  |_|_|     |____/ |_/_/   \_\_| \_\|_|
    
    """)



################################################################
#Variables

ffox = ["[Desktop Entry]", "Name=Firefox", "Comment=Web Browser", "Exec=/opt/firefox/firefox %u", "Terminal=false", "Type=Application", "Icon=/opt/firefox/browser/chrome/icons/default/default128.png", "Categories=Network;WebBrowser;", "MimeType=text/html;text/xml;application/xhtml+xml;application/xml;application/vnd.mozilla.xul+xml;application/rss+xml;application/rdf+xml;image/gif;image/jpeg;image/png;x-scheme-handler/http;x-scheme-handler/https;", "StartupNotify=true"]
Programs_to_Install = ["terminator", "plank", "anonsurf", "cheat.sh", "gufw", "payload all things", "airgeddon", "python3-pip", "vlc", "filezilla", "qbittorrent", "htop", "postgresql-update & run at startup", "apt-transport-https", "Change default ssh keys", "make python3 default"]
SRC1=("deb https://http.kali.org/kali kali-rolling main non-free contrib", "deb-src https://http.kali.org/kali kali-rolling main non-free contrib")

################################################################
#Ensure the script is being ran as root

if not os.geteuid()==0:
    sys.exit(print(Fore.RED +'This script must be run as root!'))
    
################################################################
# Main Menu user selection

def menu():
    time.sleep(1)
    print("\n")
    print(Fore.GREEN + "[1] Update & Upgrade system\n")
    print(Fore.GREEN + "[2] Install Programs\n")
    print(Fore.GREEN + "[3] Replace Firefox ESR with Regular Firefox\n")
    print(Fore.GREEN + "[4] Install VScode\n")
    print(Fore.GREEN + "[0] Exit Program\n")
      
menu()
option = int(input(Fore.GREEN + "Enter your option: "))
print("\n")

################################################################
# Menu functions to be called

def option_1():
    time.sleep(1)
    os.system("apt-get update & apt-get full-upgrade -y && apt-get autoremove && sudo apt-get autoclean && sudo updatedb")
    print("\n")
    input(Fore.YELLOW + "Press Enter to continue...") 
    
    
def option_2():
    time.sleep(1)
    for items in Programs_to_Install:
        print(Fore.GREEN + "The following programs will be installed: ", end="")
        print(Fore.MAGENTA + items)
    print("\n")
    print(Fore.GREEN + "Please be patient")
    time.sleep(2)
    print("\n")
    os.system("sudo apt-get install terminator -y")
    print("\n")
    os.system("apt-get install plank -y")
    print("\n")
    os.system("wget -qO - https://download.sublimetext.com/sublimehq-pub.gpg | sudo apt-key add -")
    os.system("echo 'deb https://download.sublimetext.com/ apt/stable/' | sudo tee /etc/apt/sources.list.d/sublime-text.list && apt-get update & apt-get install sublime-text")
    print("\n")
    os.system("git clone https://github.com/Und3rf10w/kali-anonsurf.git && ~/kali-anonsurf/installer.sh")
    print("\n")
    os.system("curl https://cht.sh/:cht.sh | tee /usr/local/bin/cht.sh && chmod +x /usr/local/bin/cht.sh && apt-get install rlwrap -y")
    print("\n")
    os.system("apt-get install gufw -y")
    print("\n")
    os.system("git clone https://github.com/swisskyrepo/PayloadsAllTheThings.git")
    print("\n")
    os.system("apt-get install airgeddon -y")
    print("\n")
    os.system("apt-get install python3-pip -y")
    print("\n")
    os.system("apt-get install vlc -y")
    print("\n")
    os.system("apt-get install filezilla -y")
    print("\n")
    os.system("apt-get install qbittorrent -y")
    print("\n")
    os.system("apt-get install htop -y")
    print("\n")
    os.system("sudo sh -c 'echo 'deb http://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main' > /etc/apt/sources.list.d/pgdg.list'")
    os.system("wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -")
    os.system("apt-get -y install postgresql")
    os.system("update-rc.d postgresql enable")
    print("\n")
    os.system("dpkg-reconfigure openssh-server")
    print("\n")
    os.system("update-alternatives --install /usr/bin/python python /usr/bin/python2.7 1 && update-alternatives --install /usr/bin/python python /usr/bin/python3.9 2")
    print("\n")
    print(Fore.GREEN + "Program Installation Complete")
    time.sleep(2)
    print("\n")
    input(Fore.YELLOW + "Press Enter to continue...")
    
        
    
def option_3():
    time.sleep(1)
    os.system("apt-get --purge autoremove firefox-esr -y && wget -O FirefoxSetup.tar.bz2 'https://download.mozilla.org/?product=firefox-latest&os=linux64'")
    os.system("tar -xvf FirefoxSetup.tar.bz2 && rm FirefoxSetup*")
    os.system("sudo mv firefox /opt")
    os.system("touch firefox.txt")
    with open("firefox.txt", "w+") as f:
        for items in ffox:
            f.write('%s\n' %items)
    f.close() 
    os.rename("firefox.txt", "firefox.desktop")
    os.system("mv firefox.desktop /usr/share/applications")
    os.system("ln -s /opt/firefox/firefox /usr/local/bin/firefox")
    print("\n")
    print(Fore.GREEN + "Firefox Installation Complete")
    time.sleep(2)
    print("\n") 
    input(Fore.YELLOW + "Press Enter to continue...")
    
def option_4():
    time.sleep(1)
    os.system("wget https://az764295.vo.msecnd.net/stable/3c4e3df9e89829dce27b7b5c24508306b151f30d/code_1.55.2-1618307277_amd64.deb")
    os.system("apt install ./code*.deb")
    os.system("rm code*")
    print("\n")
    print(Fore.GREEN + "VScode Installation Complete")
    
################################################################
# Menu Options
    
while option != 0:
    if option == 1:
        os.system("clear")
        print(Fore.GREEN + "Executing Option 1\n")
        option_1()
    elif option == 2:
        os.system("clear")
        print(Fore.GREEN + "Executing Option 2\n")
        option_2()
    elif option == 3:
        os.system("clear")
        print(Fore.GREEN + "Executing Option 3\n")
        option_3()
    elif option == 4:
        os.system("clear")
        print(Fore.GREEN + "Executing Option 4\n")
        option_4()
    else:
        print(Fore.RED + "Invalid Option\n")
        
            
    menu()
    option = int(input(Fore.GREEN + "Enter your option: "))
    print("\n")

os.system("clear")
print(Fore.YELLOW + "Thank you for using this program. Good bye!")
time.sleep(1)

################################################################




