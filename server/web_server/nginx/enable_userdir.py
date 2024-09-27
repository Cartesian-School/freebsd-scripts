#!/usr/bin/env python3

import os
import sys
import subprocess
import re
from pathlib import Path


def display_clean():
    os.system('clear')
    print("")

def check_root():
    if os.geteuid() != 0:
        print("This script must be run as root.")
        sys.exit(1)

def get_nginx_conf():
    # Attempt to find the main Nginx configuration file
    possible_paths = [
        "/usr/local/etc/nginx/nginx.conf",
        "/etc/nginx/nginx.conf"
    ]
    for path in possible_paths:
        if os.path.isfile(path):
            return path
    print("Error: Main Nginx configuration file not found.")
    sys.exit(1)

def enable_userdir_in_nginx():
    nginx_conf = get_nginx_conf()

    # Check if include for conf.d/*.conf is enabled
    with open(nginx_conf, 'r') as f:
        nginx_conf_content = f.read()

    if not re.search(r'include.*conf\.d/\*\.conf;', nginx_conf_content):
        print("Enabling configurations from conf.d in nginx.conf...")
        nginx_conf_content = re.sub(
            r'(http\s*\{)',
            r'\1\n    include conf.d/*.conf;',
            nginx_conf_content,
            count=1
        )
        with open(nginx_conf, 'w') as f:
            f.write(nginx_conf_content)

    # Find the conf.d configuration directory from nginx.conf
    matches = re.findall(r'^\s*include\s+(.*conf\.d/\*\.conf);', nginx_conf_content, re.MULTILINE)
    if matches:
        nginx_conf_dir = matches[0].replace('/*', '')
        nginx_conf_dir = nginx_conf_dir.strip('"').strip("'").rstrip('/')
        if not nginx_conf_dir.startswith('/'):
            nginx_conf_dir = os.path.join(os.path.dirname(nginx_conf), nginx_conf_dir)
    else:
        nginx_conf_dir = "/usr/local/etc/nginx/conf.d"

    userdir_conf = os.path.join(nginx_conf_dir, "userdir.conf")

    # Create the configuration directory if it doesn't exist
    os.makedirs(nginx_conf_dir, exist_ok=True)

    # Check if Userdir configuration already exists
    if os.path.isfile(userdir_conf):
        print("Userdir configuration already exists in Nginx.")
    else:
        # Create the Userdir configuration file
        print("Enabling Userdir in Nginx configuration...")
        with open(userdir_conf, 'w') as f:
            f.write("""server {
    listen       80;
    server_name  localhost;

    location ~ ^/~(.+?)(/.*)?$ {
        alias /home/$1/public_html$2;
        index  index.html index.htm;
        autoindex on;
    }
}
""")
        print("Userdir configuration added to Nginx.")

    # Extract server_name from configuration
    server_name = None
    with open(userdir_conf, 'r') as f:
        for line in f:
            match = re.match(r'^\s*server_name\s+(.*);', line)
            if match:
                server_name = match.group(1)
                break

    # If server_name is localhost or empty, try to find another server_name
    if not server_name or server_name == "localhost":
        conf_files = Path(nginx_conf_dir).glob("*.conf")
        for conf_file in conf_files:
            with open(conf_file, 'r') as f:
                for line in f:
                    match = re.match(r'^\s*server_name\s+(.*);', line)
                    if match and match.group(1) != "localhost":
                        server_name = match.group(1)
                        break
            if server_name and server_name != "localhost":
                break
        else:
            server_name = "localhost"

    # Test Nginx configuration and reload the service
    print("Reloading Nginx to apply the new configuration...")
    result = subprocess.run(['nginx', '-t'])
    if result.returncode == 0:
        subprocess.run(['service', 'nginx', 'reload'])
        print("Nginx reloaded successfully.")
    else:
        print("Error: Nginx configuration contains errors.")
        sys.exit(1)

    return server_name

def create_user_public_html():
    while True:
        # Prompt for username
        username = input("Enter the username to create public_html: ").strip()

        # Check if the user exists
        try:
            import pwd
            pwd.getpwnam(username)
            break
        except KeyError:
            print(f"Error: User {username} does not exist.")
            choice = input("Would you like to try again? (y/n): ").strip().lower()
            if choice == 'y':
                continue
            else:
                print("Exiting the script.")
                sys.exit(1)

    user_home = os.path.expanduser(f"~{username}")
    public_html_dir = os.path.join(user_home, "public_html")
    index_file = os.path.join(public_html_dir, "index.html")

    # Set permissions on the user's home directory
    os.chmod(user_home, 0o711)

    # Create the public_html directory
    os.makedirs(public_html_dir, exist_ok=True)

    # Set permissions on public_html
    os.chmod(public_html_dir, 0o755)

    # Create the test index.html page
    with open(index_file, 'w') as f:
        f.write("""<html>
<body>
<div style="width: 100%; font-size: 40px; font-weight: bold; text-align: center;">
Nginx UserDir Test Page
</div>
</body>
</html>
""")

    # Set ownership of the files
    uid = pwd.getpwnam(username).pw_uid
    gid = pwd.getpwnam(username).pw_gid
    os.chown(public_html_dir, uid, gid)
    os.chown(index_file, uid, gid)

    print(f"Test page created at {index_file}")
    return username

def main():
    display_clean()
    check_root()
    print("Enabling Userdir in Nginx and creating a test page for the user... \n")
    server_name = enable_userdir_in_nginx()
    username = create_user_public_html()
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
    print(f"Setup complete. You can check the page at http://{server_name}/~{username}/")
    print("") 

if __name__ == "__main__":
    main()
