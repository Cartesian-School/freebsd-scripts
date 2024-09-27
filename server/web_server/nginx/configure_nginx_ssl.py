#!/usr/bin/env python3

import os
import sys
import subprocess
import re
import shutil
from pathlib import Path

def check_root():
    if os.geteuid() != 0:
        print("This script must be run as root.")
        sys.exit(1)

def install_dependencies():
    # Install bind-tools for dig
    if shutil.which('dig') is None:
        print("Installing bind-tools for the dig command...")
        result = subprocess.run(['pkg', 'install', '-y', 'bind-tools'])
        if result.returncode != 0:
            print("Error: Failed to install bind-tools.")
            sys.exit(1)
        print("bind-tools successfully installed.")
    else:
        print("bind-tools are already installed.")

    # Install curl if not installed
    if shutil.which('curl') is None:
        print("Installing curl...")
        result = subprocess.run(['pkg', 'install', '-y', 'curl'])
        if result.returncode != 0:
            print("Error: Failed to install curl.")
            sys.exit(1)
        print("curl successfully installed.")
    else:
        print("curl is already installed.")

    # Install certbot
    if shutil.which('certbot') is None:
        print("Installing Certbot...")
        result = subprocess.run(['pkg', 'install', '-y', 'py-certbot', 'py-certbot-nginx'])
        if result.returncode != 0:
            print("Error: Failed to install Certbot.")
            sys.exit(1)
        print("Certbot installed.")
    else:
        print("Certbot is already installed.")

def get_server_ip():
    # Get the external IP address of the server
    if shutil.which('curl') is not None:
        try:
            server_ip = subprocess.check_output(['curl', '-s', 'https://api.ipify.org'], text=True).strip()
        except subprocess.CalledProcessError:
            server_ip = None
    elif shutil.which('fetch') is not None:
        try:
            server_ip = subprocess.check_output(['fetch', '-qo', '-', 'https://api.ipify.org'], text=True).strip()
        except subprocess.CalledProcessError:
            server_ip = None
    else:
        print("Error: Could not find a command to get the IP address (curl or fetch).")
        sys.exit(1)

    if not server_ip:
        print("Error: Failed to determine your server's IP address.")
        sys.exit(1)

    print(f"Your server's IP address: {server_ip}")
    return server_ip

def get_domain_name(server_ip):
    while True:
        domain = input("Enter the domain name for the SSL certificate: ").strip()
        if not domain:
            print("Error: Domain name cannot be empty.")
            continue
        # Validate domain name
        if re.match(r'^([a-zA-Z0-9](-?[a-zA-Z0-9])*\.)+[a-zA-Z]{2,}$', domain):
            # Check if the domain points to the server's IP address
            print(f"Checking DNS record for {domain}...")
            try:
                domain_ip = subprocess.check_output(['dig', '+short', domain], text=True).strip().split('\n')[-1]
            except subprocess.CalledProcessError:
                domain_ip = None

            if not domain_ip:
                print(f"Error: Could not retrieve IP address for domain {domain}.")
                continue

            print(f"Domain {domain} points to IP address: {domain_ip}")
            if domain_ip != server_ip:
                print(f"Error: Domain {domain} does not point to your server's IP address ({server_ip}).")
                print("Please update your domain's DNS record and wait for the changes to propagate.")
                choice = input("Do you want to enter a different domain name? (y/n)\n> ").strip().lower()
                if choice == 'y':
                    continue
                else:
                    print("Exiting the script.")
                    sys.exit(1)
            else:
                return domain
        else:
            print("Error: Invalid domain name. Please enter a valid domain name.")

def get_email():
    while True:
        email = input("Enter your email for Let's Encrypt registration: ").strip()
        if not email:
            print("Error: Email cannot be empty.")
            continue
        # Simple email validation
        if re.match(r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$', email):
            return email
        else:
            print("Error: Invalid email format. Please enter a valid email.")

def obtain_ssl_certificate(domain, email):
    # Obtain the SSL certificate using Certbot
    print(f"Obtaining SSL certificate for {domain}...")
    webroot_path = f"/usr/local/www/{domain}"
    cmd = [
        'certbot', 'certonly', '--webroot', '-w', webroot_path,
        '-d', domain, '--email', email, '--agree-tos', '--no-eff-email'
    ]
    result = subprocess.run(cmd)
    if result.returncode != 0:
        print("Error: Failed to obtain SSL certificate.")
        sys.exit(1)
    print("SSL certificate successfully obtained.")

def configure_nginx_ssl(domain):
    config_file = Path(f"/usr/local/etc/nginx/conf.d/{domain}.conf")
    ssl_certificate = Path(f"/usr/local/etc/letsencrypt/live/{domain}/fullchain.pem")
    ssl_certificate_key = Path(f"/usr/local/etc/letsencrypt/live/{domain}/privkey.pem")
    root_dir = Path(f"/usr/local/www/{domain}")

    # Check if SSL certificates exist
    if not ssl_certificate.exists() or not ssl_certificate_key.exists():
        print("Error: SSL certificates not found. Please ensure the certificates exist.")
        sys.exit(1)

    # Create Nginx configuration with SSL/TLS support
    print("Configuring Nginx for HTTPS...")
    config_content = f"""server {{
        listen       80;
        server_name  {domain};
        return       301 https://$host$request_uri;
    }}

    server {{
        listen       443 ssl http2;
        server_name  {domain};
        root         {root_dir};

        ssl_certificate "{ssl_certificate}";
        ssl_certificate_key "{ssl_certificate_key}";
        ssl_session_cache shared:SSL:1m;
        ssl_session_timeout  5m;
        ssl_ciphers  HIGH:!aNULL:!MD5;
        ssl_prefer_server_ciphers on;

        location / {{
            index  index.html index.htm;
        }}

        location /.well-known/acme-challenge/ {{
            allow all;
        }}
    }}
    """

    # Write the configuration file
    config_file.parent.mkdir(parents=True, exist_ok=True)
    with open(config_file, 'w') as f:
        f.write(config_content)
    print("Nginx configuration updated.")

    # Test Nginx configuration and reload the service
    print("Reloading Nginx to apply the new configuration...")
    result = subprocess.run(['service', 'nginx', 'configtest'])
    if result.returncode == 0:
        subprocess.run(['service', 'nginx', 'reload'])
        print("Nginx reloaded successfully.")
    else:
        print("Error: Nginx configuration contains errors.")
        sys.exit(1)

    print(f"SSL/TLS setup for {domain} is complete!")

def main():
    check_root()
    print("Automatic SSL/TLS setup for Nginx on FreeBSD...")
    install_dependencies()
    server_ip = get_server_ip()
    domain = get_domain_name(server_ip)
    email = get_email()
    obtain_ssl_certificate(domain, email)
    configure_nginx_ssl(domain)

if __name__ == "__main__":
    main()
