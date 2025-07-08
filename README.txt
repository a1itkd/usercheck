# UserCheck 🔐

**Linux User Security Audit Tool**  
By: Ali Monam (@alimonam.sec)

---

## 🧠 What is UserCheck?

UserCheck is a Linux user security auditing tool that helps you identify:

- Users without passwords
- Locked accounts
- Users with sudo privileges
- Inactive users (based on /home access)
- Users with non-login shells

It generates a detailed report and saves it in the `logs/` folder.

---

## ⚙️ Installation

Clone the repo and give the script execute permission:

```bash
git clone https://github.com/a1itkd/Usercheck.git
cd Usercheck
chmod +x usercheck.py


## 🚀 Usage

sudo ./usercheck.py
OR 
sudo usercheck




📁 Example Output:


UserSecureCheck Report - 2025-07-08 13:00:00
==================================================

[!] Users without password:
    - testuser

[+] No locked accounts found.

[!] Users with sudo privileges:
    - ali
    - admin

[!] Inactive users (> 90 days):
    - guest: 123 days inactive

[+] All users have interactive shells.

==================================================



🔐 Notes:
This tool requires root privileges to read /etc/shadow.
Works on most Linux distributions

