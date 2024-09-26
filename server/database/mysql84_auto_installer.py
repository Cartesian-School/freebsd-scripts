import subprocess
import os

# Function to display and clear the screen
def display_clean():
    os.system('clear')
    print("")

# Function to install MySQL 8.4
def install_mysql():
    print("Installing MySQL 8.4 server and client...")

    # Install MySQL 8.4 server and client
    subprocess.run(["pkg", "install", "-y", "mysql84-server", "mysql84-client"], check=True)

    # Enable and start MySQL service
    subprocess.run(["sysrc", "mysql_enable=YES"], check=True)
    subprocess.run(["service", "mysql-server", "start"], check=True)

# Function to configure charset in MySQL
def configure_mysql_charset():
    charset_conf = '/usr/local/etc/mysql/conf.d/charset.cnf'
    
    # Ensure conf.d directory exists
    os.makedirs(os.path.dirname(charset_conf), exist_ok=True)

    # Add charset configuration
    print("Configuring MySQL charset to use utf8mb4...")
    with open(charset_conf, 'w') as f:
        f.write('''[mysqld]
character-set-server = utf8mb4

[client]
default-character-set = utf8mb4
''')
    print("Charset configured to utf8mb4.")

# Function to run mysql_secure_installation equivalent
def secure_mysql_installation():
    print("Securing MySQL installation...")

    # Run mysql_secure_installation using non-interactive way
    subprocess.run(["mysql_secure_installation"], check=True)

# Function to configure firewall (optional)
def configure_firewall():
    print("Configuring firewall to allow MySQL access on port 3306...")
    
    # Allow MySQL through firewall and make it permanent
    subprocess.run(["firewall-cmd", "--add-service=mysql"], check=True)
    subprocess.run(["firewall-cmd", "--runtime-to-permanent"], check=True)

# Function to create and delete a test database
def create_and_delete_test_db():
    print("Creating test database and table...")

    # Connect to MySQL as root
    conn = subprocess.Popen(['mysql', '-u', 'root', '-p'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    
    commands = '''
    CREATE DATABASE test_database;
    CREATE TABLE test_database.test_table (id INT PRIMARY KEY, name VARCHAR(50), address VARCHAR(50));
    INSERT INTO test_database.test_table(id, name, address) VALUES(1, 'CentOS', 'Hiroshima');
    SELECT * FROM test_database.test_table;
    DROP DATABASE test_database;
    exit;
    '''
    
    conn.communicate(commands)
    
    print("Test database created, verified, and deleted successfully.")

# Function to display instructions for creating a new user and database
def display_instructions():
    print("""
    ===========================================
    Steps to create a new MySQL user and database:
    
    1. Log in to MySQL as root:
       $ mysql -u root -p
       (Enter the MySQL root password)

    2. Create a new user:
       mysql> CREATE USER 'new_user'@'localhost' IDENTIFIED BY 'password';

    3. Grant all privileges to the new user:
       mysql> GRANT ALL PRIVILEGES ON *.* TO 'new_user'@'localhost';

    4. Create a new database:
       mysql> CREATE DATABASE new_database;

    5. Grant privileges to the new user on the new database:
       mysql> GRANT ALL PRIVILEGES ON new_database.* TO 'new_user'@'localhost';

    6. Exit MySQL:
       mysql> exit;

    7. Log in to MySQL as the new user and create tables in the new database:
       $ mysql -u new_user -p new_database
       (Enter the password for the new user)

    8. Create a new table:
       mysql> CREATE TABLE new_table (id INT PRIMARY KEY, name VARCHAR(50), address VARCHAR(50));

    9. Insert data into the table:
       mysql> INSERT INTO new_table (id, name, address) VALUES (1, 'FreeBSD', 'Boston');

    10. Query the table:
       mysql> SELECT * FROM new_table;

    11. Exit MySQL:
       mysql> exit;
    ===========================================
    """)

# Main script flow
def main():
    display_clean()

    # Confirm MySQL installation
    while True:
        choice = input("Do you want to install MySQL 8.4 and configure it? (y/n): ").strip().lower()
        if choice in ['y', 'n']:
            break
        print("Invalid input. Please enter 'y' for yes or 'n' for no.")

    if choice == 'y':
        # Install MySQL 8.4 server and client
        install_mysql()
        
        # Configure MySQL charset to utf8mb4
        configure_mysql_charset()

        # Secure MySQL installation
        secure_mysql_installation()

        # Configure firewall to allow MySQL access (optional)
        configure_firewall()

        # Create and delete a test database
        create_and_delete_test_db()

        print("MySQL 8.4 installation and configuration completed successfully.")
        
        # Display instructions for creating a new user and database
        display_instructions()
    else:
        print("MySQL installation skipped.")

# Run the main script
if __name__ == "__main__":
    main()
