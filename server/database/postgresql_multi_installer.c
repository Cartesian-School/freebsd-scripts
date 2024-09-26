#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// Function to display and clear the screen
void display_clean() {
    system("clear");
    printf("\n");
}

// Function to run system commands
void run_command(const char* command) {
    int ret = system(command);
    if (ret != 0) {
        printf("Command failed: %s\n", command);
        exit(1);
    }
}

// Function to install PostgreSQL for a specific version
void install_postgresql(const char* version) {
    printf("Installing PostgreSQL %s and necessary dependencies...\n", version);

    // Construct the package names for the selected version
    char package_command[256];
    snprintf(package_command, sizeof(package_command), "pkg install -y postgresql%s-server postgresql%s-client py311-psycopg2 py311-psycopg2cffi py311-types-psycopg2", version, version);
    
    // Install PostgreSQL server, client, and psycopg2 dependencies
    run_command(package_command);

    // Enable PostgreSQL service
    run_command("sysrc postgresql_enable=YES");

    // Initialize the PostgreSQL database cluster
    printf("Initializing PostgreSQL database...\n");
    run_command("/usr/local/etc/rc.d/postgresql initdb");

    // Start PostgreSQL service
    run_command("service postgresql start");

    // Check PostgreSQL service status
    run_command("service postgresql status");
}

// Function to configure PostgreSQL (pg_hba.conf)
void configure_postgresql(const char* version) {
    // Construct the path to the postgresql.conf and pg_hba.conf files
    char conf_path[256];
    snprintf(conf_path, sizeof(conf_path), "/var/db/postgres/data%s/postgresql.conf", version);
    
    // Print the current listen_addresses setting from postgresql.conf
    char grep_command[256];
    snprintf(grep_command, sizeof(grep_command), "grep listen_addresses %s", conf_path);
    run_command(grep_command);

    // Backup the original pg_hba.conf
    char pg_hba_conf_path[256];
    snprintf(pg_hba_conf_path, sizeof(pg_hba_conf_path), "/var/db/postgres/data%s/pg_hba.conf", version);
    char backup_command[256];
    snprintf(backup_command, sizeof(backup_command), "cp -p %s %s.org", pg_hba_conf_path, pg_hba_conf_path);
    run_command(backup_command);

    // Update pg_hba.conf with new settings
    printf("Configuring pg_hba.conf...\n");
    FILE* file = fopen(pg_hba_conf_path, "w");
    if (file == NULL) {
        printf("Error opening %s for writing.\n", pg_hba_conf_path);
        exit(1);
    }

    fprintf(file, "local   all             all                                     peer\n");
    fprintf(file, "host    all             all             127.0.0.1/32            ident\n");
    fprintf(file, "host    all             all             ::1/128                 ident\n");
    fprintf(file, "local   replication     all                                     peer\n");
    fprintf(file, "host    replication     all             127.0.0.1/32            ident\n");
    fprintf(file, "host    replication     all             ::1/128                 ident\n");

    fclose(file);
    printf("pg_hba.conf configured successfully.\n");

    // Restart PostgreSQL service to apply the changes
    run_command("service postgresql restart");
}

// Function to create and delete a test database
void create_and_delete_test_db() {
    printf("Creating test database 'test_db'...\n");

    // Create the test database, user, and insert data
    const char* sql_commands = 
        "sudo -u postgres psql -c \"CREATE DATABASE test_db;\" && "
        "sudo -u postgres psql -c \"CREATE USER test_user WITH PASSWORD 'password';\" && "
        "sudo -u postgres psql -c \"GRANT ALL PRIVILEGES ON DATABASE test_db TO test_user;\" && "
        "sudo -u postgres psql -d test_db -c \"CREATE TABLE test_table (id SERIAL PRIMARY KEY, message TEXT);\" && "
        "sudo -u postgres psql -d test_db -c \"INSERT INTO test_table (message) VALUES ('All OK');\" && "
        "sudo -u postgres psql -d test_db -c \"SELECT * FROM test_table;\"";

    run_command(sql_commands);

    // Drop the test database and user
    run_command("sudo -u postgres psql -c \"DROP DATABASE test_db;\" && sudo -u postgres psql -c \"DROP USER test_user;\"");

    printf("Test database 'test_db' and user 'test_user' were successfully deleted.\n");
}

// Function to display instructions for creating a new user and database
void display_instructions() {
    printf("\n===========================================\n");
    printf("Steps to create a new PostgreSQL user and database:\n");
    printf("1. Log in to the PostgreSQL shell as the superuser:\n");
    printf("   $ sudo -u postgres psql\n");
    printf("2. Create a new user:\n");
    printf("   postgres=# CREATE USER your_username WITH PASSWORD 'your_password';\n");
    printf("3. Create a new database:\n");
    printf("   postgres=# CREATE DATABASE your_database;\n");
    printf("4. Grant privileges to the new user on the new database:\n");
    printf("   postgres=# GRANT ALL PRIVILEGES ON DATABASE your_database TO your_username;\n");
    printf("5. Exit the PostgreSQL shell:\n");
    printf("   postgres=# \\q\n");
    printf("===========================================\n\n");
}

// Main script flow
int main() {
    display_clean();

    char version[10];
    char choice[10];

    // Confirm PostgreSQL version
    while (1) {
        printf("Choose PostgreSQL version to install (15, 16, 17): ");
        scanf("%s", version);

        if (strcmp(version, "15") == 0 || strcmp(version, "16") == 0 || strcmp(version, "17") == 0) {
            break;
        } else {
            printf("Invalid input. Please enter one of the versions: 15, 16, 17.\n");
        }
    }

    // Confirm PostgreSQL installation
    while (1) {
        printf("Do you want to install PostgreSQL %s and configure it? (y/n): ", version);
        scanf("%s", choice);

        if (strcmp(choice, "y") == 0 || strcmp(choice, "n") == 0) {
            break;
        } else {
            printf("Invalid input. Please enter 'y' for yes or 'n' for no.\n");
        }
    }

    if (strcmp(choice, "y") == 0) {
        // Install PostgreSQL for the selected version
        install_postgresql(version);
        
        // Configure PostgreSQL with pg_hba.conf
        configure_postgresql(version);

        // Create and delete a test database
        create_and_delete_test_db();
        
        printf("PostgreSQL %s installation and configuration completed successfully.\n", version);

        // Display instructions for creating a new user and database
        display_instructions();
    } else {
        printf("PostgreSQL %s installation skipped.\n", version);
    }

    return 0;
}
