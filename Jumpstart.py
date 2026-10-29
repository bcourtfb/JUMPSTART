#!/usr/bin/env python3
"""JumpStart - post-install setup helper for Kali Linux. (WORK IN PROGRESS)"""

import os
import subprocess
import sys

try:
    import colorama
    from colorama import Fore
except ImportError:
    sys.exit("colorama is required: apt-get install python3-colorama")

colorama.init(autoreset=True)

################################################################
# Settings

KEYRING_DIR = "/etc/apt/keyrings"
TOOLS_DIR = "/opt"

# Packages available straight from the Kali repos
APT_PACKAGES = [
    "terminator", "plank", "gufw", "airgeddon", "python3-pip", "vlc",
    "filezilla", "qbittorrent", "htop", "rlwrap", "git", "wget", "gnupg",
]

BANNER = r"""
     _ _   _ __  __ ____    ____ _____  _    ____ _____
    | | | | |  \/  |  _ \  / ___|_   _|/ \  |  _ \_   _|
 _  | | | | | |\/| | |_) | \___ \ | | / _ \ | |_) || |
| |_| | |_| | |  | |  __/   ___) || |/ ___ \|  _ < | |
 \___/ \___/|_|  |_|_|     |____/ |_/_/   \_\_| \_\|_|
"""

################################################################
# Helpers


def clear_screen():
    os.system("clear")


def pause():
    input(Fore.YELLOW + "\nPress Enter to continue...")


def run(cmd):
    """Run a shell command, echo it first, and return True if it succeeded."""
    print(Fore.BLUE + f"$ {cmd}")
    result = subprocess.run(cmd, shell=True)
    if result.returncode != 0:
        print(Fore.RED + f"[!] Failed (exit {result.returncode}): {cmd}")
        return False
    return True


def run_all(*cmds):
    """Run commands in order, stopping at the first one that fails."""
    return all(run(cmd) for cmd in cmds)


def apt_install(*packages):
    return run("apt-get install -y " + " ".join(packages))


def add_apt_repo(name, key_url, repo, arch=None):
    """Add a third-party APT repo with its own keyring (apt-key is deprecated)."""
    os.makedirs(KEYRING_DIR, exist_ok=True)
    keyring = f"{KEYRING_DIR}/{name}.gpg"
    if not run(f"wget -qO- {key_url} | gpg --dearmor --yes -o {keyring}"):
        return False
    options = f"signed-by={keyring}" + (f" arch={arch}" if arch else "")
    with open(f"/etc/apt/sources.list.d/{name}.list", "w") as f:
        f.write(f"deb [{options}] {repo}\n")
    return run("apt-get update")


def git_clone(url, dest):
    """Clone a repo, or pull the latest changes if it is already there."""
    if os.path.isdir(os.path.join(dest, ".git")):
        return run(f"git -C {dest} pull")
    return run(f"git clone {url} {dest}")


################################################################
# Install steps


def install_sublime():
    return (add_apt_repo("sublime-text",
                         "https://download.sublimetext.com/sublimehq-pub.gpg",
                         "https://download.sublimetext.com/ apt/stable/")
            and apt_install("sublime-text"))


def install_anonsurf():
    dest = f"{TOOLS_DIR}/kali-anonsurf"
    return (git_clone("https://github.com/Und3rf10w/kali-anonsurf.git", dest)
            and run(f"cd {dest} && ./installer.sh"))


def install_cheat_sh():
    return run_all("curl -fsSL https://cht.sh/:cht.sh -o /usr/local/bin/cht.sh",
                   "chmod +x /usr/local/bin/cht.sh")


def install_payloads():
    return git_clone("https://github.com/swisskyrepo/PayloadsAllTheThings.git",
                     f"{TOOLS_DIR}/PayloadsAllTheThings")


def install_postgresql():
    # Kali ships PostgreSQL; the upstream pgdg repo has no "kali-rolling" suite
    return apt_install("postgresql") and run("systemctl enable --now postgresql")


