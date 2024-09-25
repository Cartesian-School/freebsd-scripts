#!/usr/bin/env python3

import os
import subprocess
import shutil
import difflib
import re
import getpass

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
print("1. Automatic Sudo Rights Configuration for the %wheel Group")
print("")
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
print("2. Git installation")
print("")
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
primt("")


# 3. Installation of OpenJDK
print("3. Installation of OpenJDK")
print("")

# 3.1. Ask the user if they want to install OpenJDK
while True:
    install_jdk = input("Do you want to install OpenJDK? (y/n): ").strip().lower()
    if install_jdk in ['y', 'n']:
        break
    print("Please enter 'y' for yes or 'n' for no.")

if install_jdk == 'y':
    # Ask the user which version of OpenJDK to install
    while True:
        print("Select the version of OpenJDK to install:")
        print("1. OpenJDK 11 (Java Runtime Environment 11 LTS)")
        print("2. OpenJDK 17 (Java Development Kit 17 LTS)")
        print("3. OpenJDK 21 (Java Development Kit 21 LTS)")
        print("0. Cancel and skip installation")
        user_choice = input("Enter 1, 2, 3, or 0: ").strip()

        if user_choice in ['0', '1', '2', '3']:
            break
        print("Invalid input. Please enter 1, 2, 3, or 0.")

    # If the user selects '0', skip installation
    if user_choice == '0':
        print("OpenJDK installation skipped.")
    else:
        # Determine the package to install based on user's choice
        if user_choice == '1':
            jdk_package = 'openjdk11'
        elif user_choice == '2':
            jdk_package = 'openjdk17'
        elif user_choice == '3':
            jdk_package = 'openjdk21'

        # Confirm the installation
        while True:
            confirm_install = input(f"Do you want to install {jdk_package}? (y/n): ").strip().lower()
            if confirm_install in ['y', 'n']:
                break
            print("Please enter 'y' for yes or 'n' for no.")

        if confirm_install == 'y':
            # Installing the selected OpenJDK package
            print(f"Installing {jdk_package}...")
            subprocess.run(["pkg", "install", "-y", jdk_package], check=True)
            print("")
            
            # 3.2 Mounting fdescfs and procfs

            # Display the message
            print("Mounting fdesc and proc filesystems...")

            # Mount fdescfs
            subprocess.run(["mount", "-t", "fdescfs", "fdesc", "/dev/fd"], check=True)

            # Mount procfs
            subprocess.run(["mount", "-t", "procfs", "proc", "/proc"], check=True)

            # Print a blank line
            print("")

            # 7.3 Adding entries to /etc/fstab for persistent mounting

            # Print a blank line
            print("")

            # Display the message
            print("Adding entries to /etc/fstab for auto-mounting fdescfs and procfs...")

            # Define the entries to add to /etc/fstab
            fstab_entries = """
            fdesc   /dev/fd         fdescfs             rw      0   0
            proc    /proc           procfs              rw      0   0
            """

            # Add the entries to /etc/fstab
            with open("/etc/fstab", "a") as fstab_file:
                fstab_file.write(fstab_entries)
            print("")

            # 3.4 Checking Java installation

            # Display the message
            print(f"Checking {jdk_package} installation:")

            # Check Java version
            subprocess.run(["java", "-version"], check=True)        
            print("")

            # Check javac version (only for JDK packages)
            if jdk_package != 'openjdk11':
                subprocess.run(["javac", "-version"], check=True)

            print(f"{jdk_package} successfully installed and configured.")
        else:
            print(f"Installation of {jdk_package} was canceled.")
else:
    print("OpenJDK installation skipped.")

os.system('clear')
primt("")


# 4. Sound driver installation and configuration
print("4. Sound driver installation and configuration")
print("")

# 4.1. Sound driver installation
# Ask the user if they want to configure the sound device
while True:
    configure_sound = input("Do you want to configure the sound device? (y/n): ").strip().lower()
    if configure_sound in ['y', 'n']:
        break
    print("Please enter 'y' for yes or 'n' for no.")

