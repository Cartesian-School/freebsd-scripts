#!/usr/bin/env python3

import subprocess
import os

# Function to clear the screen
def display_clean():
    os.system('clear')
    print("")

# Function to run commands and handle errors
def run_command(command):
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Command failed: {command}")
        print(result.stderr)
        exit(1)

# Function to check if Nginx is installed
def check_nginx_installed():
    result = subprocess.run("pkg info nginx", shell=True, capture_output=True, text=True)
    if result.returncode == 0:
        print("Nginx is already installed on this system.")
        while True:
            reinstall_choice = input("Do you want to reinstall Nginx? (y/n): ").strip().lower()
            if reinstall_choice == 'y':
                run_command("pkg remove -y nginx")
                run_command("pkg install -y nginx")
                return True
            elif reinstall_choice == 'n':
                print("Nginx reinstallation canceled.")
                return False
            else:
                print("Invalid input. Please enter 'y' for yes or 'n' for no.")
    return True

# Function to check Nginx status and start it if it's not running
def start_nginx_if_not_running():
    result = subprocess.run("service nginx status", shell=True, capture_output=True, text=True)
    if result.returncode == 0:
        print("Nginx is already running.")
    else:
        print("Starting Nginx...")
        run_command("service nginx start")

# Function to install Nginx
def install_nginx():
    print("Installing Nginx HTTP Server...")
    run_command("pkg install -y nginx")
    run_command("sysrc nginx_enable=YES")
    start_nginx_if_not_running()

# Function to configure Nginx as HTTP/Proxy server
def configure_nginx():
    nginx_conf = "/usr/local/etc/nginx/nginx.conf"
    print("Configuring Nginx as an HTTP/Proxy server...")

    # Create a backup of the original configuration file
    run_command(f"cp {nginx_conf} {nginx_conf}.bak")

    # Write new configuration to the nginx.conf file
    nginx_configuration = """
user  www;
worker_processes  auto;
error_log  /var/log/nginx/error.log warn;
pid        /var/run/nginx.pid;

events {
    worker_connections  1024;
}

http {
    include       mime.types;
    default_type  application/octet-stream;

    log_format  main  '$remote_addr - $remote_user [$time_local] "$request" '
                      '$status $body_bytes_sent "$http_referer" '
                      '"$http_user_agent" "$http_x_forwarded_for"';

    access_log  /var/log/nginx/access.log  main;

    sendfile        on;
    keepalive_timeout  65;

    # Simple HTTP server
    server {
        listen       80;
        server_name  localhost;

        location / {
            root   /usr/local/www/nginx;
            index  index.html index.htm;
        }

        error_page  500 502 503 504  /50x.html;
        location = /50x.html {
            root   /usr/local/www/nginx-dist;
        }
    }

    # Proxy server
    server {
        listen 8080;

        location / {
            proxy_pass http://127.0.0.1:80;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }
    }
}
"""
    with open(nginx_conf, 'w') as f:
        f.write(nginx_configuration)
    
    print("Nginx configuration updated.")
    run_command("service nginx restart")

def main():
    display_clean()

    print("This script will install and configure Nginx as an HTTP and Proxy server.")

    # Check if Nginx is installed
    if check_nginx_installed():
        print("Proceeding with the installation and configuration of Nginx.")

        # Install Nginx
        install_nginx()

        # Configure Nginx
        configure_nginx()

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
        print("     ")
        print("")

        print("Nginx installation and configuration completed.")
    else:
        print("Nginx installation is not required.")

if __name__ == "__main__":
    main()
