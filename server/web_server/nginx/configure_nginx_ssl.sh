#!/bin/sh

# Check for superuser privileges
if [ "$(id -u)" -ne 0 ]; then
    echo "This script must be run as root."
    exit 1
fi

install_dependencies() {
    # Install bind-tools to use the dig command
    if ! command -v dig >/dev/null 2>&1; then
        echo "Installing bind-tools for the dig command..."
        pkg install -y bind-tools
        if [ $? -ne 0 ]; then
            echo "Error: Failed to install bind-tools."
            exit 1
        fi
        echo "bind-tools successfully installed."
    else
        echo "bind-tools are already installed."
    fi

    # Install curl if not installed
    if ! command -v curl >/dev/null 2>&1; then
        echo "Installing curl..."
        pkg install -y curl
        if [ $? -ne 0 ]; then
            echo "Error: Failed to install curl."
            exit 1
        fi
        echo "curl successfully installed."
    else
        echo "curl is already installed."
    fi

    # Install certbot from FreeBSD packages
    if ! command -v certbot >/dev/null 2>&1; then
        echo "Installing Certbot..."
        pkg install -y py311-certbot py311-certbot-nginx
        if [ $? -ne 0 ]; then
            echo "Error: Failed to install Certbot."
            exit 1
        fi
        echo "Certbot installed."
    else
        echo "Certbot is already installed."
    fi
}

get_server_ip() {
    # Get the external IP address of the server
    if command -v curl >/dev/null 2>&1; then
        server_ip=$(curl -s https://api.ipify.org)
    elif command -v fetch >/dev/null 2>&1; then
        server_ip=$(fetch -qo - https://api.ipify.org)
    else
        echo "Error: Could not find a command to get the IP address (curl or fetch)."
        exit 1
    fi

    if [ -z "$server_ip" ]; then
        echo "Error: Failed to determine your server's IP address."
        exit 1
    fi
    echo "Your server's IP address: $server_ip"
}

obtain_ssl_certificate() {
    # Prompt for domain name and email to obtain the certificate
    while true; do
        read -p "Enter the domain name for the SSL certificate: " domain
        if [ -z "$domain" ]; then
            echo "Error: Domain name cannot be empty."
            continue
        fi
        # Validate the domain name
        if echo "$domain" | grep -Eq '^([a-zA-Z0-9](-?[a-zA-Z0-9])*\.)+[a-zA-Z]{2,}$'; then
            # Check if the domain points to the server's IP address
            echo "Checking DNS record for $domain..."
            domain_ip=$(dig +short "$domain" | tail -n1)
            if [ -z "$domain_ip" ]; then
                echo "Error: Could not retrieve IP address for domain $domain."
                continue
            fi
            echo "Domain $domain points to IP address: $domain_ip"
            if [ "$domain_ip" != "$server_ip" ]; then
                echo "Error: Domain $domain does not point to your server's IP address ($server_ip)."
                echo "Please update your domain's DNS record and wait for the changes to propagate."
                echo "Do you want to enter a different domain name? (y/n)"
                read -p "> " choice
                if [ "$choice" = "y" ] || [ "$choice" = "Y" ]; then
                    continue
                else
                    echo "Exiting the script."
                    exit 1
                fi
            else
                break
            fi
        else
            echo "Error: Invalid domain name. Please enter a valid domain name."
        fi
    done

    while true; do
        read -p "Enter your email for Let's Encrypt registration: " email
        if [ -z "$email" ]; then
            echo "Error: Email cannot be empty."
            continue
        fi
        # Simple email validation
        if echo "$email" | grep -Eq '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'; then
            break
        else
            echo "Error: Invalid email format. Please enter a valid email."
        fi
    done

    # Obtain the SSL certificate using Certbot
    echo "Obtaining SSL certificate for $domain..."
    certbot certonly --webroot -w /usr/local/www/$domain -d $domain --email $email --agree-tos --no-eff-email
    if [ $? -ne 0 ]; then
        echo "Error: Failed to obtain SSL certificate."
        exit 1
    fi
    echo "SSL certificate successfully obtained."
}

configure_nginx_ssl() {
    config_file="/usr/local/etc/nginx/conf.d/$domain.conf"
    ssl_certificate="/usr/local/etc/letsencrypt/live/$domain/fullchain.pem"
    ssl_certificate_key="/usr/local/etc/letsencrypt/live/$domain/privkey.pem"
    root_dir="/usr/local/www/$domain"

    # Check if SSL certificates exist
    if [ ! -f "$ssl_certificate" ] || [ ! -f "$ssl_certificate_key" ]; then
        echo "Error: SSL certificates not found. Please ensure the certificates exist."
        exit 1
    fi

    # Create Nginx configuration with SSL/TLS support
    echo "Configuring Nginx for HTTPS..."
    cat > "$config_file" <<EOF
server {
    listen       80;
    server_name  $domain;
    return       301 https://\$host\$request_uri;
}

server {
    listen       443 ssl http2;
    server_name  $domain;
    root         $root_dir;

    ssl_certificate "$ssl_certificate";
    ssl_certificate_key "$ssl_certificate_key";
    ssl_session_cache shared:SSL:1m;
    ssl_session_timeout  5m;
    ssl_ciphers  HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;

    location / {
        index  index.html index.htm;
    }

    location /.well-known/acme-challenge/ {
        allow all;
    }
}
EOF
    echo "Nginx configuration updated."

    # Test Nginx configuration and reload the service
    echo "Reloading Nginx to apply the new configuration..."
    if service nginx configtest; then
        service nginx reload
        echo "Nginx reloaded successfully."
    else
        echo "Error: Nginx configuration contains errors."
        exit 1
    fi

    echo "SSL/TLS setup for $domain is complete!"
}

main() {
    clear
    echo ""
    echo "Automatic SSL/TLS setup for Nginx on FreeBSD..."
    echo ""
    install_dependencies
    get_server_ip
    obtain_ssl_certificate
    configure_nginx_ssl
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
    echo ""
    echo "  Automatic SSL/TLS setup is complete!"
}

main
