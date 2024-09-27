#!/usr/bin/env python3

import os
import sys
import re
import subprocess
from pathlib import Path
import pwd
import grp

def check_root():
    if os.geteuid() != 0:
        print("This script must be run as root.")
        sys.exit(1)

def display_clean():
    os.system('clear')
    print("")

def get_domain_name():
    while True:
        domain = input("Enter the domain name for the virtual host: ").strip()
        if not domain:
            print("Error: Domain name cannot be empty.")
            continue
        # Validate domain name
        if re.match(r'^([a-zA-Z0-9](-?[a-zA-Z0-9])*\.)+[a-zA-Z]{2,}$', domain):
            return domain
        else:
            print("Error: Invalid domain name. Please enter a valid domain.")

def check_existing_configuration(domain, config_file, root_dir):
    if config_file.exists() or root_dir.exists():
        print(f"Warning: Configuration for domain '{domain}' already exists.")
        while True:
            overwrite_choice = input("Do you want to overwrite the existing configuration? (y/n): ").strip().lower()
            if overwrite_choice == 'y':
                print("Overwriting existing configuration...")
                return True
            elif overwrite_choice == 'n':
                print("Please enter a different domain name.")
                return False
            else:
                print("Please enter 'y' or 'n'.")
    return True

def create_virtual_host(domain):
    config_dir = Path("/usr/local/etc/nginx/conf.d")
    config_file = config_dir / f"{domain}.conf"
    root_dir = Path("/usr/local/www") / domain
    index_file = root_dir / "index.html"

    # Ensure the configuration directory exists
    config_dir.mkdir(parents=True, exist_ok=True)

    # Create the virtual host configuration file
    print(f"Creating virtual host configuration for {domain} at {config_file}...")
    server_block = f"""server {{
    listen       80;
    server_name  {domain};

    location / {{
        root   {root_dir};
        index  index.html index.htm;
    }}
}}"""
    with open(config_file, 'w') as f:
        f.write(server_block)
    print("Virtual host configuration created.")

    # Create the root directory for the virtual host
    print(f"Creating root directory for {domain} at {root_dir}...")
    root_dir.mkdir(parents=True, exist_ok=True)

    # Create a test index.html page
    print(f"Creating test index.html page at {index_file}...")
    index_content = f"""<html>
<body>
<div style="width: 100%; font-size: 40px; font-weight: bold; text-align: center;">
Nginx Virtual Host Test Page for {domain}
</div>
</body>
</html>
"""
    with open(index_file, 'w') as f:
        f.write(index_content)

    # Set correct permissions and ownership
    print("Setting permissions and ownership...")
    # Get uid and gid for 'www' user and group
    try:
        uid = pwd.getpwnam('www').pw_uid
        gid = grp.getgrnam('www').gr_gid
    except KeyError:
        print("Error: User or group 'www' does not exist.")
        sys.exit(1)

    for root, dirs, files in os.walk(root_dir):
        os.chown(root, uid, gid)
        os.chmod(root, 0o755)
        for d in dirs:
            os.chown(os.path.join(root, d), uid, gid)
            os.chmod(os.path.join(root, d), 0o755)
        for file in files:
            os.chown(os.path.join(root, file), uid, gid)
            os.chmod(os.path.join(root, file), 0o755)

    # Test Nginx configuration and reload the service
    print("Reloading Nginx to apply the new configuration...")
    result = subprocess.run(['service', 'nginx', 'configtest'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if result.returncode == 0:
        subprocess.run(['service', 'nginx', 'reload'])
        print("Nginx reloaded successfully.")
    else:
        print("Error: Nginx configuration contains errors.")
        print(result.stdout)
        print(result.stderr)
        sys.exit(1)

    print(f"\nVirtual host setup for {domain} is complete!")

def main():
    display_clean()
    check_root()
    print("Configuring Nginx virtual host...\n")
    while True:
        domain = get_domain_name()
        config_file = Path("/usr/local/etc/nginx/conf.d") / f"{domain}.conf"
        root_dir = Path("/usr/local/www") / domain
        if check_existing_configuration(domain, config_file, root_dir):
            break
    create_virtual_host(domain)
            
    print("")
    print("             ,        ,")
    print("            /(        )`")
    print("            \\ \\___   / |")
    print("            /- _  `-/  '")
    print("           (/\\/ \\ \\   /\\")
    print("           / /   | `    \\")
    print("           O O   ) /    |")
    print("           `-^--'`<     '")
    print("          (_.)  _  )   /")
    print("           `.___/   /")
    print("             `-----' /")
    print("        <----.     __\\ ")
    print("        <----|====O)))==)")
    print("        <----'    `--'")
    print("             `-----'")
    print("")  
    print("Your virtual host configuration is complete!")
    print("")
if __name__ == "__main__":
    main()
