#!/usr/bin/env python3

import os
import subprocess
import shutil
import difflib
import re

os.system('clear')
print("-----------------------")
print("   Cartesian School    ")
print("-----------------------")
print("** FreeBSD ************")
print("************* 14.1 ****")
print("* 09.24 ***************")
print("***********************")
os.system('clear')
print("")
print("=======================================================================")
print("")
print("")
print("  CCCCC    AAAAA   RRRRR  TTTTTTT  EEEEE  SSSSS  IIIII   AAAAA   N     N")
print(" C     C  A     A  R    R    T     E      S        I    A     A  NN    N")
print(" C        A AAA A  RRRRR     T     EEEEE  SSSSS    I    A AAA A  N N   N")
print(" C        A     A  R    R    T     E          S    I    A     A  N  N  N")
print(" C     C  A     A  R     R   T     E          S    I    A     A  N   N N")
print("  CCCCC   A     A  R     R   T     EEEEE  SSSSS  IIIII  A     A  N     N")
print("")
print("")
print("             ,        ,")
print("            /(        )\`")
print("            \ \___   / |")
print("            /- _  \`-/  '")
print("           (/\\/ \ \   /\\")
print("           / /   | \`    \\")
print("           O O   ) /    |")
print("           \`-^--'\`<     '")
print("          (_.)  _  )   /")
print("           \`.___/   /")
print("             \`-----' /")
print("        <----.     __\\ ")
print("        <----|====O)))==)")
print("        <----'    \`--'")
print("             \`-----'")
print("     ")
print("     Powered on FreeBSD v.14.1 ")
print("")
print("==========================================================================")
print("")
os.system('clear')

# 1. Automatic Sudo Rights Configuration for the %wheel Group

# Path to the sudoers file
sudoers_file = '/usr/local/etc/sudoers'
backup_file = '/usr/local/etc/sudoers.bak'

# Create a backup of the sudoers file
shutil.copyfile(sudoers_file, backup_file)

# Open the sudoers file for reading and writing
with open(sudoers_file, 'r') as file:
    lines = file.readlines()

# Search for the commented line
commented_line = '#%wheel ALL=(ALL) ALL'
uncommented_line = '%wheel ALL=(ALL:ALL) ALL'

# Use difflib to compare the content
differ = difflib.Differ()

# Compare lines and display differences
diff = list(differ.compare([commented_line], [uncommented_line]))

# Output the differences to show how the lines differ
print("\n".join(diff))

# If the commented line is found, replace it with the uncommented one
with open(sudoers_file, 'w') as file:
    for line in lines:
        if commented_line in line:
            file.write(uncommented_line + '\n')
            print(f"The line '{commented_line}' was replaced with '{uncommented_line}'")
        else:
            file.write(line)

print("Sudo rights for the %wheel group have been updated.")

os.system('clear')

# 2. Git installation
print("Git installation")
# Ask the user if they want to install Git and only accept 'y' or 'n'
while True:
    install_git = input("Do you want to install Git? (y/n): ").strip().lower()
    if install_git in ['y', 'n']:
        break
    print("Please enter 'y' for yes or 'n' for no.")

if install_git == 'y':
    # Print a blank line
    print(" ")

    # Display the message about Git installation
    print("Installing Git...")

    # Install Git using pkg
    subprocess.run(["pkg", "install", "-y", "git"])

    # Display the installed Git version
    subprocess.run(["git", "-V"])

    # Ask for user's name and email for Git configuration
    while True:
        user_name = input("Enter your Git user.name (e.g., 'John Doe'): ").strip()
        # Check if the input contains only valid characters (letters, spaces, and apostrophes)
        if re.match(r"^[a-zA-Z\s']+$", user_name):
            break
        print("Invalid name. Please use only letters, spaces, and apostrophes.")

    while True:
        user_email = input("Enter your Git user.email (e.g., 'example@mail.com'): ").strip()
        # Validate email using regex
        if re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", user_email):
            break
        print("Invalid email. Please enter a valid email address.")

    # Configure Git with the provided user name and email
    subprocess.run(["git", "config", "--global", "user.name", user_name])
    subprocess.run(["git", "config", "--global", "user.email", user_email])

    # Configure Git editor
    subprocess.run(["git", "config", "--global", "core.editor", "code --wait"])

    # Set default branch to 'main'
    subprocess.run(["git", "config", "--global", "init.defaultBranch", "main"])

    # Configure pull behavior
    subprocess.run(["git", "config", "--global", "pull.rebase", "false"])

    # Set automatic conversion of line endings
    subprocess.run(["git", "config", "--global", "core.autocrlf", "input"])

    # Configure fast-forward merges
    subprocess.run(["git", "config", "--global", "merge.ff", "only"])

    # Enable color in the Git interface
    subprocess.run(["git", "config", "--global", "color.ui", "auto"])

    # Configure branch colors
    subprocess.run(["git", "config", "--global", "color.branch.current", "yellow reverse"])
    subprocess.run(["git", "config", "--global", "color.branch.local", "yellow"])
    subprocess.run(["git", "config", "--global", "color.branch.remote", "blue"])

    # Configure diff colors
    subprocess.run(["git", "config", "--global", "color.diff.meta", "yellow bold"])
    subprocess.run(["git", "config", "--global", "color.diff.frag", "magenta bold"])
    subprocess.run(["git", "config", "--global", "color.diff.old", "red bold"])
    subprocess.run(["git", "config", "--global", "color.diff.new", "green bold"])

    # Configure status colors
    subprocess.run(["git", "config", "--global", "color.status.added", "green"])
    subprocess.run(["git", "config", "--global", "color.status.changed", "yellow"])
    subprocess.run(["git", "config", "--global", "color.status.untracked", "red"])

    # Display the current Git configuration
    print("Git config list: ")
    print("--------------------------------------------------------")
    print("")

    subprocess.run(["git", "config", "--list"])

    print("")
    print("Git successfully installed and configured")

else:
    print("Git installation skipped.")

os.system('clear')

