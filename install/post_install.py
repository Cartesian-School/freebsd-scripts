#!/usr/bin/env python3

import os
import subprocess
import shutil
import difflib

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


print("group wheel successfully added")

