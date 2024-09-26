#!/bin/sh

# Function to clear the screen
display_clean() {
    clear
    echo ""
}

# Function to run commands and handle errors
run_command() {
    command="$1"
    eval "$command"
    
    if [ $? -ne 0 ]; then
        echo "Command failed: $command"
        exit 1
    fi
}

# Function to check if Nginx is installed
check_nginx_installed() {
    if pkg info nginx >/dev/null 2>&1; then
        echo "Nginx is already installed on this system."
        while true; do
            echo "Do you want to reinstall Nginx? (y/n):"
            read reinstall_choice

            if [ "$reinstall_choice" = "y" ] || [ "$reinstall_choice" = "Y" ]; then
                run_command "pkg remove -y nginx"
                run_command "pkg install -y nginx"
                return 0
            elif [ "$reinstall_choice" = "n" ] || [ "$reinstall_choice" = "N" ]; then
                echo "Nginx reinstallation canceled."
                return 1
            else
                echo "Invalid input. Please enter 'y' for yes or 'n' for no."
            fi
        done
    else
        return 0
    fi
}

# Function to check Nginx status and start it if it's not running
start_nginx_if_not_running() {
    if service nginx status >/dev/null 2>&1; then
        echo "Nginx is already running."
    else
        echo "Starting Nginx..."
        run_command "service nginx start"
    fi
}

# Function to install Nginx
install_nginx() {
    echo "Installing Nginx HTTP Server..."
    run_command "pkg install -y nginx"
    run_command "sysrc nginx_enable=YES"
    start_nginx_if_not_running
}

# Function to configure Nginx as an HTTP/Proxy server
configure_nginx() {
    nginx_conf="/usr/local/etc/nginx/nginx.conf"
    echo "Configuring Nginx as HTTP/Proxy server..."

    # Create a backup of the original configuration file
    run_command "cp $nginx_conf ${nginx_conf}.bak"

    # Clear the configuration file and add new settings
    cat > "$nginx_conf" << EOF
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

    log_format  main  '\$remote_addr - \$remote_user [\$time_local] "\$request" '
                      '\$status \$body_bytes_sent "\$http_referer" '
                      '"\$http_user_agent" "\$http_x_forwarded_for"';

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
            proxy_set_header Host \$host;
            proxy_set_header X-Real-IP \$remote_addr;
            proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto \$scheme;
        }
    }
}
EOF

    echo "Nginx configuration updated."
    run_command "service nginx restart"
}

main() {
    display_clean

    echo "This script will install and configure Nginx as an HTTP and Proxy server."
    
    # Check if Nginx is installed
    if check_nginx_installed; then
        echo "Proceeding with the installation and configuration of Nginx."
        
        # Install Nginx
        install_nginx
        
        # Configure Nginx
        configure_nginx

        echo ""
        echo "             ,        ,"
        echo "            /(        )\`"
        echo "            \ \___   / |"
        echo "            /- _  \`-/  '"
        echo "           (/\\/ \ \   /\\"
        echo "           / /   | \`    \\"
        echo "           O O   ) /    |"
        echo "           \`-^--'\`<     '"
        echo "          (_.)  _  )   /"
        echo "           \`.___/   /"
        echo "             \`-----' /"
        echo "        <----.     __\ "
        echo "        <----|====O)))==)"
        echo "        <----'    \`--'"
        echo "             \`-----'"
        echo "     "
        echo ""

        echo "Nginx installation and configuration completed."
    else
        echo "Nginx installation is not required."
    fi
}

main
