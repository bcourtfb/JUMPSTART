
JumpStart
A menu-driven Python script that sets up a fresh Kali Linux install: it updates the system, installs a set of everyday and pentesting tools, swaps Firefox ESR for regular Firefox, and installs VS Code.

Status: work in progress. Try it on a VM or a snapshot before running it on a machine you care about.

Requirements
Kali Linux (or another Debian-based distro; some packages are Kali-only)

Python 3

Root privileges

An internet connection

colorama for colored output:

sudo apt install python3-colorama
Usage
sudo python3 JumpStart.py
Choose an option from the menu by typing its number. Enter 0 to exit, or press Ctrl+C at any time to abort.

Menu options
Option	What it does
1. Update & Upgrade system	Runs apt-get update, full-upgrade, autoremove and autoclean, then refreshes the locate database.
2. Install Programs	Installs the tools listed below, then reports any step that failed.
3. Replace Firefox ESR with Regular Firefox	Adds Mozilla's official APT repository, installs firefox, then removes firefox-esr.
4. Install VScode	Adds Microsoft's official APT repository and installs code.
What option 2 installs
Tool	Source
terminator, plank, gufw, airgeddon, python3-pip, vlc, filezilla, qbittorrent, htop, rlwrap	Kali repositories
Sublime Text	Official Sublime HQ APT repository
AnonSurf	Cloned to /opt/kali-anonsurf and installed
cheat.sh	/usr/local/bin/cht.sh
PayloadsAllTheThings	Cloned to /opt/PayloadsAllTheThings
PostgreSQL	Kali repositories, enabled to start at boot
python-is-python3	Makes python point to python3
Option 2 also deletes and regenerates the SSH host keys. Kali images ship with the same default keys, so new ones should be generated on every install. Clients that connected to this machine before will warn that the host key changed.

Notes
Third-party repositories are added with their own keyring in /etc/apt/keyrings (the deprecated apt-key is not used).
Running option 2 again is safe: repositories that are already cloned are updated with git pull.
Removing firefox-esr may also remove Kali metapackages that depend on it. Review what apt plans to remove before confirming.
Disclaimer
Some of the included tools (such as airgeddon and PayloadsAllTheThings) are meant for security testing. Only use them on systems and networks you own or have written permission to test.

