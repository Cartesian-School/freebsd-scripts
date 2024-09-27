#!/bin/sh

# Check for superuser privileges
if [ "$(id -u)" -ne 0 ]; then
    echo "This script must be run as root."
    exit 1
fi

get_nginx_conf() {
    # Attempt to find the main Nginx configuration file
    if [ -f "/usr/local/etc/nginx/nginx.conf" ]; then
        nginx_conf="/usr/local/etc/nginx/nginx.conf"
    elif [ -f "/etc/nginx/nginx.conf" ]; then
        nginx_conf="/etc/nginx/nginx.conf"
    else
        echo "Error: Main Nginx configuration file not found."
        exit 1
    fi
}

enable_userdir_in_nginx() {
    get_nginx_conf

    # Check if include for conf.d/*.conf is enabled
    if ! grep -q 'include.*conf\.d/\*\.conf;' "$nginx_conf"; then
        echo "Enabling configurations from conf.d in nginx.conf..."
        sed -i.bak '/http {/a\\
    \    include conf.d/*.conf;\
    ' "$nginx_conf"
    fi

    # Find the conf.d configuration directory from nginx.conf
    nginx_conf_dir=$(grep -E '^\s*include' "$nginx_conf" | grep 'conf.d/\*\.conf' | awk '{print $2}' | sed 's|/[*].*||; s|"||g; s|;||')

    if [ -z "$nginx_conf_dir" ]; then
        nginx_conf_dir="/usr/local/etc/nginx/conf.d"
    else
        # If the path is relative, convert it to absolute based on nginx.conf location
        if [ "${nginx_conf_dir#/}" = "$nginx_conf_dir" ]; then
            nginx_conf_dir="$(dirname "$nginx_conf")/$nginx_conf_dir"
        fi
    fi

    # Remove trailing slash
    nginx_conf_dir="${nginx_conf_dir%/}"

    userdir_conf="$nginx_conf_dir/userdir.conf"

    # Create the configuration directory if it doesn't exist
    mkdir -p "$nginx_conf_dir"

    # Check if Userdir configuration already exists
    if [ -f "$userdir_conf" ]; then
        echo "Userdir configuration already exists in Nginx."
    else
        # Create the Userdir configuration file
        echo "Enabling Userdir in Nginx configuration..."
        cat > "$userdir_conf" <<EOF
server {
    listen       80;
    server_name  localhost;

    location ~ ^/~(.+?)(/.*)?\$ {
        alias /home/\$1/public_html\$2;
        index  index.html index.htm;
        autoindex on;
    }
}
EOF
        echo "Userdir configuration added to Nginx."
    fi

    # Extract server_name from configuration
    server_name=$(grep -E '^\s*server_name' "$userdir_conf" | head -n1 | awk '{print $2}' | tr -d ';')

    # If server_name is localhost or empty, try to find another server_name
    if [ "$server_name" = "localhost" ] || [ -z "$server_name" ]; then
        # Search for server_name in other configurations
        server_name=$(grep -E '^\s*server_name' "$nginx_conf_dir"/*.conf | grep -v 'localhost' | head -n1 | awk '{print $3}' | tr -d ';')
        if [ -z "$server_name" ]; then
            server_name="localhost"
        fi
    fi

    # Test Nginx configuration and reload the service
    echo "Reloading Nginx to apply the new configuration..."
    if nginx -t; then
        service nginx reload
        echo "Nginx reloaded successfully."
    else
        echo "Error: Nginx configuration contains errors."
        exit 1
    fi
}

create_user_public_html() {
    while true; do
        # Prompt for username
        read -p "Enter the username to create public_html: " username

        # Check if the user exists
        if ! id "$username" >/dev/null 2>&1; then
            echo "Error: User $username does not exist."
            read -p "Would you like to try again? (y/n): " choice
            if [ "$choice" = "y" ] || [ "$choice" = "Y" ]; then
                continue
            else
                echo "Exiting the script."
                exit 1
            fi
        else
            break
        fi
    done

    user_home=$(eval echo "~$username")
    public_html_dir="$user_home/public_html"
    index_file="$public_html_dir/index.html"

    # Set permissions on the user's home directory
    chmod 711 "$user_home"

    # Create the public_html directory
    mkdir -p "$public_html_dir"

    # Set permissions on public_html
    chmod 755 "$public_html_dir"

    # Create the test index.html page
    cat > "$index_file" <<EOF
<html>
<body>
<div style="width: 100%; font-size: 40px; font-weight: bold; text-align: center;">
Nginx UserDir Test Page
</div>
</body>
</html>
EOF

    # Set ownership of the files
    chown -R "$username:$username" "$public_html_dir"

    echo "Test page created at $index_file"
}

main() {
    clear
    echo "Enabling Userdir in Nginx and creating a test page for the user..."
    enable_userdir_in_nginx
    create_user_public_html
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
    echo "Setup complete. You can check the page at http://$server_name/~$username/"
    echo ""
}

main
