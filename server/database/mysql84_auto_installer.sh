#!/bin/sh

# Function to display and clean the screen
display_clean() {
    clear
    echo ""
}

# Function to run a system command and handle errors
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

# Function to install MySQL 8.4
install_mysql() {
    echo "Installing MySQL 8.4 server and client..."

    # Install MySQL 8.4 server and client
    run_command "pkg install -y mysql84-server mysql84-client"

    # Enable and start MySQL service
    run_command "sysrc mysql_enable=YES"
    run_command "service mysql-server start"
}

# Function to configure charset in MySQL
configure_mysql_charset() {
    charset_conf="/usr/local/etc/mysql/conf.d/charset.cnf"
    echo "Configuring MySQL charset to use utf8mb4..."

    # Create the charset configuration
    cat > "$charset_conf" << EOF
[mysqld]
character-set-server = utf8mb4

[client]
default-character-set = utf8mb4
EOF

    echo "Charset configured to utf8mb4."
}

# Function to secure MySQL installation
secure_mysql_installation() {
    echo "Securing MySQL installation..."
    run_command "mysql_secure_installation"
}

# Function to configure firewall (optional)
configure_firewall() {
    echo "Configuring firewall to allow MySQL access on port 3306..."

    # Allow MySQL through the firewall and make the change permanent
    run_command "firewall-cmd --add-service=mysql"
    run_command "firewall-cmd --runtime-to-permanent"
}

# Function to create and delete a test database
create_and_delete_test_db() {
    echo "Creating test database and table..."

    # Create a test database, insert data, and delete it
    run_command "mysql -u root -p -e \"
        CREATE DATABASE test_database;
        CREATE TABLE test_database.test_table (id INT PRIMARY KEY, name VARCHAR(50), address VARCHAR(50));
        INSERT INTO test_database.test_table(id, name, address) VALUES(1, 'CentOS', 'Hiroshima');
        SELECT * FROM test_database.test_table;
        DROP DATABASE test_database;
    \""
    
    echo "Test database created, verified, and deleted successfully."
}

# Function to display instructions for creating a new user and database
display_instructions() {
    echo "\n==========================================="
    echo "Steps to create a new MySQL user and database:"
    echo ""
    echo "1. Log in to MySQL as root:"
    echo "   \$ mysql -u root -p"
    echo "   (Enter the MySQL root password)"
    echo "2. Create a new user:"
    echo "   mysql> CREATE USER 'new_user'@'localhost' IDENTIFIED BY 'password';"
    echo "3. Grant all privileges to the new user:"
    echo "   mysql> GRANT ALL PRIVILEGES ON *.* TO 'new_user'@'localhost';"
    echo "4. Create a new database:"
    echo "   mysql> CREATE DATABASE new_database;"
    echo "5. Grant privileges to the new user on the new database:"
    echo "   mysql> GRANT ALL PRIVILEGES ON new_database.* TO 'new_user'@'localhost';"
    echo "6. Exit MySQL:"
    echo "   mysql> exit;"
    echo "7. Log in to MySQL as the new user and create tables in the new database:"
    echo "   \$ mysql -u new_user -p new_database"
    echo "   (Enter the password for the new user)"
    echo "8. Create a new table:"
    echo "   mysql> CREATE TABLE new_table (id INT PRIMARY KEY, name VARCHAR(50), address VARCHAR(50));"
    echo "9. Insert data into the table:"
    echo "   mysql> INSERT INTO new_table (id, name, address) VALUES (1, 'FreeBSD', 'Boston');"
    echo "10. Query the table:"
    echo "   mysql> SELECT * FROM new_table;"
    echo "11. Exit MySQL:"
    echo "   mysql> exit;"
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
}

# Main script flow
main() {
    display_clean

    while true; do
        echo "Do you want to install MySQL 8.4 and configure it? (y/n):"
        read choice

        if [ "$choice" = "y" ] || [ "$choice" = "Y" ]; then
            break
        elif [ "$choice" = "n" ] || [ "$choice" = "N" ]; then
            echo "MySQL installation skipped."
            exit 0
        else
            echo "Invalid input. Please enter 'y' for yes or 'n' for no."
        fi
    done

    # Install MySQL 8.4 server and client
    install_mysql

    # Configure MySQL charset to utf8mb4
    configure_mysql_charset

    # Secure MySQL installation
    secure_mysql_installation

    # Configure firewall to allow MySQL access (optional)
    configure_firewall

    # Create and delete a test database
    create_and_delete_test_db

    echo "MySQL 8.4 installation and configuration completed successfully."

    # Display instructions for creating a new user and database
    display_instructions
}

main
