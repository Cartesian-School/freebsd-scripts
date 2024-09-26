#!/bin/sh

# Function to create a virtual host configuration file for Nginx
configure_virtual_host() {
    # Variables for domain and root directory
    domain="www.virtual.host"
    config_file="/usr/local/etc/nginx/conf.d/virtual.host.conf"
    root_dir="/usr/share/nginx/virtual.host"
    index_file="$root_dir/index.html"

    # 1. Create a virtual host configuration file
    echo "Creating virtual host configuration for $domain at $config_file..."
    
    if [ ! -d "/usr/local/etc/nginx/conf.d" ]; then
        mkdir -p /usr/local/etc/nginx/conf.d
    fi

    # Create the configuration file for the virtual host
    cat > $config_file <<EOF
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

    # 2. Create the root directory for the virtual host
    echo "Creating the root directory for $domain at $root_dir..."
    mkdir -p $root_dir

    # 3. Create a test index.html page
    echo "Creating a test index.html page at $index_file..."
    cat > $index_file <<EOF
<html>
<body>
<div style="width: 100%; font-size: 40px; font-weight: bold; text-align: center;">
Nginx Virtual Host Test Page
</div>
</body>
</html>
EOF

    # Step 4: Reload Nginx to apply the changes
    echo "Reloading Nginx to apply the new configuration..."
    service nginx reload
    echo ""
    echo "             ,        ,"
    echo "            /(        )\`"
    echo "            \\ \\___   / |"
    echo "            /- _  \`-/  '"
    echo "           (/\\/ \\ \\   /\\"
    echo "           / /   | \`    \\"
    echo "           O O   ) /    |"
    echo "           \`-^--'\`<     '"
    echo "          (_.)  _  )   /"
    echo "           \`.___/   /"
    echo "             \`-----' /"
    echo "        <----.     __\\ "
    echo "        <----|====O)))==)"
    echo "        <----'    \`--'"
    echo "             \`-----'"
    echo ""
    echo ""

    echo "Nginx virtual host configuration for $domain is complete!"
}

main() {
    echo "Configuring Nginx virtual host..."
    configure_virtual_host
    echo "Virtual host setup is done!"
}

main
