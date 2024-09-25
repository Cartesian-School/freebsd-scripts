#!/usr/bin/env python3

import os
import subprocess
import shutil

os.system('clear')

print("-----------------------")
print("   Cartesian School    ")
print("-----------------------")
print("** FreeBSD ************")
print("************* 14.1 ****")
print("* 09.24 ***************")
print("***********************")
os.system('clear')

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

# 1. Unlock %wheel
subprocess.run(["pkg", "install", "-y", "sudo"])
print("add %wheel in sudoers...")

# sudoers
sudoers_file = '/usr/local/etc/sudoers'
backup_file = '/usr/local/etc/sudoers.bak'

# string in sudoers
search_line = '%wheel ALL=(ALL) ALL'
line_found = False

with open(sudoers_file, 'r') as file:
    for line in file:
        line = line.strip()
        if line == search_line:
            line_found = True
            break

if not line_found:
    # backup sudoers
    shutil.copyfile(sudoers_file, backup_file)
    # added new string in sudoers
    with open(sudoers_file, 'a') as file:
        file.write('%wheel ALL=(ALL:ALL) ALL\n')
    print(" %wheel successfully added")
else:
    print("The %wheel group already has sudo rights.")

print("group wheel successfully added")