if configure_sound == 'y':
    # Display the message about configuring the sound device
    print("Configuring the sound device...")

    # Load the snd_hda module
    subprocess.run(["kldload", "snd_hda"], check=True)

    # Path to the /boot/loader.conf file
    loader_conf = "/boot/loader.conf"
    snd_hda_line = 'snd_hda_load="YES"'

    # Check if 'snd_hda_load="YES"' is present in /boot/loader.conf, if not, add it
    if os.path.exists(loader_conf):
        with open(loader_conf, 'r') as file:
            content = file.read()
        if snd_hda_line not in content:
            with open(loader_conf, 'a') as file:
                file.write(snd_hda_line + "\n")
            print(f"Added '{snd_hda_line}' to {loader_conf}")
        else:
            print(f"The line '{snd_hda_line}' is already present in {loader_conf}")
    else:
        # If the file doesn't exist, create it and add the line
        with open(loader_conf, 'w') as file:
            file.write(snd_hda_line + "\n")
        print(f"Created file {loader_conf} and added '{snd_hda_line}'")

    # Set hw.snd.default_unit=0
    subprocess.run(["sysctl", "hw.snd.default_unit=0"], check=True)

    # Path to the /etc/sysctl.conf file
    sysctl_conf = "/etc/sysctl.conf"
    hw_snd_line = 'hw.snd.default_unit=0'

    # Check if 'hw.snd.default_unit=0' is present in /etc/sysctl.conf, if not, add it
    if os.path.exists(sysctl_conf):
        with open(sysctl_conf, 'r') as file:
            content = file.read()
        if hw_snd_line not in content:
            with open(sysctl_conf, 'a') as file:
                file.write(hw_snd_line + "\n")
            print(f"Added '{hw_snd_line}' to {sysctl_conf}")
        else:
            print(f"The line '{hw_snd_line}' is already present in {sysctl_conf}")
    else:
        # If the file doesn't exist, create it and add the line
        with open(sysctl_conf, 'w') as file:
            file.write(hw_snd_line + "\n")
        print(f"Created file {sysctl_conf} and added '{hw_snd_line}'")

    # 4.2. Installation and configuration of sound packages for XFCE

    # Display the message about installing sound packages
    print("Installing sound packages for XFCE...")

    # List of packages to install
    packages = [
        "pulseaudio",
        "pavucontrol",
        "xfce4-pulseaudio-plugin",
        "vlc"
    ]

    # Install the packages
    subprocess.run(["pkg", "install", "-y"] + packages, check=True)

    # Enable pulseaudio on system startup
    subprocess.run(["sysrc", 'pulseaudio_enable="YES"'], check=True)

    # Re-apply the hw.snd.default_unit=0 setting
    subprocess.run(["sysctl", "hw.snd.default_unit=0"], check=True)

    # Print a blank line for formatting
    print("")

    print("Sound packages successfully installed and configured.")
else:
    print("Sound device configuration skipped.")
    
os.system('clear')
primt("")


# 5. Install the webcam drivers and utilities
print("Install the webcam drivers and utilities")
print("")

# 5.1. Ask the user if they want to install the webcam drivers and utilities
while True:
    install_webcam = input("Do you want to install the webcam drivers and utilities? (y/n): ").strip().lower()
    if install_webcam in ['y', 'n']:
        break
    print("Please enter 'y' for yes or 'n' for no.")

if install_webcam == 'y':
    # 5.2. Installation of necessary packages for the webcam
    print("Installing v4l-utils, v4l_compat, and webcamd...")
    subprocess.run(["pkg", "install", "-y", "v4l-utils", "v4l_compat", "webcamd"], check=True)

    # 5.3. Configure webcamd as a service
    print("Configuring webcamd as a service...")
    subprocess.run(["sysrc", 'webcamd_enable="YES"'], check=True)

    # 5.4. Load the cuse module for the webcam
    print("Loading the cuse module...")
    subprocess.run(["kldload", "cuse"], check=True)

    loader_conf = "/boot/loader.conf"
    cuse_line = 'cuse_load="YES"'

    # Check if 'cuse_load="YES"' is present in loader.conf, and add it if necessary
    if os.path.exists(loader_conf):
        with open(loader_conf, 'r') as file:
            content = file.read()
        if cuse_line not in content:
            with open(loader_conf, 'a') as file:
                file.write(cuse_line + "\n")
            print(f"Added '{cuse_line}' to {loader_conf}")
        else:
            print(f"The line '{cuse_line}' is already present in {loader_conf}")
    else:
        # If the file doesn't exist, create it and add the line
        with open(loader_conf, 'w') as file:
            file.write(cuse_line + "\n")
        print(f"Created {loader_conf} and added '{cuse_line}'")

    print("")

    # 5.5. Add user permissions for working with the webcam
    print("Adding root and the current user to the webcamd group...")
    current_user = getpass.getuser()
    subprocess.run(["pw", "groupmod", "webcamd", "-m", f"root,{current_user}"], check=True)
    print("")

    # 5.6. Check connected devices
    print("Checking connected USB devices for the webcam...")
    usbconfig_output = subprocess.run(["usbconfig", "list"], capture_output=True, text=True, check=True)
    print(usbconfig_output.stdout)

    webcam_device = None
    for line in usbconfig_output.stdout.splitlines():
        if "ugen" in line:
            webcam_device = line.split()[0]
            break

    if webcam_device:
        print(f"Webcam device found: {webcam_device}")

        # 5.7. Automatically configure webcamd with the detected device
        print(f"Configuring webcamd with device {webcam_device}...")
        subprocess.run(["sysrc", f'webcamd_0_flags="-d {webcam_device}"'], check=True)
        print("Webcam successfully configured.")
    else:
        print("No webcam device detected. Continuing with the next section.")
else:
    print("Webcam installation skipped.")
primt("")
print("Proceeding to the next section of the installation...")

os.system('clear')
primt("")

# 6. Install XOrg
print("6. Install XOrg")
print("")
# 6.1. Ask the user if they want to install XOrg
while True:
    install_xorg = input("Do you want to install XOrg? (y/n): ").strip().lower()
    if install_xorg in ['y', 'n']:
        break
    print("Please enter 'y' for yes or 'n' for no.")

if install_xorg == 'y':
    print("Installing XOrg...")
    subprocess.run(["pkg", "install", "-y", "xorg"], check=True)

    # 6.2 Adding the root user to the video group
    print("Adding root to the video group...")
    print("")
    subprocess.run(["pw", "groupmod", "video", "-m", "root"], check=True)   
    print("XOrg and video group setup completed successfully.")
else:
    print("XOrg installation skipped.")
print("Proceeding to the next section of the installation...")

os.system('clear')
primt("")
