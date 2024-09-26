import subprocess
import os
import sys

# Function to display and clean the screen
def display_clean():
    os.system('clear')
    print("")

# Function to install necessary dependencies and PostgreSQL 17
def install_postgresql17():
    print("Installing PostgreSQL 17 and necessary dependencies...")
    
    # Install PostgreSQL 17 server, client, and psycopg2 dependencies
    subprocess.run(["pkg", "install", "-y", "postgresql17-server", "postgresql17-client", "py311-psycopg2", "py311-psycopg2cffi", "py311-types-psycopg2"], check=True)
    
    # Enable PostgreSQL service
    subprocess.run(["sysrc", "postgresql_enable=YES"], check=True)

    # Initialize the PostgreSQL database cluster
    print("Initializing PostgreSQL database...")
    subprocess.run(["/usr/local/etc/rc.d/postgresql", "initdb"], check=True)

    # Start PostgreSQL service
    subprocess.run(["service", "postgresql", "start"], check=True)

    # Check PostgreSQL service status
    subprocess.run(["service", "postgresql", "status"], check=True)

# Function to configure PostgreSQL (pg_hba.conf)
def configure_postgresql():
    # Print the current listen_addresses setting from postgresql.conf
    subprocess.run(["grep", "listen_addresses", "/var/db/postgres/data17/postgresql.conf"], check=True)

    # Backup the original pg_hba.conf
    subprocess.run(["cp", "-p", "/var/db/postgres/data17/pg_hba.conf", "/var/db/postgres/data17/pg_hba.conf.org"], check=True)
    
    # Update pg_hba.conf with new settings
    pg_hba_conf_path = "/var/db/postgres/data17/pg_hba.conf"
    
    print("Configuring pg_hba.conf...")
    pg_hba_content = '''
    local   all             all                                     peer
    host    all             all             127.0.0.1/32            ident
    host    all             all             ::1/128                 ident
    local   replication     all                                     peer
    host    replication     all             127.0.0.1/32            ident
    host    replication     all             ::1/128                 ident
    '''
    
    with open(pg_hba_conf_path, 'w') as f:
        f.write(pg_hba_content)
    
    print("pg_hba.conf configured successfully.")

    # Restart PostgreSQL service to apply the changes
    subprocess.run(["service", "postgresql", "restart"], check=True)

# Main script flow
def main():
    display_clean()

    # Confirm PostgreSQL installation
    while True:
        choice = input("Do you want to install PostgreSQL 17 and configure it? (y/n): ").strip().lower()
        if choice in ['y', 'n']:
            break
        print("Invalid input. Please enter 'y' for yes or 'n' for no.")

    if choice == 'y':
        # Install PostgreSQL 17 and necessary dependencies
        install_postgresql17()
        
        # Configure PostgreSQL with pg_hba.conf
        configure_postgresql()
        
        print("PostgreSQL 17 installation and configuration completed successfully.")
    else:
        print("PostgreSQL installation skipped.")

# Run the main script
if __name__ == "__main__":
    main()
