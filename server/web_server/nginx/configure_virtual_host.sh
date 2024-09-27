#!/bin/sh

# Check for superuser privileges
if [ "$(id -u)" -ne 0 ]; then
    echo "This script must be run as root."
    exit 1
fi

configure_virtual_host() {
    while true; do
        # Prompt the user for the domain name
        read -p "Enter the domain name for the virtual host: " domain
        if [ -z "$domain" ]; then
            echo "Error: Domain name cannot be empty."
            continue
        fi

        # Validate the domain name for invalid characters
        if echo "$domain" | grep -Eq '^([a-zA-Z0-9](-?[a-zA-Z0-9])*\.)+[a-zA-Z]{2,}$'; then
            # Check if the domain already exists
            config_file="/usr/local/etc/nginx/conf.d/$domain.conf"
            root_dir="/usr/local/www/$domain"

            if [ -e "$config_file" ] || [ -d "$root_dir" ]; then
                echo "Warning: Configuration for domain '$domain' already exists."
                while true; do
                    read -p "Do you want to overwrite the existing configuration? (y/n): " overwrite_choice
                    case "$overwrite_choice" in
                        y|Y )
                            echo "Overwriting existing configuration..."
                            break 2  # Exit both loops and proceed
                            ;;
                        n|N )
                            echo "Please enter a different domain name."
                            continue 2  # Restart the outer loop
                            ;;
                        * )
                            echo "Please enter 'y' or 'n'."
                            ;;
                    esac
                done
            else
                break  # Domain is valid and does not exist; proceed
            fi
        else
            echo "Error: Invalid domain name. Please enter a valid domain."
        fi
    done

    # Proceed with setting up the virtual host
    # Variables are already set: $domain, $config_file, $root_dir
    index_file="$root_dir/index.html"

    # Create the virtual host configuration file
    echo "Creating virtual host configuration for $domain at $config_file..."

    if [ ! -d "/usr/local/etc/nginx/conf.d" ]; then
        mkdir -p "/usr/local/etc/nginx/conf.d"
    fi

    cat > "$config_file" <<EOF
server {
    listen       80;
    server_name  $domain;

    location / {
        root   $root_dir;
        index  index.html index.htm;
    }
}
EOF
    echo "Virtual host configuration created."

    # Create the root directory for the virtual host
    echo "Creating root directory for $domain at $root_dir..."
    mkdir -p "$root_dir"

    # Create a test index.html page
    echo "Creating test index.html page at $index_file..."
    cat > "$index_file" <<EOF
<html>
<body>
<div style="width: 100%; font-size: 40px; font-weight: bold; text-align: center;">
Nginx Virtual Host Test Page for $domain
</div>
</body>
</html>
EOF

    # Set correct permissions and ownership
    chown -R www:www "$root_dir"
    chmod -R 755 "$root_dir"

    # Test Nginx configuration and reload the service
    echo "Reloading Nginx to apply the new configuration..."
    if service nginx configtest; then
        service nginx reload
        echo "Nginx reloaded successfully."
    else
        echo "Error: Nginx configuration contains errors."
        exit 1
    fi

    echo "Virtual host setup for $domain is complete!"
}

main() {
    echo "Configuring Nginx virtual host..."
    configure_virtual_host
    echo "Virtual host configuration is complete!"
}

main
