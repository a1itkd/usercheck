#!/usr/bin/env python3

import os
import time
import subprocess
import pwd
from datetime import datetime
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

# Tool Icon
print(Fore.CYAN + Style.BRIGHT + """
========================================
        UserCheck by Ali Monam
  Linux User Security Audit Tool - PRO
========================================
""")


def check_users_without_password():
    print(Fore.YELLOW + "[+] Checking users without password...")
    users_without_pass = []

    with open("/etc/shadow", "r") as shadow_file:
        for line in shadow_file:
            parts = line.strip().split(":")
            if len(parts) > 1:
                username, password = parts[0], parts[1]
                if password == "" or password in ["*", "!", "!!"]:
                    users_without_pass.append(username)

    return users_without_pass

def check_locked_accounts():
    print(Fore.YELLOW + "[+] Checking for locked accounts...")
    locked_accounts = []

    with open("/etc/shadow", "r") as shadow_file:
        for line in shadow_file:
            parts = line.strip().split(":")
            if len(parts) > 1:
                username, password = parts[0], parts[1]
                if password.startswith("!") or password.startswith("!!"):
                    locked_accounts.append(username)

    return locked_accounts


def check_sudo_users():
    print(Fore.YELLOW + "[+] Checking users with sudo privileges...")
    sudo_users = []

    try:
        output = subprocess.check_output("getent group sudo", shell=True).decode()
        if ":" in output:
            parts = output.strip().split(":")
            if len(parts) > 3:
                members = parts[3].split(",")
                sudo_users = [user.strip() for user in members if user.strip()]
    except Exception as e:
        print(Fore.RED + f"[!] Error checking sudo users: {e}")

    return sudo_users

def check_inactive_users_by_home(days_threshold=90):
    print(Fore.YELLOW + f"[+] Checking for inactive users (by /home last access > {days_thre>
    inactive_users = []
    current_time = time.time()

    home_dir = "/home"
    if not os.path.exists(home_dir):
        print(Fore.RED + "[!] /home directory not found!")
        return inactive_users

    for user in os.listdir(home_dir):
        user_path = os.path.join(home_dir, user)
        if os.path.isdir(user_path):
            last_access = os.path.getatime(user_path)
            days_inactive = int((current_time - last_access) / 86400)
            if days_inactive > days_threshold:
                inactive_users.append((user, f"{days_inactive} days inactive"))

    return inactive_users


def check_shells():
    print(Fore.YELLOW + "[+] Checking user shells...")
    special_shells = {}

    for user in pwd.getpwall():
        if user.pw_uid >= 1000 and user.pw_name != "nobody":
            shell = user.pw_shell
            if shell in ["/usr/sbin/nologin", "/bin/false"]:
                special_shells[user.pw_name] = shell

    return special_shells


def write_report(data):
    now = datetime.now()
    timestamp = now.strftime("%Y-%m-%d_%H-%M-%S")
    report_name = f"logs/user_audit_{timestamp}.txt"

    os.makedirs("logs", exist_ok=True)

    report = f"UserSecureCheck Report - {now.strftime('%Y-%m-%d %H:%M:%S')}\n"
    report += "="*50 + "\n\n"

    if data["no_password"]:
        report += "[!] Users without password:\n"
        for user in data["no_password"]:
            report += f"    - {user}\n"
    else:
        report += "[+] All users have passwords set.\n"

    report += "\n"

    if data["locked_accounts"]:
        report += "[!] Locked user accounts:\n"
        for user in data["locked_accounts"]:
            report += f"    - {user}\n"
    else:
        report += "[+] No locked accounts found.\n"

    report += "\n"
if data["sudo_users"]:
        report += "[!] Users with sudo privileges:\n"
        for user in data["sudo_users"]:
            report += f"    - {user}\n"
    else:
        report += "[+] No sudo users found (besides root).\n"

    report += "\n"

    if data["inactive_users"]:
        report += f"[!] Inactive users (>{data['days_threshold']} days):\n"
        for user, status in data["inactive_users"]:
            report += f"    - {user}: {status}\n"
    else:
        report += "[+] No inactive users found.\n"

    report += "\n"

    if data["special_shells"]:
        report += "[!] Users with non-login shells:\n"
        for user, shell in data["special_shells"].items():
            report += f"    - {user}: {shell}\n"
    else:
        report += "[+] All users have interactive shells.\n"

    report += "\n" + "="*50 + "\n"

    with open(report_name, "w") as f:
        f.write(report)

    print(Fore.GREEN + f"[+] Report written to {report_name}")

if __name__ == "__main__":
    threshold = 90
    result = {
        "no_password": check_users_without_password(),
        "locked_accounts": check_locked_accounts(),
        "sudo_users": check_sudo_users(),
        "inactive_users": check_inactive_users_by_home(threshold),
        "special_shells": check_shells(),
        "days_threshold": threshold
    }
    write_report(result)
