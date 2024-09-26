#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// Function to display and clear the screen
void display_clean() {
    system("clear");
    printf("\n");
}

// Function to run a system command
void run_command(const char* command) {
    int ret = system(command);
    if (ret != 0) {
        printf("Command failed: %s\n", command);
        exit(1);
    }
}

// Function to install MySQL 8.4
void install_mysql() {
    printf("Installing MySQL 8.4 server and client...\n");

    // Install MySQL 8.4 server and client
    run_command("pkg install -y mysql84-server mysql84-client");

    // Enable and start MySQL service
    run_command("sysrc mysql_enable=YES");
    run_command("service mysql-server start");
}

// Function to configure charset in MySQL
void configure_mysql_charset() {
    const char* charset_conf = "/usr/local/etc/mysql/conf.d/charset.cnf";
    printf("Configuring MySQL charset to use utf8mb4...\n");

    // Create the charset configuration
    FILE* file = fopen(charset_conf, "w");
    if (file == NULL) {
        printf("Error opening file %s for writing.\n", charset_conf);
        exit(1);
    }

    fprintf(file, "[mysqld]\ncharacter-set-server = utf8mb4\n\n");
    fprintf(file, "[client]\ndefault-character-set = utf8mb4\n");
    fclose(file);

    printf("Charset configured to utf8mb4.\n");
}

// Function to secure MySQL installation
void secure_mysql_installation() {
    printf("Securing MySQL installation...\n");
    run_command("mysql_secure_installation");
}

// Function to configure firewall (optional)
void configure_firewall() {
    printf("Configuring firewall to allow MySQL access on port 3306...\n");
    
    // Allow MySQL through the firewall and make the change permanent
    run_command("firewall-cmd --add-service=mysql");
    run_command("firewall-cmd --runtime-to-permanent");
}

// Function to create and delete a test database
void create_and_delete_test_db() {
    printf("Creating test database and table...\n");

    // Commands to create a test database, insert data, and delete it
    const char* commands = 
        "mysql -u root -p <<EOF\n"
        "CREATE DATABASE test_database;\n"
        "CREATE TABLE test_database.test_table (id INT PRIMARY KEY, name VARCHAR(50), address VARCHAR(50));\n"
        "INSERT INTO test_database.test_table(id, name, address) VALUES(1, 'CentOS', 'Hiroshima');\n"
        "SELECT * FROM test_database.test_table;\n"
        "DROP DATABASE test_database;\n"
        "EOF";

    run_command(commands);
    printf("Test database created, verified, and deleted successfully.\n");
}

// Function to display instructions for creating a new user and database
void display_instructions() {
    printf("\n===========================================\n");
    printf("Steps to create a new MySQL user and database:\n\n");
    printf("1. Log in to MySQL as root:\n");
    printf("   $ mysql -u root -p\n");
    printf("   (Enter the MySQL root password)\n\n");

    printf("2. Create a new user:\n");
    printf("   mysql> CREATE USER 'new_user'@'localhost' IDENTIFIED BY 'password';\n\n");

    printf("3. Grant all privileges to the new user:\n");
    printf("   mysql> GRANT ALL PRIVILEGES ON *.* TO 'new_user'@'localhost';\n\n");

    printf("4. Create a new database:\n");
    printf("   mysql> CREATE DATABASE new_database;\n\n");

    printf("5. Grant privileges to the new user on the new database:\n");
    printf("   mysql> GRANT ALL PRIVILEGES ON new_database.* TO 'new_user'@'localhost';\n\n");

    printf("6. Exit MySQL:\n");
    printf("   mysql> exit;\n\n");

    printf("7. Log in to MySQL as the new user and create tables in the new database:\n");
    printf("   $ mysql -u new_user -p new_database\n");
    printf("   (Enter the password for the new user)\n\n");

    printf("8. Create a new table:\n");
    printf("   mysql> CREATE TABLE new_table (id INT PRIMARY KEY, name VARCHAR(50), address VARCHAR(50));\n\n");

    printf("9. Insert data into the table:\n");
    printf("   mysql> INSERT INTO new_table (id, name, address) VALUES (1, 'FreeBSD', 'Boston');\n\n");

    printf("10. Query the table:\n");
    printf("   mysql> SELECT * FROM new_table;\n\n");

    printf("11. Exit MySQL:\n");
    printf("   mysql> exit;\n");
    printf("===========================================\n\n");
}

// Main script flow
int main() {
    display_clean();

    char choice[10];
    printf("Do you want to install MySQL 8.4 and configure it? (y/n): ");
    scanf("%s", choice);

    if (strcmp(choice, "y") == 0 || strcmp(choice, "Y") == 0) {
        // Install MySQL 8.4 server and client
        install_mysql();
        
        // Configure MySQL charset to utf8mb4
        configure_mysql_charset();

        // Secure MySQL installation
        secure_mysql_installation();

        // Configure firewall to allow MySQL access (optional)
        configure_firewall();

        // Create and delete a test database
        create_and_delete_test_db();

        printf("MySQL 8.4 installation and configuration completed successfully.\n");
        
        // Display instructions for creating a new user and database
        display_instructions();
    } else {
        printf("MySQL installation skipped.\n");
    }

    return 0;
}
