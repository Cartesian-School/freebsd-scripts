#!/bin/sh

# Function to display and clean the screen
display_clean() {
    clear
    echo ""
}

# Function to run system commands and handle errors
run_command() {
    command="$1"
    
    # Execute the command
    eval "$command"
    
    # Check if the command executed successfully
    if [ $? -ne 0 ]; then
        echo "Command failed: $command"
        exit 1
    fi
}

# Function to install PostgreSQL 17 and necessary dependencies
install_postgresql17() {
    echo "Installing PostgreSQL 17 and necessary dependencies..."

    # Install PostgreSQL 17 server, client, and psycopg2 dependencies
    run_command "pkg install -y postgresql17-server postgresql17-client py311-psycopg2 py311-psycopg2cffi py311-types-psycopg2"

    # Enable PostgreSQL service
    run_command "sysrc postgresql_enable=YES"

    # Initialize the PostgreSQL database cluster
    echo "Initializing PostgreSQL database..."
    run_command "/usr/local/etc/rc.d/postgresql initdb"

    # Start PostgreSQL service
    run_command "service postgresql start"

    # Check PostgreSQL service status
    run_command "service postgresql status"
}

# Function to configure PostgreSQL (pg_hba.conf)
configure_postgresql() {
    # Print the current listen_addresses setting from postgresql.conf
    run_command "grep listen_addresses /var/db/postgres/data17/postgresql.conf"

    # Backup the original pg_hba.conf
    run_command "cp -p /var/db/postgres/data17/pg_hba.conf /var/db/postgres/data17/pg_hba.conf.org"

    # Update pg_hba.conf with new settings
    pg_hba_conf_path="/var/db/postgres/data17/pg_hba.conf"
    echo "Configuring pg_hba.conf..."
    
    # Write the new configuration to pg_hba.conf
    cat > "$pg_hba_conf_path" << EOF
local   all             all                                     peer
host    all             all             127.0.0.1/32            ident
host    all             all             ::1/128                 ident
local   replication     all                                     peer
host    replication     all             127.0.0.1/32            ident
host    replication     all             ::1/128                 ident
EOF

    echo "pg_hba.conf configured successfully."

    # Restart PostgreSQL service to apply the changes
    run_command "service postgresql restart"
}

# Function to display instructions for creating a new user and database
display_instructions() {
    echo "\n==========================================="
    echo "Steps to create a new PostgreSQL user and database:"
    echo "1. Log in to the PostgreSQL shell as the superuser:"
    echo "   \$ sudo -u postgres psql"
    echo "2. Create a new user:"
    echo "   postgres=# CREATE USER your_username WITH PASSWORD 'your_password';"
    echo "3. Create a new database:"
    echo "   postgres=# CREATE DATABASE your_database;"
    echo "4. Grant privileges to the new user on the new database:"
    echo "   postgres=# GRANT ALL PRIVILEGES ON DATABASE your_database TO your_username;"
    echo "5. Exit the PostgreSQL shell:"
    echo "   postgres=# \\q"
    echo "                 ,        ,"
    echo "                /(        )\`"
    echo "                \ \___   / |"
    echo "                /- _  \`-/  '"
    echo "               (/\\/ \ \   /\\"
    echo "               / /   | \`    \\"
    echo "               O O   ) /    |"
    echo "               \`-^--'\`<     '"
    echo "              (_.)  _  )   /"
    echo "               \`.___/   /"
    echo "                 \`-----' /"
    echo "            <----.     __\ "
    echo "            <----|====O)))==)"
    echo "            <----'    \`--'"
    echo "                 \`-----'"
    echo " "   
}

main() {
    display_clean

    while true; do
        echo "Do you want to install PostgreSQL 17 and configure it? (y/n):"
        read choice

        if [ "$choice" = "y" ] || [ "$choice" = "n" ]; then
            break
        else
            echo "Invalid input. Please enter 'y' for yes or 'n' for no."
        fi
    done

    if [ "$choice" = "y" ]; then
        install_postgresql17
        
        configure_postgresql
        
        echo "PostgreSQL 17 installation and configuration completed successfully."
        display_instructions
    else
        echo "PostgreSQL installation skipped."
    fi
}

main
