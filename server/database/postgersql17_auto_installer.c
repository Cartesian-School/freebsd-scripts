#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// Function to display and clean the screen
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

// Function to install PostgreSQL 17 and necessary dependencies
void install_postgresql17() {
    printf("Installing PostgreSQL 17 and necessary dependencies...\n");

    // Install PostgreSQL 17 server, client, and psycopg2 dependencies
    run_command("pkg install -y postgresql17-server postgresql17-client py311-psycopg2 py311-psycopg2cffi py311-types-psycopg2");

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
void configure_postgresql() {
    // Print the current listen_addresses setting from postgresql.conf
    run_command("grep listen_addresses /var/db/postgres/data17/postgresql.conf");

    // Backup the original pg_hba.conf
    run_command("cp -p /var/db/postgres/data17/pg_hba.conf /var/db/postgres/data17/pg_hba.conf.org");

    // Update pg_hba.conf with new settings
    const char* pg_hba_conf_path = "/var/db/postgres/data17/pg_hba.conf";
    printf("Configuring pg_hba.conf...\n");

    FILE* file = fopen(pg_hba_conf_path, "w");
    if (file == NULL) {
        printf("Error opening pg_hba.conf for writing.\n");
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

    char choice[10];
    while (1) {
        printf("Do you want to install PostgreSQL 17 and configure it? (y/n): ");
        scanf("%s", choice);

        if (strcmp(choice, "y") == 0 || strcmp(choice, "n") == 0) {
            break;
        } else {
            printf("Invalid input. Please enter 'y' for yes or 'n' for no.\n");
        }
    }

    if (strcmp(choice, "y") == 0) {
        // Install PostgreSQL 17 and necessary dependencies
        install_postgresql17();
        
        // Configure PostgreSQL with pg_hba.conf
        configure_postgresql();
        
        printf("PostgreSQL 17 installation and configuration completed successfully.\n");
        display_instructions();
    } else {
        printf("PostgreSQL installation skipped.\n");
    }

    return 0;
}