def regenerate_ssh_keys():
    # Kali images ship identical host keys, so remove them before regenerating
    return run_all("rm -f /etc/ssh/ssh_host_*",
                   "dpkg-reconfigure openssh-server")


def make_python3_default():
    return apt_install("python-is-python3")


INSTALL_STEPS = [
    ("Kali packages: " + ", ".join(APT_PACKAGES), lambda: apt_install(*APT_PACKAGES)),
    ("Sublime Text", install_sublime),
    ("AnonSurf", install_anonsurf),
    ("cheat.sh", install_cheat_sh),
    ("PayloadsAllTheThings", install_payloads),
    ("PostgreSQL (enabled at startup)", install_postgresql),
    ("Regenerate default SSH host keys", regenerate_ssh_keys),
    ("Make python3 the default python", make_python3_default),
]

################################################################
# Menu actions


def update_system():
    run_all("apt-get update",
            "apt-get full-upgrade -y",
            "apt-get autoremove -y",
            "apt-get autoclean",
            "updatedb")
    pause()


def install_programs():
    print(Fore.GREEN + "The following will be installed:")
    for label, _ in INSTALL_STEPS:
        print(Fore.MAGENTA + f"  - {label}")
    print(Fore.GREEN + "\nPlease be patient\n")

    if not run("apt-get update"):
        pause()
        return

    failed = []
    for label, step in INSTALL_STEPS:
        print(Fore.CYAN + f"\n==> {label}")
        if not step():
            failed.append(label)

    if failed:
        print(Fore.RED + "\nThese steps failed:")
        for label in failed:
            print(Fore.RED + f"  - {label}")
    else:
        print(Fore.GREEN + "\nProgram Installation Complete")
    pause()


def install_firefox():
    # Mozilla's APT repo keeps Firefox updated through apt, unlike a tarball in /opt
    ok = add_apt_repo("mozilla",
                      "https://packages.mozilla.org/apt/repo-signing-key.gpg",
                      "https://packages.mozilla.org/apt mozilla main")
    if ok:
        with open("/etc/apt/preferences.d/mozilla", "w") as f:
            f.write("Package: *\nPin: origin packages.mozilla.org\nPin-Priority: 1000\n")
        # Install the new browser before removing the old one
        ok = apt_install("firefox") and run("apt-get purge -y firefox-esr")
    print(Fore.GREEN + "\nFirefox Installation Complete" if ok
          else Fore.RED + "\nFirefox Installation Failed")
    pause()


def install_vscode():
    ok = (add_apt_repo("vscode",
                       "https://packages.microsoft.com/keys/microsoft.asc",
                       "https://packages.microsoft.com/repos/code stable main",
                       arch="amd64")
          and apt_install("code"))
    print(Fore.GREEN + "\nVScode Installation Complete" if ok
          else Fore.RED + "\nVScode Installation Failed")
    pause()


MENU = {
    "1": ("Update & Upgrade system", update_system),
    "2": ("Install Programs", install_programs),
    "3": ("Replace Firefox ESR with Regular Firefox", install_firefox),
    "4": ("Install VScode", install_vscode),
}

################################################################
# Main loop


def main():
    if not sys.platform.startswith("linux"):
        sys.exit(Fore.RED + "This script only runs on Kali/Debian Linux.")
    if os.geteuid() != 0:
        sys.exit(Fore.RED + "This script must be run as root!")

    while True:
        clear_screen()
        print(Fore.CYAN + BANNER)
        for key, (label, _) in MENU.items():
            print(Fore.GREEN + f"[{key}] {label}\n")
        print(Fore.GREEN + "[0] Exit Program\n")

        choice = input(Fore.GREEN + "Enter your option: ").strip()
        if choice == "0":
            break
        if choice not in MENU:
            print(Fore.RED + "Invalid Option")
            pause()
            continue

        label, action = MENU[choice]
        clear_screen()
        print(Fore.GREEN + f"Executing: {label}\n")
        action()

    clear_screen()
    print(Fore.YELLOW + "Thank you for using this program. Good bye!")


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print(Fore.YELLOW + "\nAborted.")
        sys.exit(130)
