#!/bin/sh

# Function to display and clean the screen
display_clean() {
    clear
    echo ""
}

# Function to install PostgreSQL for a specific version
install_postgresql() {
    local version=$1
    echo "Installing PostgreSQL $version and necessary dependencies..."

    # Install PostgreSQL server, client, and psycopg2 dependencies
    pkg install -y postgresql${version}-server postgresql${version}-client py311-psycopg2 py311-psycopg2cffi py311-types-psycopg2

    # Enable PostgreSQL service
    sysrc postgresql_enable="YES"

    # Initialize the PostgreSQL database cluster
    echo "Initializing PostgreSQL database..."
    /usr/local/etc/rc.d/postgresql initdb

    # Start PostgreSQL service
    service postgresql start

    # Check PostgreSQL service status
    service postgresql status
}

# Function to configure PostgreSQL (pg_hba.conf)
configure_postgresql() {
    local version=$1
    local conf_path="/var/db/postgres/data${version}/postgresql.conf"
    local pg_hba_conf_path="/var/db/postgres/data${version}/pg_hba.conf"

    # Print the current listen_addresses setting from postgresql.conf
    grep "listen_addresses" "$conf_path"

    # Backup the original pg_hba.conf
    cp -p "$pg_hba_conf_path" "${pg_hba_conf_path}.org"

    # Update pg_hba.conf with new settings
    echo "Configuring pg_hba.conf..."
    cat > "$pg_hba_conf_path" << EOF
local   all             all                                     peer
host    all             all             127.0.0.1/32            ident
host    all             all             ::1/128                 ident
local   replication     all                                     peer
host    replication     all             127.0.0.1/32            ident
host    replication     all             ::1/128                 ident
EOF

    # Restart PostgreSQL service to apply the changes
    service postgresql restart
}

# Function to create and delete a test database
create_and_delete_test_db() {
    echo "Creating test database 'test_db'..."

    # Create the test database and user
    sudo -u postgres psql -c "CREATE DATABASE test_db;"
    sudo -u postgres psql -c "CREATE USER test_user WITH PASSWORD 'password';"
    sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE test_db TO test_user;"

    # Create a test table and insert data
    sudo -u postgres psql -d test_db -c "CREATE TABLE test_table (id SERIAL PRIMARY KEY, message TEXT);"
    sudo -u postgres psql -d test_db -c "INSERT INTO test_table (message) VALUES ('All OK');"

    # Verify the inserted data
    sudo -u postgres psql -d test_db -c "SELECT * FROM test_table;"

    # Drop the test database and user
    sudo -u postgres psql -c "DROP DATABASE test_db;"
    sudo -u postgres psql -c "DROP USER test_user;"

    echo "Test database 'test_db' and user 'test_user' were successfully deleted."
}

# Function to display instructions for creating a new user and database
display_instructions() {
    echo ""
    echo "Steps to create a new PostgreSQL user and database:"
    echo ""
    echo "1. Log in to the PostgreSQL shell as the superuser:"
    echo "   \$ sudo -u postgres psql"
    echo "2. Create a new user:"
    echo '   postgres=# CREATE USER your_username WITH PASSWORD "your_password";'
    echo "3. Create a new database:"
    echo "   postgres=# CREATE DATABASE your_database;"
    echo "4. Grant privileges to the new user on the new database:"
    echo "   postgres=# GRANT ALL PRIVILEGES ON DATABASE your_database TO your_username;"
    echo "5. Exit the PostgreSQL shell:"
    echo "   postgres=# \\q              ,        ,"
    echo "                              /(        )\`"
    echo "                              \ \___   / |"
    echo "                              /- _  \`-/  '"
    echo "                             (/\\/ \ \   /\\"
    echo "                             / /   | \`    \\"
    echo "                             O O   ) /    |"
    echo "                             \`-^--'\`<     '"
    echo "                            (_.)  _  )   /"
    echo "                             \`.___/   /"
    echo "                               \`-----' /"
    echo "                          <----.     __\ "
    echo "                          <----|====O)))==)"
    echo "                          <----'    \`--'"
    echo "                               \`-----'"
    echo " "
    echo "==========================================="
}

    



    echo "   postgres=# GRANT ALL PRIVILEGES ON DATABASE your_database TO your_username;"
    echo "5. Exit the PostgreSQL shell:"
    echo "   postgres=# \\q"
    echo "==========================================="
    echo ""
}

# Main script flow
main() {
    display_clean

    # Confirm PostgreSQL version
    while true; do
        echo "Choose PostgreSQL version to install (15, 16, 17):"
        read version
        if [ "$version" = "15" ] || [ "$version" = "16" ] || [ "$version" = "17" ]; then
            break
        else
            echo "Invalid input. Please enter one of the versions: 15, 16, 17."
        fi
    done

    # Confirm PostgreSQL installation
    while true; do
        echo "Do you want to install PostgreSQL $version and configure it? (y/n):"
        read choice
        if [ "$choice" = "y" ] || [ "$choice" = "n" ]; then
            break
        else
            echo "Invalid input. Please enter 'y' for yes or 'n' for no."
        fi
    done

    if [ "$choice" = "y" ]; then
        # Install PostgreSQL for the selected version
        install_postgresql "$version"

        # Configure PostgreSQL with pg_hba.conf
        configure_postgresql "$version"

        # Create and delete a test database
        create_and_delete_test_db

        echo "PostgreSQL $version installation and configuration completed successfully."

        # Display instructions for creating a new user and database
        display_instructions
    else
        echo "PostgreSQL $version installation skipped."
    fi
}

# Run the main script
main
